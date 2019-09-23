#!/usr/bin/env python3
"""Script to convert DIPS metadata spreadsheets into ArchivesSpace input.
Input is a DIPS formatted CSV spreadsheet. Output is a CSV that uses the
proper header row and fields for upload to ArchivesSpace.
"""

from os import path
from time import strftime

# TODO: Don't forget to fix Excell spaces with "strip"

def get_file():
    return "/Users/limen/Desktop/"

def main():
    dips_csv = get_file()
    aspace_csv = path.join(path.dirname(dips_csv), f'as_import_{strftime("%Y%m%d_%H%M%S")}.csv')


if __name__ == '__main__':
    main()
