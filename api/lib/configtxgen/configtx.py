import yaml
import os
from api.config import CELLO_HOME


class ConfigTX:
    def __init__(self, network, filepath=CELLO_HOME):
        self.filepath = filepath
        self.network = network
        self.orderer = {'BatchTimeout':'2s','OrdererType':"etcdraft",
                        'BatchSize':{'AbsoluteMaxBytes':'98 MB','MaxMessageCount':2000,'PreferredMaxBytes':'10 MB'}}
        self.raft_option = {'TickInterval':"600ms",'ElectionTick':10,'HeartbeatTick':1, 'MaxInflightBlocks':5,'SnapshotIntervalSize':"20 MB"}

    def create(self, consensus, orderers, peers, orderer_cfg=None, application=None, option=None):

        OrdererOrganizations = []
        OrdererAddress = []
        for orderer in orderers:
            OrdererOrganizations.append(dict(Name=orderer["name"].split(".")[0].capitalize(),
                                             ID='{}MSP'.format(orderer["name"].split(".")[0].capitalize()),
                                             MSPDir='{}/{}/crypto-config/ordererOrganizations/{}/msp'.format(self.filepath,self.network,orderer['name']),
                                             Policies=dict(Readers=dict(Type="Signature",Rule="OR('{}MSP.member')".format(orderer["name"].split(".")[0].capitalize())),
                                                           Writers=dict(Type="Signature",Rule="OR('{}MSP.member')".format(orderer["name"].split(".")[0].capitalize())),
                                                           Admins=dict(Type="Signature",Rule="OR('{}MSP.admin')".format(orderer["name"].split(".")[0].capitalize())))
                                             ))
            for host in orderer['hosts']:
                OrdererAddress.append('{}.{}:{}'.format(host['name'], orderer['name'], host["port"]))

        PeerOrganizations = []
        for peer in peers:
            PeerOrganizations.append(dict(Name=peer["name"].split(".")[0].capitalize(),
                                          ID='{}MSP'.format(peer["name"].split(".")[0].capitalize()),
                                          MSPDir='{}/{}/crypto-config/peerOrganizations/{}/msp'.format(self.filepath,peer['name'],peer['name']),
                                          AnchorPeers=[{'Port': peer["hosts"][0]["port"], 'Host': '{}.{}'.format(peer["hosts"][0]["name"],peer["name"])}],
                                          Policies=dict(Readers=dict(Type="Signature",Rule="OR('{}MSP.peer', '{}MSP.admin','{}MSP.client')".format(peer["name"].split(".")[0].capitalize(),peer["name"].split(".")[0].capitalize(),peer["name"].split(".")[0].capitalize())),
                                                        Writers=dict(Type="Signature",Rule="OR('{}MSP.admin','{}MSP.client')".format(peer["name"].split(".")[0].capitalize(),peer["name"].split(".")[0].capitalize())),
                                                        Admins=dict(Type="Signature",Rule="OR('{}MSP.admin')".format(peer["name"].split(".")[0].capitalize())))
                                          ))
        Organizations = OrdererOrganizations + PeerOrganizations

        Orderer = {'BatchTimeout': orderer_cfg['BatchTimeout'] if orderer_cfg else self.orderer['BatchTimeout'],
                       'Organizations': None,
                       'Addresses': OrdererAddress,
                       'OrdererType': consensus if consensus else self.orderer['OrdererType'],
                       'BatchSize': orderer_cfg['BatchSize'] if orderer_cfg else self.orderer['BatchSize']
                       }

        channel = {"Policies": dict(Readers=dict(Type="ImplicitMeta", Rule="ANY Readers"),
                                    Writers=dict(Type="ImplicitMeta", Rule="ANY Writers"),
                                    Admins=dict(Type="ImplicitMeta", Rule="MAJORITY Admins"))
                   }


        if consensus == 'etcdraft':
            Consenters = []
            for orderer in orderers:
                for host in orderer['hosts']:
                    Consenters.append(dict(Host='{}.{}'.format(host['name'], orderer['name']),
                                           Port=host['port'],
                                           ClientTLSCert='{}/{}/crypto-config/ordererOrganizations/{}/orderers/{}.{}/tls/server.crt'
                                           .format(self.filepath,orderer['name'], orderer['name'],host['name'], orderer['name']),
                                           ServerTLSCert='{}/{}/crypto-config/ordererOrganizations/{}/orderers/{}.{}/tls/server.crt'
                                           .format(self.filepath,orderer['name'],orderer['name'], host['name'], orderer['name'])))
            Option = option if option else self.raft_option
            Orderer['EtcdRaft'] = dict(Consenters=Consenters,Options=Option)
            Orderer["Policies"] = dict(Readers=dict(Type="ImplicitMeta",Rule="ANY Readers"),
                                       Writers=dict(Type="ImplicitMeta",Rule="ANY Writers"),
                                       Admins=dict(Type="ImplicitMeta",Rule="MAJORITY Admins"),
                                       BlockValidation=dict(Type="ImplicitMeta",Rule="MAJORITY Writers"))
            #Profiles['TwoOrgsOrdererGenesis']['Orderer']['EtcdRaft'] = dict(Consenters=Consenters, Options=Option)

        Application = application if application else {'Organizations': None,
                                                       "Policies":dict(Readers=dict(Type="ImplicitMeta",Rule="ANY Readers"),
                                                                       Writers=dict(Type="ImplicitMeta",Rule="ANY Writers"),
                                                                       Admins=dict(Type="ImplicitMeta",Rule="MAJORITY Admins"))
        }
        Profiles = {'TwoOrgsOrdererGenesis': {
            # 'Orderer': {'BatchTimeout': orderer_cfg['BatchTimeout'] if orderer_cfg else self.orderer['BatchTimeout'],
            #             'Organizations': OrdererOrganizations,
            #             'Addresses': OrdererAddress,
            #             'OrdererType': consensus if consensus else self.orderer['OrdererType'],
            #             'BatchSize': orderer_cfg['BatchSize'] if orderer_cfg else self.orderer['BatchSize']
            #             },
            "Orderer":Orderer,
            'Consortiums': {'SampleConsortium': {'Organizations': PeerOrganizations}},
            "Policies": dict(Readers=dict(Type="ImplicitMeta", Rule="ANY Readers"),
                             Writers=dict(Type="ImplicitMeta", Rule="ANY Writers"),
                             Admins=dict(Type="ImplicitMeta", Rule="MAJORITY Admins"))
        }}

        configtx = dict(Application=Application, Orderer=Orderer, Profiles=Profiles, Organizations=Organizations, Channel=channel)
        os.system('mkdir -p {}/{}'.format(self.filepath, self.network))

        with open('{}/{}/configtx.yaml'.format(self.filepath, self.network), 'w', encoding='utf-8') as f:
            yaml.dump(configtx, f)

    def update(self):
        pass


if __name__ == "__main__":
    orderers=[{"name":"orderer.cello.com","hosts":[{"name": "zoo", "port":8051}]}]
    #peers = [{"name": "org1.cello.com", "hosts": [{"name": "foo", "port": 7051},{"name": "car", "port": 7052}]},
    #         {"name": "org2.cello.com", "hosts": [{"name": "zoo", "port": 7053}]}]
    peers = [{"name": "org1.cello.com", "hosts": [{"name": "foo", "port": 7051}, {"name": "car", "port": 7052}]}]
    ConfigTX("test").create(consensus="etcdraft", orderers=orderers, peers=peers)
