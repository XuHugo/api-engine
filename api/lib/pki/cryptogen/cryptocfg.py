import yaml
import os
from api.config import CELLO_HOME


class CryptoConfig:
    def __init__(self, name, file="crypto-config.yaml", country="CN", locality="BJ", province="CP", enablenodeous=True, filepath=CELLO_HOME):
        self.filepath = filepath
        self.name = name
        self.country = country
        self.locality = locality
        self.province = province
        self.enablenodeous = enablenodeous
        self.file = file

    def create(self) -> None:
        try:
            network = {}
            for item in ["Peer", "Orderer"]:
                org = []
                ca = dict(Country=self.country,
                          Locality=self.locality,
                          Province=self.province)
                specs = []
                # for host in org_info["Specs"]:
                #     specs.append(dict(Hostname=host))
                if item == "Peer":
                    org.append(dict(Domain=self.name,
                                    Name=self.name.split(".")[0].capitalize(),
                                    CA=ca,
                                    Specs=specs,
                                    EnableNodeOUs=self.enablenodeous))
                    network = {'PeerOrgs': org}
                else:
                    org.append(dict(Domain=self.name.split(".", 1)[1],
                                    Name=self.name.split(".")[0].capitalize() + item,
                                    CA=ca,
                                    Specs=specs,
                                    EnableNodeOUs=self.enablenodeous))
                    network['OrdererOrgs'] = org

            os.system('mkdir -p {}/{}'.format(self.filepath, self.name))

            with open('{}/{}/{}'.format(self.filepath, self.name, self.file), 'w', encoding='utf-8') as f:
                yaml.dump(network, f)
        except Exception as e:
            err_msg = "CryptoConfig create failed for {}!".format(e)
            raise Exception(err_msg)

    def update(self, org_info: any) -> None:
        try:
            with open('{}/{}/{}'.format(self.filepath, self.name, self.file), 'r+', encoding='utf-8') as f:
                network = yaml.load(f, Loader=yaml.FullLoader)
                if org_info["type"] == "peer":
                    orgs = network['PeerOrgs']
                else:
                    orgs = network['OrdererOrgs']

                for org in orgs:
                    specs = org["Specs"]
                    for host in org_info["Specs"]:
                        specs.append(dict(Hostname=host))

            with open('{}/{}/{}'.format(self.filepath, self.name, self.file), 'w', encoding='utf-8') as f:
                yaml.dump(network, f)
        except Exception as e:
            err_msg = "CryptoConfig update failed for {}!".format(e)
            raise Exception(err_msg)

    def delete(self):
        try:
            os.system('rm -rf {}/{}'.format(self.filepath, self.name))
        except Exception as e:
            err_msg = "CryptoConfig delete failed for {}!".format(e)
            raise Exception(err_msg)


if __name__ == "__main__":
    cryptoconfig = CryptoConfig("org.cello.com")
    #cryptoconfig.create()
    org = {
        "type": "peer",
        "Specs": ["foo2", "bar2", "baz2"]
    }
    cryptoconfig.update(org)
    # cryptoconfig.delete()
