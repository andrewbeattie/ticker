"""
This module defines a Constants class that stores various constants used in the application.
The constants are implemented as read-only properties to prevent accidental modification.
"""


class Constants:
    def __init__(self):
        self.__BASE_URL: str = "https://www.tickspot.com/api/v2/"
        self.__BASE_URL_SUB_ID: str = "https://www.tickspot.com/%s/api/v2/"
        self.__DATE_FORMAT: str = "%Y-%m-%d"

    @property
    def BASE_URL(self) -> str:
        return self.__BASE_URL

    @property
    def BASE_URL_SUB_ID(self) -> str:
        return self.__BASE_URL_SUB_ID

    @property
    def DATE_FORMAT(self) -> str:
        return self.__DATE_FORMAT

    @BASE_URL.setter
    def BASE_URL(self, value: str):
        raise ValueError('Cannot modify constant BASE_URL')

    @BASE_URL_SUB_ID.setter
    def BASE_URL_SUB_ID(self, value: str):
        raise ValueError('Cannot modify constant BASE_URL_SUB_ID')

    @DATE_FORMAT.setter
    def DATE_FORMAT(self, value: str):
        raise ValueError('Cannot modify constant DATE_FORMAT')
