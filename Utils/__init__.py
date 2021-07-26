# coding=utf-8
"""
Class
"""
import sys

true = True
false = False
null = None
empty = ""
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


class System:
    """
    System
    """

    def __init__(self):
        self.out = Out()
        self.err = Err()


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
        sys.stdout.flush()

    @staticmethod
    def print(value: str, iterability: bool = true):
        """

        :type iterability: bool
        :param iterability:
        :param value:
        """
        if iterability:
            sys.stdout.writelines(value)
        else:
            sys.stdout.write(value)


class Err:
    """
    Out
    """

    def __init__(self):
        self.placeholder = null

    @staticmethod
    def println(value):
        """

        :param value:
        """
        sys.stderr.println(value)
        sys.stderr.flush()

    @staticmethod
    def print(value: str, iterability: bool = true):
        """

        :type iterability: bool
        :param iterability:
        :param value:
        """
        if iterability:
            sys.stderr.writelines(value)
        else:
            sys.stderr.write(value)


System = System()
