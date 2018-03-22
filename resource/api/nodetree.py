from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
import json
import uuid

from common.ret_status import RetStatus
from common.database import db
from common.satree import TreeManager
from model.nodetree import NodeTree, ReqNodeSchema, RspNodeSchema

class TreeRoot(Resource):
    @jwt_required()
    def get(self):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        ret = tm.get_root_node(many=True)
        if ret.check() is False:
            return ret.dumps_json()
        else:
            ret.data = RspNodeSchema(many=True).dump(ret.data).data
            return ret.dumps_json()

class TreeList(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        ret = tm.find_node(node_uuid=node_uuid, many=True)
        if ret.check() is False:
            return ret.dumps_json()
        else:
            ret.data = RspNodeSchema(many=True).dump(ret.data).data
            return ret.dumps_json()

class TreeEdit(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        ret = tm.find_node(node_uuid=node_uuid)
        if ret.check() is False:
            return ret.dumps_json()
        else:
            ret.data = RspNodeSchema().dump(ret.data).data
            return ret.dumps_json()
    @jwt_required()
    def post(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        req_json = json.dumps(request.get_json())
        load_data, error = ReqNodeSchema().loads(req_json)
        if error:
            return RetStatus(False, "parse request data failed.")
        new_node = NodeTree(title=load_data['title'], is_student=load_data['is_student'], identity_coding=load_data['identity_coding'])
        ret = tm.add_node(node_uuid=node_uuid, node=new_node)
        if ret.check() is False:
            return ret.dumps_json()
        return RetStatus(True, "add node success.")
    @jwt_required()
    def put(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        target_node = tm.find_node(node_uuid=node_uuid)
        if target_node.check() is False:
            return target_node.dumps_json()
        req_json = json.dumps(request.get_json())
        load_data, error = ReqNodeSchema().loads(req_json)
        if error:
            return RetStatus(False, "parse request data failed.")
        target_node.data['title']                = load_data['title']
        target_node.data['is_student']          = load_data['is_student']
        target_node.data['identity_coding']     = load_data['identity_coding']
        update_ret = tm.update_node(target_node.data)
        if update_ret.check() is False:
            return update_ret.dumps_json()
        return RetStatus(True, "update node success.")
    @jwt_required()
    def delete(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return RetStatus(False, "get manager handle failed. ").dumps_json()
        del_ret = tm.delete_node(node_uuid=node_uuid)
        if del_ret.check() is False:
            return del_ret.dumps_json()
        return RetStatus(True, "delete node success")
