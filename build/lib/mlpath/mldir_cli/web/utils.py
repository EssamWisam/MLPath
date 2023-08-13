import os


def get_json_paths(dir_path):
    json_paths = {}
    for root, dirs, files in os.walk(dir_path):
        root_basename = os.path.basename(root)
        if root_basename == 'Quests':
            for dir in dirs:
                json_paths[dir] = {}
        elif root_basename == 'json':
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    grandparent = os.path.basename(os.path.dirname(os.path.dirname(root)))
                    parent = os.path.basename(os.path.dirname(root))
                    file_full_path = os.path.join(root, file)
                    if '-config.json' in file:
                        json_paths[grandparent][parent]['config'] = file_full_path
                    else:
                        json_paths[grandparent][parent]['data'] = file_full_path
        else:
            for dir in dirs:
                if dir != 'json':
                    json_paths[root_basename][dir] = {}
    
    return json_paths