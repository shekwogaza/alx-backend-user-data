#!/usr/bin/env python3
"""Module for filtering sensitive information from log messages."""


from typing import List
import re


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
