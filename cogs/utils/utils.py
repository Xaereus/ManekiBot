from datetime import timedelta
from random import choice, randrange
from discord import Color


def rnd_color_hex():
    """Returns a randomized hexademical value that can be used as a color."""
    return int(''.join([choice('0123456789ABCDEF') for x in range(6)]), 16)


def rnd_color_discord():
    """Returns a discord.Color object with a random value."""
    return Color(value = rnd_color_hex())


def random_date(start, end):
    """Return a random datetime between two datetime objects."""
    return start + timedelta(days = randrange((end - start).days))


def clamp(val: int, mx: int, mn: int):
    """
    Returns mx if val > mx. Returns mn if val < mn. Returns val otherwise.

    :param val: Value being clamped
    :param mx: Maximum allowed integer for val
    :param mn: Minimum allowed value for val
    :return: int
    """
    if val > mx:
        return mx
    elif val < mn:
        return mn
    return val


def emojit(val):
    vals = {'0': "\N{DIGIT ZERO}\N{COMBINING ENCLOSING KEYCAP}",
            '1': "\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",
            '2': "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",
            '3': "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",
            '4': "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",
            '5': "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}",
            '6': "\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}",
            '7': "\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}",
            '8': "\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}",
            '9': "\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}",
            'a': "\N{Latin Capital letter A}",
            'b': "\N{Latin Capital letter B}",
            'c': "\N{Latin Capital letter C}",
            'd': "\N{Latin Capital letter D}",
            'e': "\N{Latin Capital letter E}",
            'f': "\N{Latin Capital letter F}",
            'g': "\N{Latin Capital letter G}",
            'h': "\N{Latin Capital letter H}",
            'i': "\N{Latin Capital letter I}",
            'j': "\N{Latin Capital letter J}",
            'k': "\N{Latin Capital letter K}",
            'l': "\N{Latin Capital letter L}",
            'm': "\N{Latin Capital letter M}",
            'n': "\N{Latin Capital letter N}",
            'o': "\N{Latin Capital letter O}",
            'p': "\N{Latin Capital letter P}",
            'q': "\N{Latin Capital letter Q}",
            'r': "\N{Latin Capital letter R}",
            's': "\N{Latin Capital letter S}",
            't': "\N{Latin Capital letter T}",
            'u': "\N{Latin Capital letter U}",
            'v': "\N{Latin Capital letter V}",
            'w': "\N{Latin Capital letter W}",
            'x': "\N{Latin Capital letter X}",
            'y': "\N{Latin Capital letter Y}",
            'z': "\N{Latin Capital letter Z}"}

    return vals[str(val)]

