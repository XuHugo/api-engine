#
# SPDX-License-Identifier: Apache-2.0
#
import logging

from api.lib.agent.base import AgentBase
from api.lib.agent.kubernetes.common import KubernetesClient
from api.lib.agent.kubernetes.fabric import FabricNetwork
from api.utils.port_picker import set_ports_mapping


LOG = logging.getLogger(__name__)


class KubernetesAgent(AgentBase):
    def __init__(self, node=None):
        if node is None:
            node = {}
        config_file = node.get("k8s_config_file")
        self._project_name = node.get("name")
        self._network_type = node.get("network_type")
        self._network_version = node.get("network_version")
        self._node_type = node.get("type")
        self._node_id = node.get("id")
        self._agent_id = node.get("agent_id")

        self._client = KubernetesClient(config_file=config_file)
        self._network = FabricNetwork(
            version=self._network_version,
            node_type=self._node_type,
            agent_id=self._agent_id,
            node_id=self._node_id,
        )
        self._client.get_or_create_namespace(name=self._agent_id)
        self._config = self._network.generate_config()

    def create(self, *args, **kwargs):
        deployment = self._config.get("deployment")
        service = self._config.get("service")
        ingress = self._config.get("ingress")

        if deployment:
            self._client.create_deployment(self._agent_id, **deployment)
        if service:
            success, service_response = self._client.create_service(
                self._agent_id, **service
            )
            if service.get("service_type") == "NodePort" and success:
                ports = service_response.spec.ports
                ports = [
                    {"external": port.node_port, "internal": port.port}
                    for port in ports
                ]
                set_ports_mapping(self._node_id, ports, True)
        if ingress:
            self._client.create_ingress(self._agent_id, **ingress)

    def start(self, *args, **kwargs):
        pass

    def stop(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        deployment = self._config.get("deployment")
        service = self._config.get("service")
        ingress = self._config.get("ingress")

        if ingress:
            self._client.delete_ingress(
                namespace=self._agent_id, name=ingress.get("name")
            )
        if service:
            self._client.delete_service(
                namespace=self._agent_id, name=service.get("name")
            )
        if deployment:
            self._client.delete_deployment(
                namespace=self._agent_id, name=deployment.get("name")
            )

    def generate_config(self, *args, **kwargs):
        return self._config
