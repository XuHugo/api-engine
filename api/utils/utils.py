#
# SPDX-License-Identifier: Apache-2.0
#
from zipfile import ZipFile
import os


def zipDir(dirpath, outFullName):
    """
    Compress the specified folder
    :param dirpath: specified folder
    :param outFullName: Save path+xxxx.zip
    :return: null
    """
    dir_dst = "/" + dirpath.rsplit("/", 1)[1]
    zip = ZipFile(outFullName, "w")
    for path, dirnames, filenames in os.walk(dirpath):
        fpath = dir_dst + path.replace(dirpath, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()

