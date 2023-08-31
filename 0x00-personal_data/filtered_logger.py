#!/usr/bin/env python3
"""Regex-ing"""
import re
from typing import List
import logging
import os
import datetime


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=()):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def filter_datum(self, fields: List[str], redaction: str,
                     message: str, separator: str) -> str:
        """returns the log message obfuscated"""
        if fields in self.fields:
            return self.REDACTION
        return message

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        data = super().format(record)
        for field in self.fields:
            data = data.replace(
                f"{field}=", f"{field}={self.REDACTION}{self.SEPARATOR}")
        return data
