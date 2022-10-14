#!/usr/bin/python3

# This is a "smart" Minecraft chunk remover to make your world ready for the next Minecraft update or to optimize your survival world for uploading online.
# Author:  Thijmen Voskuilen (https://github.com/thijmer)
# License: GPLv3

#Imports
from genericpath import isfile
import sqlite3
import os.path



# Run the program!
if __name__ == "__main__":
    # Disclaimers
    print("Running this tool could end up destroying your world. Make sure to backup before using this!")
    input("Press enter if you have made a backup. Otherwise, close out of this program.")
    print("\n"*5)

    # Ask for path to the Ledger database. Loop until an existing path is inputted.
    file_found = False
    while not file_found:
        sql_path: str = input("Path of the ledger.sqlite database [ledger.sqlite]: ")
        # Default to the ledger.sqlite in the current directory. (To make debugging less tiresome)
        if not sql_path:
            sql_path = "ledger.sqlite"
         # Check if it actually exists and is a file. Otherwise, just ask again.
        if os.path.exists(sql_path):
            if os.path.isfile(sql_path):
                file_found = True
            else:
                print("'%s' has to be a file." % sql_path)
        else:
            print("'%s': No such file or directory" % sql_path)
    
    # Ask for path to the region file directory. Loop until an existing path is inputted.
    file_found = False
    while not file_found:
        region_path: str = input("Path of the region file directory [region]: ")
        # Default to the region directory in the current directory. (To make debugging less tiresome)
        if not region_path:
            region_path = "region"
        # Check if it actually exists and is a directory. Otherwise, just ask again.
        if os.path.exists(region_path):
            if os.path.isdir(region_path):
                file_found = True
            else:
                print("'%s' has to be a directory." % region_path)
        else:
            print("'%s': No such file or directory" % region_path)