import os
import yaml
import socket
import time


def load_config(config_folder='../config') -> dict:
    os.chdir('src')
    environments = ['dev', 'acc', 'prod']
    curr_environment = os.getenv('environment', 'dev')
    files_in_folder = os.listdir(config_folder)
    config_dict: Dict = dict()
    for file in files_in_folder:
        print(file)
        if os.path.splitext(file)[1].lower() == '.yaml' and 'TEMPLATE' not in file:
            full_filename = os.path.join(os.path.normpath(config_folder), os.path.normpath(file))
            file_content = yaml.safe_load(open(full_filename, 'r'))
            shadow_file_content = file_content.copy()
            for key in file_content.keys():
                if key in environments:
                    if key == curr_environment:
                        merge(shadow_file_content, shadow_file_content[key])
                    del shadow_file_content[key]
                if key in config_dict.keys():
                    raise ValueError(f"Duplicate config key names found for key '{key}'!")
            config_dict.update(shadow_file_content)
    return config_dict

def merge(a, b, path=None):
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                a.update(b)
        else:
            a[key] = b[key]
    return a