import platform

from .dataIO import dataIO
from copy import deepcopy
from os import listdir


class Settings:
    # TODO: Add documentation for all methods in Settings

    def __init__(self):
        if not dataIO.is_valid_json("botSettings.json"):
            self.bot_settings = {"currActivity": "",
                                 "extensions": {"mamacog": {
                                     "load": True
                                 }},
                                 "guardians": [
                                     466550423969595402,
                                     197544495724756992,
                                     279092204771868672
                                 ]}
            self.save_bot_settings()
        else:
            self.bot_settings = dataIO.load_json("botSettings.json")

        self.check_extensions()

    def save_bot_settings(self):
        """Saves self.bot_settings to a json in the data folder."""
        dataIO.dump_json("botSettings.json", self.bot_settings)

    def check_extensions(self):
        extensions = list(filter(None, [file[:-3] if file[-3:] == '.py' and '__init__' not in file
                                        else None for file in listdir('cogs')]))

        for extension in extensions:
            if extension not in self.extensions:
                self.bot_settings['extensions'][extension] = {'load': False}

        for extension in self.extensions:
            if extension not in extensions:
                self.bot_settings['extensions'].__delitem__(extension)

        self.save_bot_settings()

    def disable_extension(self, extension):
        self.bot_settings['extensions'][extension]['load'] = False
        self.save_bot_settings()

    def enable_extension(self, extension):
        self.bot_settings['extensions'][extension]['load'] = True
        self.save_bot_settings()

    @property
    def current_activity(self):
        return self.bot_settings['currActivity']

    @property
    def token(self):
        with open('token.txt', 'r') as tokentxt:
            token = tokentxt.read()

        if "win" not in str(platform.platform()).lower():
            token = token[:-1]

        return token

    @property
    def guardians(self):
        return self.bot_settings['guardians'].copy()

    @property
    def extensions(self):
        """
        Copy of all extensions for the bot.

        :return: the bot's extensions
        :rtype: dict
        """
        return deepcopy(self.bot_settings['extensions'])

    @property
    def loaded_extensions(self):
        ret = {}
        for extension in self.extensions:
            if self.extensions[extension]['load']:
                ret[extension] = self.extensions[extension]
        return ret

    @property
    def unloaded_extensions(self):
        ret = {}
        for extension in self.extensions:
            if not self.extensions[extension]['load']:
                ret[extension] = self.extensions[extension]
        return ret


# TODO: Remove need to instantiate Settings object outside of Maneki
settings = Settings()
