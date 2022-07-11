# -*- coding: UTF-8 -*-

import csv
import os
import sys

import pytest

from .test_apc_csv import RowObject

sys.path.append(os.path.join(sys.path[0], "python"))
import openapc_toolkit as oat

INSTITUTIONS_FILE_PATH = "data/institutions.csv" 
INSTITUTIONS_DATA = []

# Prefix for all error messages
MSG_HEAD = "{}, line {}: "

# Number of expected columns in the institutions file 
EXP_ROW_LENGTH = 12

with open(INSTITUTIONS_FILE_PATH, "r") as f:
    reader = csv.reader(f)
    # Use RowObject to store contextual information along with CSV rows for better error messages
    for row in reader:
        row_object = RowObject("institutions.csv", reader.line_num, row, None)
        INSTITUTIONS_DATA.append(row_object)

@pytest.mark.parametrize("row_object", INSTITUTIONS_DATA)
def test_data_format(row_object):
    if len(row_object.row) != EXP_ROW_LENGTH:
        msg = MSG_HEAD + "Row does not consist of {} columns."
        msg = msg.format(row_object.file_name, row_object.line_number, EXP_ROW_LENGTH)
        pytest.fail(msg)
