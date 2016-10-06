import os
import glob
import hashlib
import datetime

import staticjinja


# TODO
# - Add torrent file generation
# - Add argument inline for generation
# - Auto fetch from GitHub releases


def humand_readable_bytes(num):
    for x in ['bytes', 'KiB', 'MiB', 'GiB', 'TiB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def files_parser(files_directory, file_extension):
    """ Return a sorted by date list of tuple(filename, size, modified_date, md5_hash)"""
    file_list_info = []
    file_list = [fn for fn in glob.glob(os.path.join(files_directory, "*" + file_extension))
                 if os.path.isfile(fn)]
    for file_path in file_list:
        with open(file_path) as file_to_check:
            data = file_to_check.read()
            md5 = hashlib.md5(data).hexdigest()
            last_modified = datetime.datetime.fromtimestamp(
                os.path.getmtime(file_path))
        size = humand_readable_bytes(os.path.getsize(file_path))

        file_list_info.append((os.path.basename(
            file_path), size, last_modified, md5))
    sorted_files_info = sorted(
        file_list_info, key=lambda t: t[1], reverse=True)
    titles = ["Filename", "Size", "Last Modified", "MD5"]
    return (titles, sorted_files_info)
    
if __name__ == "__main__":

    contexts = {'file_list': files_parser(
        'iso', '*'), 'site_name': 'Poppy dowloads archive'}
    site = staticjinja.make_site(contexts=[('.*.html', contexts)])
    site.render()
