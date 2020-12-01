import yaml
import os


class CryptoConfig:
    def __init__(self, org, filepath="/opt/cello"):
        self.filepath = filepath
        self.org = org

    def create(self, org_info: any) -> None:

        org = []
        ca = dict(Country=org_info['ca']['country'],
                  Locality=org_info['ca']['locality'],
                  Province=org_info['ca']['province'])

        specs = []
        for host in org_info["Specs"]:
            specs.append(dict(Hostname=host))
        org.append(dict(Domain=org_info['domain'],
                        Name=org_info['name'],
                        CA=ca,
                        Specs=specs,
                        EnableNodeOUs=org_info['enableNodeOUs']))

        if org_info["type"] == "peer":
            network = dict(PeerOrgs=org)
        else:
            network = dict(OrdererOrgs=org)

        os.system('mkdir -p {}/{}'.format(self.filepath, self.org))

        with open('{}/{}/crypto-config.yaml'.format(self.filepath, self.org), 'w', encoding='utf-8') as f:
            yaml.dump(network, f)

    def update(self, org_info: any) -> None:
        with open('{}/crypto-config.yaml'.format(self.filepath), 'r+', encoding='utf-8') as f:
            network = yaml.load(f)
            if org_info["type"] == "peer":
                orgs = network['PeerOrgs']
            else:
                orgs = network['OrdererOrgs']

            for org in orgs:
                if org["Name"] == org_info["name"]:
                    specs = org["Specs"]
                    for host in org_info["Specs"]:
                        specs.append(dict(Hostname=host))

        with open('{}/crypto-config.yaml'.format(self.filepath), 'w', encoding='utf-8') as f:
            yaml.dump(network, f)

    def delete(self):
        pass

    def get(self):
        pass


if __name__ == "__main__":
    cryptoconfig = CryptoConfig(org="org1")
    org = {"ca": {
        "country": "china",
        "province": "beijing",
        "locality": "changping"
    },
        "type": "peer",
        "name": "org1",
        "domain": "org1.h3c.com",
        "enableNodeOUs": True,
        "Specs": ["foo", "bar", "baz"]
    }
    cryptoconfig.create(org)
    # org = {
    #     "type": "peer",
    #     "name": "org1",
    #     "Specs": ["foo2", "bar2", "baz2"]
    # }
    # cryptoconfig.update(org)
