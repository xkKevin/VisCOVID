import hashlib
from utils import load_config
import os


def check_two_paths(path1, path2):
    with open(path1, 'rb') as file1 , open(path2, "rb") as file2:
        buf1 = file1.read()
        buf2 = file2.read()
        hasher1 = hashlib.md5()
        hasher2 = hashlib.md5()
        hasher1.update(buf1)
        hasher2.update(buf2)
        print(hasher1.hexdigest()==hasher2.hexdigest())



def check_export(config):
    export_path = config['export']['root']
    archived_path = config['export']['archived']
    export_files = os.listdir(export_path)
    archived_files = os.listdir(archived_path)
    print(export_files)
    print(archived_files)
    export_len = len(export_files)
    a = list(range(export_len))
    list(map(lambda i: check_two_paths(export_path + export_files[i], archived_path + archived_files[i]), list(range(export_len))))


if __name__ == "__main__":
    config = load_config()
    check_export(config)