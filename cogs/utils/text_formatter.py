import re


class TextFormatter:
    def regscan(self, string: str, regex: iter, *, clean_str: bool = True):
        """
        Converts a normal string into a regex string. Intended for converting strings from json files.

        :rtype: bool
        :param string: String to search with regex
        :param regex: List of strings or a string of regex
        :param clean_str: If what is being searched is to be run through clean()
        :raises: TypeError
        """

        if clean_str:
            string = self.clean(string)

        if type(regex) == list:
            for reg in regex:
                if bool(re.search(reg, string)):
                    return True
            return False

        elif type(regex) == str:
            return bool(re.search(regex, string))

        else:
            raise TypeError

    @staticmethod
    def clean(string: str, lower = True):
        """
        Returns a cleaned string (as in a string without punctuation) that is lowercase if lower is true.

        :rtype: str
        :param string: String to be cleaned
        :param lower: If cleaned string is lowercase
        """

        return re.sub(r'[^a-z\d\s]+', '', string.lower() if lower else string)

    @staticmethod
    def deblank(iterable: iter):
        """
        Removes all instances of None or "" in a list or values in a dict.

        :rtype: iter
        :param iterable: The list or dict to be
        """

        if type(iterable) == dict:
            newiter = dict()
            for key, value in iterable:
                if value is not None and value != "":
                    newiter[key] = value

        elif type(iterable) == list:
            newiter = list(filter(None, iterable))

        else:
            raise TypeError

        return newiter

    @staticmethod
    def readable_list(sentence: list):
        """
        Takes a list and seperates it into a readable sentence.

        Ex: ['You', 'him', 'I'] -> 'You, him, and I'
            ['You', 'I']        -> 'You and I'
            ['You']             -> 'You'
            []                  -> ''
        """

        if len(sentence) == 0:
            result = ''
        elif len(sentence) == 1:
            result = sentence[0]
        elif len(sentence) == 2:
            result = sentence[0] + 'and' + sentence[1]
        else:
            result = f"{', '.join([word for word in sentence[:-1]])}, and {sentence[-1]} won!"

        return result

    @staticmethod
    def escape(text):
        text = (text.replace("`", "\\`")
                    .replace("*", "\\*")
                    .replace("_", "\\_")
                    .replace("~", "\\~"))
        return text

    # TODO: Test silent_mention().
    @staticmethod
    def silent_mention(text):
        text = text.replace("@", "@\u200B")
        return text


txt_frmt = TextFormatter()
