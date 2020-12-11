from subprocess import call
from api.config import CELLO_HOME,FABRIC_TOOL


class CryptoGen:

    def __init__(self, name, filepath=CELLO_HOME, cryptogen=FABRIC_TOOL, version="2.2.0"):
        self.cryptogen = cryptogen + "/cryptogen"
        self.filepath = filepath
        self.version = version
        self.name = name

    def generate(self, output="crypto-config", config="crypto-config.yaml"):
        try:
            call([self.cryptogen, "generate", "--output={}/{}/{}".format(self.filepath, self.name, output),
                  "--config={}/{}/{}".format(self.filepath, self.name, config)])
        except Exception as e:
            err_msg = "cryptogen generate fail for {}!".format(e)
            raise err_msg

    def extend(self, input="crypto-config", config="./crypto-config.yaml"):
        try:
            call([self.cryptogen, "extend", "--input={}/{}/{}".format(self.filepath, self.name, input),
                  "--config={}/{}/{}".format(self.filepath, self.name, config)])
        except Exception as e:
            err_msg = "cryptogen extend fail for {}!".format(e)
            raise err_msg

    def version(self):
        pass

    def help(self):
        pass

    def showtemplate(self):
        pass


if __name__ == "__main__":
    cryptogen = CryptoGen("org.cello.com")
    #cryptogen.generate()
    cryptogen.extend()
