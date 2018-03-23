from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
import json
import uuid

from common.ret_status import RetStatus
from common.database import db
from common.satree import TreeManager
from model.nodetree import NodeTree
from model.nodeinfo import NodeInfo, OutInfoSchema

class NodeInfoEdit(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        node = tm.find_node(node_uuid=node_uuid)
        if node.check() is False:
            return node.dumps_json()
        node.data = OutInfoSchema().dump(node.data).data
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
        load_data, error = OutInfoSchema(exclude=('uuid')).loads(req_json)
        if error:
            return RetStatus(False, "parse request data failed.")
        node_info = NodeInfo(uuid=uuid.uuid1(), age=load_data['age'], sex=load_data['sex'], campus_id=load_data['campus_id'], nodes=[node,])
        add_ret = NodeInfo.ADD(node_info)
        if add_ret.check() is False:
            return add_ret.dumps_json()
        return RetStatus(True, "add success")

    @jwt_required()
    def put(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        node = tm.find_node(node_uuid)
        if node.check() is False:
            return node.dumps_json()
        req_json = json.dumps(request.get_json())
        load_data, error = OutInfoSchema().loads(req_json)
        if error:
            return RetStatus(False, "parse request data failed.")
        node.data.msg['age']        = load_data['age']
        node.data.msg['sex']        = load_data['sex']
        node.data.msg['campus_id'] = load_data['campus_id']
        update_ret = NodeInfo.UPDATE()
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
        if node.data.infos is None:
            return RetStatus(False, "nothing will be deleted.")
        del_ret = NodeInfo.DEL(node.data.infos)
        if del_ret.check() is False:
            return del_ret.dumps_json()
        return RetStatus(True, "delete success.")
