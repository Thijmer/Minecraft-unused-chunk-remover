# Unused chunk remover

A tool that allows you to remove the untouched regions in your world to make your world ready for the next Minecraft update or to optimize your survival world for uploading online.

**You need to have used the Ledger mod since the very beginning of your world! Otherwise your world will be destroyed. Make sure to backup!**  
**Because Ledger only works on servers and not in single player, this script does not work for single player worlds.**

## How it works
[Ledger](https://modrinth.com/mod/ledger) is a block logging tool developed by Quilt Server Tools (not me). It logs all changes to blocks to make it easier to track down grievers and rollback their damage. Because it logs everything, *this* program can use its logs to find out if someone has built (or destroyed) something in a region file and remove it if it hasn't been touched. This way, it can be regenerated the next time it is loaded, allowing Minecraft features from the latest version to generate.  
This script does not remove single chunks, but rather 512*512 block .mca files.

## How to use it
1. Make sure you have Python installed on your computer
2. Clone this repository
3. **Make sure to backup your world!**
4. Open a terminal and run the .py file
5. Supply the information the program asks for
6. Done!
