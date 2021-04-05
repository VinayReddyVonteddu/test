'''This program verifies the symlinks in entrylists/timedomain_entries and if they are pointing .str files in /entry_directories/macromolecules/ folder. 
If they are pointing to nothing, delete the symlink.  If there is no symlink for entry, create the symlink in the entry_lists.'''
from pathlib import Path
import json
import os
import logging
logging.basicConfig(level=logging.INFO)

macromolecules = "/projects/BMRB/public/entry_directories/macromolecules"
time_domain_entries = "/projects/BMRB/public/ftp/pub/bmrb/entry_lists/test_td_entries"
# Iterate the symlinks in timedomain_entries to verify if they are valid or else delete them
for eid in os.listdir(time_domain_entries):
    #Join path for /entrylists/timedomain_entries/entry_id
    eid_path  = os.path.join(time_domain_entries, eid)
    #Join path for macromolecules/entry_id
    macro_path = os.path.join(macromolecules, eid)
    macro_time_domain = os.path.join(macro_path, "timedomain_data")
    #Assign original path to the macro_link
    macro_link = str(Path(eid_path).resolve())
    #Verify if the original path and symlink's path match and path exists
    if macro_link == macro_path and os.path.exists(macro_link):
        continue
    else: 
        logging.info('SYM LINK NOT FOUND %s -> %s ', eid_path, macro_link)
        #Delete symlink if the symlink is not found
        os.unlink(eid_path)
#Itearte the macromolecules directory to verify all str files have symlink's or else create symlink in /entrylists/timedomain_entries
for eid in os.listdir(macromolecules):
    eid_dir = os.path.join(macromolecules, eid)
    time_domain_path = os.path.join(time_domain_entries, eid)
    macro_time_domain = os.path.join(eid_dir, "timedomain_data")
    if not os.path.isdir(eid_dir) or not os.path.exists(macro_time_domain):
        continue
    if os.path.exists(time_domain_path):
        continue         
    else:
        #Create Symlink
        os.symlink(eid_dir, time_domain_path)
        logging.info("Symbolic link created successfully to %s", eid_dir)
        logging.info("Checking symlink again %s - > %s", time_domain_path, str(Path(time_domain_path).resolve()))
