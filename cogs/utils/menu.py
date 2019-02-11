import asyncio
import contextlib
from typing import Callable, ClassVar, Iterable, List, Optional, Sequence, Tuple, Union

import discord

from . import utils
from .text_formatter import txt_frmt

_ReactableEmoji = Union[str, discord.Emoji]


class Menu:
    def __init__(self, ctx, data: dict, title, page_num: int = 1, timeout = 60, size = 5):
        """
        Emoji controlled menu for selecting functions or commands to be run.

        :param ctx:
            Context from the command that generated this menu.
        :param data:
            A dictionary of {str: func}, where the string is what is displayed on the menu and the function
            is the coroutine called when the string is selected.
        :param title:
            Title of all pages. Expected to generally be the name of the command that created the menu.
        :param page_num:
            The page number to be displayed.
        :param timeout:
            The amount of time in seconds before the menu removes the options and stops working.
        :param size:
            Size of each page. Going above 10 will do bad things, so don't.
        """
        self.ctx = ctx
        self.size = size
        self.title = title
        self.timeout = timeout
        self.msg = None
        self.controls = {"⬅": self.prev_page, "❌": self.close_menu, "➡": self.next_page}

        self.data = list(txt_frmt.d_chunk(data, size))
        self.page_num = utils.clamp(page_num, len(self.pages), 1)

    @property
    def pages(self):
        pages = []
        for p in self.data:
            page = discord.Embed(color = 0xFFFFFF, title = self.title)
            page.add_field(name = f"**Page: {len(pages) + 1}**",
                           value = '\n'.join([f"`{list(p.keys()).index(key)}:` {key}" for key in p.keys()]))
            pages.append(page)
        return pages

    @property
    def curr_page(self):
        return self.pages[self.page_num - 1]

    def set_controls(self, data: dict):
        controls = {"⬅": self.prev_page, "❌": self.close_menu, "➡": self.next_page}
        data = dict(zip([utils.emojit(n) for n in range(0, len(data))], list(data.values())))
        controls.update(data)
        self.controls = controls

    async def set_data(self, data, size = 5):
        """Sets the menu's data to `data` and updates the menu's content."""
        self.data = list(txt_frmt.d_chunk(data, size))
        self.page_num = 1
        await self.update()

    async def update(self):
        if self.msg is None:
            self.msg = await self.ctx.send(embed = self.curr_page)
        else:
            await self.msg.edit(embed = self.curr_page)

        self.set_controls(self.data[self.page_num - 1])
        self.start_adding_reactions(self.controls.keys())

        try:
            react, user = await self.ctx.bot.wait_for(
                "reaction_add",
                check = ReactionPredicate.with_emojis(tuple(self.controls.keys()), self.msg, self.ctx.author),
                timeout = self.timeout
            )
        except asyncio.TimeoutError:
            try:
                await self.msg.clear_reactions()
            except discord.Forbidden:  # cannot remove all reactions
                for key in self.controls.keys():
                    await self.msg.remove_reaction(key, self.ctx.bot.user)
            except discord.NotFound:
                return
        else:
            await self.msg.remove_reaction(react.emoji, user)
            await self.controls[react.emoji](self = self.ctx.bot.get_cog_commands(self.ctx.command.cog_name),
                                             ctx = self.ctx, menu = self)

    async def next_page(self):
        """Changes the page number to +1 of the current. Changes to first page if the current page is the last.
        Updates the menu once the page number is changed."""
        if self.page_num == len(self.pages):
            self.page_num = 1  # Loop around to the first item
        else:
            self.page_num += 1
        return await self.update()

    async def prev_page(self):
        """Changes the page number to -1 of the current. Changes to last page if the current page is the first.
        Updates the menu once the page number is changed."""
        if self.page_num == 1:
            self.page_num = len(self.pages)  # Loop around to the last item
        else:
            self.page_num -= 1
        return await self.update()

    async def close_menu(self):
        with contextlib.suppress(discord.NotFound):
            await self.msg.delete()

    def start_adding_reactions(self, emojis: Iterable[_ReactableEmoji]) -> asyncio.Task:
        """Start adding reactions to a message.
        This is a non-blocking operation - calling this will schedule the
        reactions being added, but the calling code will continue to
        execute asynchronously. There is no need to await this function.
        This is particularly useful if you wish to start waiting for a
        reaction whilst the reactions are still being added - in fact,
        this is exactly what `menu` uses to do that.
        This spawns a `asyncio.Task` object and schedules it on ``loop``.
        If ``loop`` omitted, the loop will be retrieved with
        `asyncio.get_event_loop`.
        Parameters
        ----------
        emojis : Iterable[Union[str, discord.Emoji]]
            The emojis to react to the message with.
        Returns
        -------
        asyncio.Task
            The task for the coroutine adding the reactions.
        """

        async def task():
            # The task should exit silently if the message is deleted
            with contextlib.suppress(discord.NotFound):
                for emoji in emojis:
                    await self.msg.add_reaction(emoji)

        if self.ctx.bot.loop is None:
            self.ctx.bot.loop = asyncio.get_event_loop()

        return self.ctx.bot.loop.create_task(task())


