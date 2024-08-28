#!/usr/bin/env python3
"""Module for filtering sensitive information from log messages."""


import logging
from typing import List
import re


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """_summary_

        Args:
            fields (List[str]): _description_
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """_summary_

        Args:
            record (logging.LogRecord): _description_

        Returns:
            str: _description_
        """
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """_summary_

    Args:
        fields (_type_): _description_
        redaction (_type_): _description_
        message (_type_): _description_
        separator (_type_): _description_
    """
    return re.sub(
        f'({"|".join(map(re.escape, fields))})=([^{separator}]*)',
        f'\\1={redaction}', message)
