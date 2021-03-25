"""
Purpose: Read, modify and write the STR files using the PYNMRSTAR utility to replace the symlink's in _experiment_file loop
"""

import logging
import os
from pathlib import Path

import pynmrstar

logging.basicConfig(level=logging.INFO)

metabolomics = "/projects/BMRB/public/entry_directories/metabolomics/"
for entryid in os.listdir(metabolomics):
    # Concatenate the path with entry ID(ex:bsme000xxxx)
    eid_path = os.path.join(metabolomics, entryid)
    eid_file = os.path.join(eid_path, entryid + ".str")
    # Verify if the path exists
    if not os.path.isdir(eid_path) or not os.path.exists(eid_file):
        continue

    entry = pynmrstar.Entry.from_file(eid_file)

    files = entry.get_loops_by_category("_Experiment_file")
    # Read the experiment file from the entries
    for fl in files:
        nameIndex = fl.tag_index("Name")
        directoryIndex = fl.tag_index("Directory_path")

        for dt in fl.data:
            dir_path = dt[directoryIndex]
            file_path = dt[nameIndex]
            path = os.path.join(eid_path, dir_path, file_path)
            # Assign the original link to path_link
            path_link = Path(path).resolve()
            path_link_uri = path_link.as_uri().replace("file://", "")
            # condition to check if path is symlink
            if path_link_uri != path:
                logging.info("SYM LINK FOUND %s - > %s ", path, path_link_uri)
                # Assign the parent of the path_link to the dir_link as URI which is after /entry id/ 
                dir_link = path_link.parent.as_uri().split(entryid + "/")[1] + "/"
                logging.info("SYM LINK RESOLVED %s, %s", dir_link, path_link.name)
                # Assign name and directory path
                dt[nameIndex] = path_link.name
                dt[directoryIndex] = dir_link
        fl.validate()
    link_path = "./link_directories/" + entryid + "/"
    os.makedirs(link_path)
    entry.write_to_file(link_path + entryid + ".str")
