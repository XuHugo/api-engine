from subprocess import call
import os


class CryptoGen:

    def __init__(self, filepath="/opt/cello", cryptogen="/opt/bin/cryptogen", version="2.2.0"):
        self.cryptogen = cryptogen
        self.filepath = filepath
        self.version = version

    def generate(self, org_name, output="crypto-config", config="crypto-config.yaml"):
        try:
            call([self.cryptogen, "generate", "--output={}/{}/{}".format(self.filepath, org_name, output),
                  "--config={}/{}/{}".format(self.filepath, org_name, config)])
        except Exception as e:
            err_msg = "cryptogen generate fail! "
            raise Exception(err_msg+str(e))

    def showtemplate(self):
        pass

    def extend(self, org_name, input="crypto-config", config="./crypto-config.yaml"):
        try:
            call([self.cryptogen, "extend", "--input={}/{}/{}".format(self.filepath, org_name, input),
                  "--config={}/{}/{}".format(self.filepath, org_name, config)])
        except Exception as e:
            err_msg = "cryptogen extend fail! "
            raise Exception(err_msg+str(e))

    def version(self):
        pass

    def help(self):
        pass


if __name__ == "__main__":
    cryptogen = CryptoGen()
    cryptogen.generate(org_name="org1", output="crypto-config", config="crypto-config.yaml")
    #cryptogen.extend(org_name="org1", input="crypto-config", config="crypto-config.yaml")
