from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
import json
import uuid

from common.ret_status import RetStatus
from common.database import db, basic_opt
from common.satree import TreeManager
from model.nodetree import NodeTree
from model.nodemsg import NodeMsg, OutMsgSchema

class NodeMsgEdit(db.Model, basic_opt):
    @jwt_required()
    def get(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        node = tm.find_node(node_uuid=node_uuid)
        if node.check() is False:
            return node.dumps_json()
        node.data = OutMsgSchema().dump(node.data.msgs).data
        return node.dumps_json()

    @jwt_required()
    def post(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        node = tm.find_node(node_uuid=node_uuid)
        if node.check() is False:
            return node.dumps_json()
        req_json = json.dumps(request.get_json())
        load_data, error = NodeMsgEdit(exclude=('uuid')).loads(req_json)
        if error:
            return RetStatus(False, "parse request data failed.")
        new_msg = NodeMsg(load_data['title'], load_data['msg'], nodes=[node,])
        add_ret = NodeMsg.ADD(new_msg)
        if add_ret.check() is False:
            return add_ret.dumps_json()
        return RetStatus(True, "add success.")

    @jwt_required()
    def put(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        node = tm.check(node_uuid=node_uuid)
        if node.check() is False:
            return node.dumps_json()
        if node.data is False:
            return RetStatus(False, "invalid node uuid.")
        req_json = json.dumps(request.get_json())
        load_data, error = OutMsgSchema().loads(req_json)
        node.data.msgs['title'] = load_data['title']
        node.data.msgs['msg']   = load_data['msg']
        update_ret = NodeMsg.UPDATE()
        if update_ret.check() is False:
            return update_ret.dumps_json()
        return RetStatus(True, "update success.")

    @jwt_required()
    def delete(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        node = tm.find_node(node_uuid=node_uuid)
        if node.check() is False:
            return node.dumps_json()
        if node.data is None:
            return RetStatus(False, "nothing will be delete.")
        delete_ret = NodeMsg.DEL(node.data.msgs)
        if delete_ret.check() is False:
            return delete_ret.dumps_json()
        return RetStatus(True, "delete success.")
