import os
import json
import hashlib
from hurry.filesize import size

path = "/media/alex_newman/Sony_16GB"


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


raw_data = {}

for parent_directory, child_directories, files in os.walk(path):

    for file in files:
        file_path = os.path.join(parent_directory, file)
        print("Processing: {}".format(file_path))

        file_size = os.path.getsize(file_path)
        file_hash = md5(file_path)
        file_hash += ':' + str(file_size)

        values = raw_data.get(file_hash, [])
        values.append(file_path)
        raw_data[file_hash] = values


filtered_data = {}
freed = 0

for key, values in raw_data.items():
    if len(values) == 1:
        continue

    filtered_data.update({key: values})
    freed += int(key.split(":")[-1])*(len(values)-1)

text = json.dumps(filtered_data, separators=(',', ':'), sort_keys=True, indent=4)
print(text)
print("Potential space can be freed: {}".format(size(freed)))
