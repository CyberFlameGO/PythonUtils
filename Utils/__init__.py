# coding=utf-8
"""
Class
"""
true = True
false = False
null = None
empty = ""


class System:
    """
    System
    """

    def __init__(self):
        self.out = Out()


class Out:
    """
    Out
    """
    def __init__(self):
        self.placeholder = null

    @staticmethod
    def println(value, end="\r\n"):
        """

        :param end:
        :param value:
        """
        print(value, end=end)

    @staticmethod
    def print(value, end=empty):
        """

        :param end:
        :param value:
        """
        print(value, end=end)


System = System()
