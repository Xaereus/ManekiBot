import random
from copy import deepcopy
from .utils.dataIO import dataIO
from .utils.text_formatter import txt_frmt
from discord.ext import commands


class TalkerCog:
    """
    TalkerCog is a cog that talks back. Sass included, batteries not included.
    -- Designed for use with Cueball --
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.responses = dataIO.load_json('conversation/responses.json')
        self.personalized = dataIO.load_json('conversation/personalized.json')

    @staticmethod
    def check_response(message, responses):
        """Loops through the responses dict and returns the first valid response."""
        for resp in responses.values():
            if txt_frmt.regscan(message.content, resp['settings']['regex'],
                                clean_str = bool('clean' not in resp['settings'])):
                return {'response': random.choice(resp['responses'])}
        return None

    async def on_message(self, message):
        if message.content.startswith("!!") or message.author == self.bot.user:
            return

        responses = deepcopy(self.responses)
        personalized = deepcopy(self.personalized)

        # Personalized response checker.
        if str(message.author.id) in self.personalized:
            if "ignored" in self.personalized[str(message.author.id)]:
                return

            dataIO.merge(responses, personalized[str(message.author.id)])

        response = self.check_response(message, responses)

        if response is not None:
            await message.channel.send(response['response'])


def setup(bot):
    bot.add_cog(TalkerCog(bot))