class ReactionPredicate(Callable[[discord.Reaction, discord.abc.User], bool]):
    """Borrowed from RedBot.

    A collection of predicates for reaction events.
    All checks are combined with :meth:`ReactionPredicate.same_context`.
    Examples
    --------
    Confirming a yes/no question with a tick/cross reaction::
        from redbot.core.utils.predicates import ReactionPredicate
        from redbot.core.utils.menus import start_adding_reactions
        msg = await ctx.send("Yes or no?")
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)
        if pred.result is True:
            # User responded with tick
            ...
        else:
            # User responded with cross
            ...
    Waiting for the first reaction from any user with one of the first
    5 letters of the alphabet::
        from redbot.core.utils.predicates import ReactionPredicate
        from redbot.core.utils.menus import start_adding_reactions
        msg = await ctx.send("React to me!")
        emojis = ReactionPredicate.ALPHABET_EMOJIS[:5]
        start_adding_reactions(msg, emojis)
        pred = ReactionPredicate.with_emojis(emojis, msg)
        await ctx.bot.wait_for("reaction_add", check=pred)
        # pred.result is now the index of the letter in `emojis`
    Attributes
    ----------
    result : Any
        The object which the message content matched with. This is
        dependent on the predicate used - see each predicate's
        documentation for details, not every method will assign this
        attribute. Defaults to ``None``.
    """

    YES_OR_NO_EMOJIS: ClassVar[Tuple[str, str]] = (
        "\N{WHITE HEAVY CHECK MARK}",
        "\N{NEGATIVE SQUARED CROSS MARK}",
    )
    """Tuple[str, str] : A tuple containing the tick emoji and cross emoji, in that order."""

    ALPHABET_EMOJIS: ClassVar[List[str]] = [
        chr(code)
        for code in range(
            ord("\N{REGIONAL INDICATOR SYMBOL LETTER A}"),
            ord("\N{REGIONAL INDICATOR SYMBOL LETTER Z}") + 1,
        )
    ]
    """List[str] : A list of all 26 alphabetical letter emojis."""

    NUMBER_EMOJIS: ClassVar[List[str]] = [
        chr(code) + "\N{COMBINING ENCLOSING KEYCAP}" for code in range(ord("0"), ord("9") + 1)
    ]
    """List[str] : A list of all single-digit number emojis, 0 through 9."""

    def __init__(
            self, predicate: Callable[["ReactionPredicate", discord.Reaction, discord.abc.User], bool]
    ) -> None:
        self._pred: Callable[
            ["ReactionPredicate", discord.Reaction, discord.abc.User], bool
        ] = predicate
        self.result = None

    def __call__(self, reaction: discord.Reaction, user: discord.abc.User) -> bool:
        return self._pred(self, reaction, user)

    # noinspection PyUnusedLocal
    @classmethod
    def same_context(
            cls, message: Optional[discord.Message] = None, user: Optional[discord.abc.User] = None
    ) -> "ReactionPredicate":
        """Match if a reaction fits the described context.
        This will ignore reactions added by the bot user, regardless
        of whether or not ``user`` is supplied.
        Parameters
        ----------
        message : Optional[discord.Message]
            The message which we expect a reaction to. If unspecified,
            the reaction's message will be ignored.
        user : Optional[discord.abc.User]
            The user we expect to react. If unspecified, the user who
            added the reaction will be ignored.
        Returns
        -------
        ReactionPredicate
            The event predicate.
        """
        # noinspection PyProtectedMember
        me_id = message._state.self_id
        return cls(
            lambda self, r, u: u.id != me_id
                               and (message is None or r.message.id == message.id)
                               and (user is None or u.id == user.id)
        )

    @classmethod
    def with_emojis(
            cls,
            emojis: Sequence[Union[str, discord.Emoji, discord.PartialEmoji]],
            message: Optional[discord.Message] = None,
            user: Optional[discord.abc.User] = None,
    ) -> "ReactionPredicate":
        """Match if the reaction is one of the specified emojis.
        Parameters
        ----------
        emojis : Sequence[Union[str, discord.Emoji, discord.PartialEmoji]]
            The emojis of which one we expect to be reacted.
        message : discord.Message
            Same as ``message`` in :meth:`same_context`.
        user : Optional[discord.abc.User]
            Same as ``user`` in :meth:`same_context`.
        Returns
        -------
        ReactionPredicate
            The event predicate.
        """
        same_context = cls.same_context(message, user)

        def predicate(self: ReactionPredicate, r: discord.Reaction, u: discord.abc.User):
            if not same_context(r, u):
                return False

            try:
                self.result = emojis.index(r.emoji)
            except ValueError:
                return False
            else:
                return True

        return cls(predicate)

    @classmethod
    def yes_or_no(
            cls, message: Optional[discord.Message] = None, user: Optional[discord.abc.User] = None
    ) -> "ReactionPredicate":
        """Match if the reaction is a tick or cross emoji.
        The emojis used can are in
        `ReactionPredicate.YES_OR_NO_EMOJIS`.
        This will assign ``True`` for *yes*, or ``False`` for *no* to
        the `result` attribute.
        Parameters
        ----------
        message : discord.Message
            Same as ``message`` in :meth:`same_context`.
        user : Optional[discord.abc.User]
            Same as ``user`` in :meth:`same_context`.
        Returns
        -------
        ReactionPredicate
            The event predicate.
        """
        same_context = cls.same_context(message, user)

        def predicate(self: ReactionPredicate, r: discord.Reaction, u: discord.abc.User) -> bool:
            if not same_context(r, u):
                return False

            try:
                self.result = not bool(self.YES_OR_NO_EMOJIS.index(r.emoji))
            except ValueError:
                return False
            else:
                return True

        return cls(predicate)
