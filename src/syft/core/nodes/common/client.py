from ...message.syft_message import SyftMessageWithReply
from ...message.syft_message import SyftMessageWithoutReply
from ....decorators import syft_decorator
from ....common.id import UID
from ...io.connection import ClientConnection
from ...io.address import Address
from ...io.address import address as create_address
from ..abstract.node import AbstractNodeClient
from .location_aware_object import LocationAwareObject
from .service.child_node_lifecycle_service import RegisterChildNodeMessage
from ...io.route import Route
from typing import List

class Client(AbstractNodeClient, LocationAwareObject):
    """Client is an incredibly powerful abstraction in Syft. We assume that,
    no matter where a client is, it can figure out how to communicate with
    the Node it is supposed to point to. If I send you a client I have
    with all of the metadata in it, you should have all the information
    you need to know to interact with a node (although you might not
    have permissions - clients should not store private keys)."""


    @syft_decorator(typechecking=True)
    def __init__(self, address: Address, name: str, routes: List[Route]):
        LocationAwareObject.__init__(self, address=address)

        self.name = name
        self.routes = routes

    def add_me_to_my_address(self):
        raise NotImplementedError

    @syft_decorator(typechecking=True)
    def register(self, client: AbstractNodeClient) -> None:
        msg = RegisterChildNodeMessage(child_node_client=client, address=self.address)
        self.send_msg_without_reply(msg=msg)

    @property
    def target_node_id(self) -> UID:
        """This client points to an node, this returns the id of that node."""
        raise NotImplementedError

    @target_node_id.setter
    def target_node_id(self, new_target_node_id: UID) -> UID:
        """This client points to an node, this saves the id of that node"""
        raise NotImplementedError

    @syft_decorator(typechecking=True)
    def send_msg_with_reply(self, msg: SyftMessageWithReply) -> SyftMessageWithoutReply:
        return self.routes[0].send_msg_with_reply(msg=msg)

    @syft_decorator(typechecking=True)
    def send_msg_without_reply(self, msg: SyftMessageWithoutReply) -> None:
        return self.routes[0].send_msg_without_reply(msg=msg)

    @syft_decorator(typechecking=True)
    def __repr__(self) -> str:
        return f"<Client pointing to node with id:{self.node_id}>"