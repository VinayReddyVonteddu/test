'''This program verifies the symlinks in entrylists/nmrstar3.1 and if they are pointing .str files in /entry_directories/macromolecules/entry_id folder. 
If they are pointing to nothing, delete the symlink.  If there is no symlink for entry, create the symlink in the entry_lists.'''
from pathlib import Path
import shutil
import json
import os

import logging
logging.basicConfig(level=logging.INFO)

macromolecules = "/projects/BMRB/public/entry_directories/macromolecules/"
nmr_str = "/projects/BMRB/public/ftp/pub/bmrb/entry_lists/test_nmr_star"
# Iterate the symlinks in nmr-str3.1 to verify if they are valid or else delete them
for eid_file in os.listdir(nmr_str):
    eid = eid_file.replace(".str", "")
    #Join path for /entrylists/nmr-str3.1/entry_id.str file
    eid_path  = os.path.join(nmr_str, eid_file)
    #Join path for macromolecules/entry_id/entry_id_3.str file
    macro_path = os.path.join(macromolecules, eid, eid + "_3.str")
    #Assign original path to the macro_link
    macro_link = str(Path(eid_path).resolve())
    #Verify if the original path and symlink's path match and path exists
    if macro_link == macro_path and os.path.exists(macro_link):
        continue
    else: 
        logging.info('SYM LINK NOT FOUND %s -> %s ', eid_path, macro_link)
        #Delete symlink if the symlink is not found
        os.unlink(eid_path)
#Itearte the macromolecules directory to verify all str files have symlink's or else create symlink in /entrylists/nmr-str3.1
for eid in os.listdir(macromolecules):
    eid_dir = os.path.join(macromolecules, eid)
    #Join path for /entrylists/nmr-str3.1/entry_id.str file
    star_path = os.path.join(nmr_str, eid + ".str")
    #Join path for macromolecules/entry_id/entry_id_3.str file
    eid_path = os.path.join(eid_dir, eid + "_3.str")
    #Verify if the macromolecules/entry_id/entry_id_3.str exists
    if not os.path.isdir(eid_dir) or not os.path.exists(eid_path):
        continue
    #Verify if /entrylists/nmr-str3.1/entry_id.str exists 
    if os.path.exists(star_path):
        continue         
    else:
        #Create Symlink
        os.symlink(eid_path, star_path)
        logging.info("Symbolic link created successfully to %s", eid_path)
        logging.info("Checking symlink again %s - > %s", star_path, Path(star_path).resolve().as_uri())
