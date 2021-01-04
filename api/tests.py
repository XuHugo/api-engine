from django.test import TestCase

# Create your tests here.
from zipfile import ZipFile
import os


def zipDir(dirpath,outFullName):
    """
    Compress the specified folder
    :param dirpath: specified folder
    :param outFullName: Save path+xxxx.zip
    :return: null
    """
    dir_dst = "/" + dirpath.rsplit("/", 1)[1]
    zip = ZipFile(outFullName, "w")
    for path,dirnames,filenames in os.walk(dirpath):
        fpath = dir_dst + path.replace(dirpath, '')
        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()
f1 = "/opt/cello/org.cello.com/crypto-config/peerOrganizations/org.cello.com/peers/peer1.org.cello.com/msp"
if __name__ == "__main__":
    # f = ZipFile("/opt/msp.zip", "w")
    # f.write()
    # f.close()

    zipDir(f1,"/opt/test/msp.zip")
