from subprocess import call


class ConfigTxGen:

    def __init__(self, network, filepath="/opt/cello", configtxgen="/opt/bin/configtxgen", version="2.2.0"):
        self.network = network
        self.configtxgen = configtxgen
        self.filepath = filepath
        self.version = version

    def genesis(self, profile="TwoOrgsOrdererGenesis", channelid="testchainid", outputblock="genesis.block"):
        try:
            call([self.configtxgen, "-configPath", "{}/{}/".format(self.filepath, self.network),
                  "-profile", "{}".format(profile),
                  "-outputBlock", "{}/{}/{}".format(self.filepath, self.network, outputblock),
                  "-channelID", "{}".format(channelid)])
        except Exception as e:
            err_msg = "configtxgen genesis fail! "
            raise Exception(err_msg + str(e))

    def channeltx(self, profile, channelid, outputblock):
        pass

    def anchorpeer(self, profile, channelid, outputblock):
        pass


if __name__ == "__main__":
    ConfigTxGen("test").genesis()

