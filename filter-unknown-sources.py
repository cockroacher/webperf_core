# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import json
import os

def main(_):
    """
    WebPerf Core - Software update
    """

    collection = get_software_sources('software-unknown-sources.json')
    known_collection = get_software_sources('software-sources.json')

    names_to_remove = []
    for key in collection.keys():
        item = collection[key]

        if len(key) < 3:
            names_to_remove.append(key)
            continue

        if 'versions' not in item:
            names_to_remove.append(key)
            continue

        versions = item['versions']
        if 'unknown' in versions:
            del versions['unknown']

        if 'aliases' in known_collection and key in known_collection['aliases']:
            names_to_remove.append(key)

        if 'softwares' in known_collection and key in known_collection['softwares']:
            names_to_remove.append(key)

        # Change the below number to filter out how many versions should be minimum
        if len(item['versions'].keys()) < 2:
            names_to_remove.append(key)
            continue

    for key in names_to_remove:
        print(f'\t- {key}')
        if key in collection:
            del collection[key]

    set_softwares('software-unknown-sources-filtered.json', collection)


def set_softwares(filename, collection):
    base_directory = Path(os.path.dirname(
        os.path.realpath(__file__)) + os.path.sep)

    file_path = f'{base_directory}{os.path.sep}data{os.path.sep}{filename}'
    if not os.path.isfile(file_path):
        file_path = f'{base_directory}{os.path.sep}{filename}'
    if not os.path.isfile(file_path):
        print(f"ERROR: No {filename} file found!")

    print('set_software_sources', file_path)

    data = json.dumps(collection, indent=4)
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        file.write(data)

def get_software_sources(filename):
    base_directory = Path(os.path.dirname(
        os.path.realpath(__file__)) + os.path.sep)

    file_path = f'{base_directory}{os.path.sep}data{os.path.sep}{filename}'
    if not os.path.isfile(file_path):
        file_path = f'{base_directory}{os.path.sep}{filename}'
    if not os.path.isfile(file_path):
        print(f"ERROR: No {filename} file found!")
        return {
        }

    print('get_software_sources', file_path)
    collection = {}
    with open(file_path, encoding='utf-8') as json_file:
        collection = json.load(json_file)

    # sort on software names
    if len(collection.keys())> 0:
        tmp = {}
        issue_keys = list(collection.keys())
        issue_keys_sorted = sorted(issue_keys, reverse=False)

        for key in issue_keys_sorted:
            tmp[key] = collection[key]

        collection = tmp

    return collection


"""
If file is executed on itself then call a definition, mostly for testing purposes
"""
if __name__ == '__main__':
    main(sys.argv[1:])
