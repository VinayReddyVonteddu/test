"""
Purpose: Read, modify and write the STR files using the PYNMRSTAR utility to replace the NMR_spec_expt_ID and
NMR_spec_expt_label to "." in _experiment_file loop when Raw_data_flag is no
"""
import logging
import os
from pathlib import Path
import pynmrstar
logging.basicConfig(level=logging.INFO)

bmrb = "/projects/BMRB/public/ftp/pub/bmrb/entry_directories/"
for entryid in os.listdir(bmrb):
    # Concatenate the path with entry ID(ex:bsme000xxxx)
    eid_path = os.path.join(bmrb, entryid)
    eid_file = os.path.join(eid_path, entryid + "_3.str")
    # Verify if the path exists
    if not os.path.isdir(eid_path) or not os.path.exists(eid_file):
        continue

    entry = pynmrstar.Entry.from_file(eid_file)
    files = entry.get_loops_by_category("_Experiment")
    # Read the experiment file from the entries
    for fl in files:
        rawDataIndex = fl.tag_index("Raw_data_flag")
        exptIdIndex = fl.tag_index("NMR_spec_expt_ID")
        exptLabelIndex = fl.tag_index("NMR_spec_expt_label")

        for dt in fl.data:
            if dt[rawDataIndex] == "no" and (dt[exptIdIndex] != "." or dt[exptLabelIndex] != "."):
                logging.info("Entry Id %s", entryid)
                logging.info("Incorrect Data Raw_data_flag -> %s, expt_ID -> %s, expt_label -> %s ", dt[rawDataIndex], dt[exptIdIndex], dt[exptLabelIndex])
                #Passing None object to exptIdIndex and ExpetLabelindex, they get converted to "." using Pynmrstar utility
                dt[exptIdIndex] = None
                dt[exptLabelIndex] = None
                logging.info("correct Data Raw_data_flag -> %s, expt_ID -> %s, expt_label -> %s ", dt[rawDataIndex], dt[exptIdIndex], dt[exptLabelIndex])
        fl.validate()
    link_path = os.path.join("./temp_directories", entryid)
    os.makedirs(link_path)
    entry.write_to_file(os.path.join(link_path, entryid + "_3.str"))
