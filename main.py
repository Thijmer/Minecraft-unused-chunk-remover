#!/usr/bin/python3

# This is a "smart" Minecraft chunk remover to make your world ready for the next Minecraft update or to optimize your survival world for uploading online.
# Author:  Thijmen Voskuilen (https://github.com/thijmer)
# License: GPLv3

#Imports
import sqlite3
import os
import math

def smart_chunk_remover(sql_path, region_path, world=1):
    """
    This is the main function. It calls the functions to index and remove the chunks.
    """
    # Connect to the Ledger database in order to read it
    con = sqlite3.connect(sql_path)

    # Find blocks changed by player activity. The chunks with these blocks in them can be kept.
    changed_coordinates = read_coordinates(con, world)
    
    regions_to_keep = coords_to_chunks(changed_coordinates)
    regions_to_remove = calculate_regions_to_remove(region_path, regions_to_keep)
    remove_regions(region_path, regions_to_remove)
    

def read_coordinates(con, world) -> 'list[tuple[str]]':
    """
    This is the function that reads the sqlite file and lists all of the blocks that have been changed.
    """
    #  Create a cursor to read from the database
    cur = con.cursor()

    # Construct SQL query
    useful_data = ['x', 'z']
    player_source_names = ["player", "command", "explosion", "insert", "remove", "portal"] # Ledger also keeps track of the source of the block change (e.g. fire, tnt, creeper, player).
    
    # The sources are stored as IDs so we need to extract those from a table in the database.
    ID_extraction_query = "SELECT id FROM sources WHERE name = '"
    ID_extraction_query += "' OR name = '".join(player_source_names) + "';"
    player_source_ids = [str(x[0]) for x in cur.execute(ID_extraction_query).fetchall()] # Read the query and put the results into a list

    # Construct the query for the block positions
    query = "SELECT " + ", ".join(useful_data) + " FROM actions WHERE (source = '"
    query += "' OR source = '".join(player_source_ids) + "') AND world_id = '%s';" % world

    # Read the data
    all_coords = cur.execute(query).fetchall()
    return all_coords


def coords_to_chunks(all_coords: 'list[tuple[str]]') -> 'list[str]':
    """Calculate the .mca files all the coords are in"""
    # Each .mca file had 512*512 blocks inside it
    chunks = []
    for coords in all_coords:
        x = coords[0]
        y = coords[1]
        x_region = str(math.floor(x/512))
        y_region = str(math.floor(y/512))
        region = "r.%s.%s.mca" % (x_region, y_region)
        chunks.append(region)
    
    # The above code will list the same mca file many times. We only need them once so this part will remove the double occurances
    chunks = list(set(chunks))
    return chunks

def calculate_regions_to_remove(region_path: str, regions_to_keep: 'list[str]') -> 'list[str]':
    """This function looks at all the region files and given which region files need to be kept, it lists which ones need to be removed."""
    all_files: list[str] = next(os.walk(region_path), (None, None, []))[2]
    deletion_files = []
    for file in all_files:
        if not file.endswith(".mca"):
            continue
        if not file in regions_to_keep:
            deletion_files.append(file)
    return deletion_files

def remove_regions(region_dir_path: str, regions_to_remove: 'list[str]'):
    for region_name in regions_to_remove:
        region_path = os.path.join(region_dir_path, region_name)
        os.remove(region_path)


# Run the program!
if __name__ == "__main__":
    # Disclaimers
    print("Running this tool could end up destroying your world. Make sure to backup before using this!")
    input("Press enter if you have made a backup. Otherwise, close out of this program.")
    print("\n"*5)

    # This script needs the path of 2 things: The Ledger sqlite database and the region directory of the Minecraft world. That's what the following code is for.
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
    
    # Now we can finally run the program!
    smart_chunk_remover(sql_path, region_path)