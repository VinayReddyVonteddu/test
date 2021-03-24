from pathlib import Path
import pynmrstar
import json
import os

metabolomics = "/projects/BMRB/public/entry_directories/metabolomics/"
for entryid in os.listdir(metabolomics):
    #Concatenate the path with entry ID(ex:bsme000xxxx)
    eid_path = metabolomics + entryid
    eid_file  = eid_path + "/" + entryid + ".str"
    if not os.path.isdir(eid_path) or not os.path.exists(eid_file):
        continue
    
    
    entry = pynmrstar.Entry.from_file(eid_file)

    files = entry.get_loops_by_category("_Experiment_file")
    for fl in files:
        dir_paths = fl.get_tag("Directory_path")
        file_paths = fl.get_tag("Name")

        data = json.loads(fl.get_json())
        nameIndex = data['tags'].index('Name')
        directoryIndex = data['tags'].index('Directory_path')

        for dir_path, file_path, dt in zip(dir_paths, file_paths, data['data']):
            path = eid_path + "/" + dir_path + file_path
            if os.path.exists(path) and os.path.islink(path):
                print ("SYM LINK FOUND ", path)
                path_link = Path(path).resolve()
                dir_link = path_link.parent.as_uri().split(entryid + "/")[1] + "/"
                print ("SYM LINK RESOLVED ", dir_link, path_link.name)
                dt[nameIndex] = path_link.name
                dt[directoryIndex] = dir_link
        fl.data = data['data']
        fl.validate()
    link_path = "./link_directories/" + entryid + "/"
    os.makedirs(link_path)
    entry.write_to_file(link_path + entryid + ".str")
