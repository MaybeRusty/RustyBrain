from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import uuid
import json

from common.database import db
from common.ret_status import RetStatus

class TreeManager:
    def __init__(self, model_obj=None, session=None):
        self.__model   = model_obj
        self.__session = session

    def get_root_node(self, node_uuid=None, many=False):
        tmp_model = self.__model
        ret = RetStatus(status=True)
        if many:
            try:
                ret.data = tmp_model.query.filter(tmp_model.root_uuid == tmp_model.node_uuid, tmp_model.parent_uuid == "").all()
            except SQLAlchemyError as e:
                return RetStatus(False, e.message)
        else:
            if node_uuid is None:
                return RetStatus(False, "invalid node uuid.")
            else:
                try:
                    ret.data = tmp_model.query.filter(tmp_model.root_uuid == tmp_model.node_uuid, tmp_model.node_uuid == node_uuid).first()
                except SQLAlchemyError as e:
                    return RetStatus(False, e.message)
        return ret

    def add_node(self, node_uuid=None, node=None):
        tmp_session = self.__session
        tmp_model   = self.__model
        if node is None:
            return RetStatus(False, "invalid insert node.")
        """add node as root"""
        if node_uuid is None:
            node.node_uuid   = uuid.uuid1()
            node.root_uuid   = node.node_uuid
            node.parent_uuid = ""
            node.left        = 0
            node.right       = 1
            try:
                tmp_session.add(node)
                tmp_session.commit()
            except SQLAlchemyError as e:
                return RetStatus(False, e.message)
        else:
            try:
                target_node = tmp_model.query.filter(tmp_model.node_uuid==node_uuid).first()
            except SQLAlchemyError as e:
                return RetStatus(False, e.message)
            if target_node is None:
                return RetStatus(False, "invalid node uuid.")
            else:
                """add node as the last children"""
                node.node_uuid   = uuid.uuid1()
                node.root_uuid   = target_node.root_uuid
                node.parent_uuid = target_node.node_uuid
                node.left        = target_node.right
                node.right       = target_node.right + 1
                try:
                    tmp_model.query.filter(tmp_model.left>target_node.right).update({tmp_model.left:tmp_model.left+2})
                    tmp_model.query.filter(tmp_model.right>=target_node.right).update({tmp_model.right:tmp_model.right+2})
                    tmp_session.add(node)
                    tmp_session.commit()
                except SQLAlchemyError as e:
                    return RetStatus(False, e.message)
        return RetStatus(True)

    """check node uuid exist"""
    def check(self, node_uuid=None):
        tmp_model = self.__model
        node = None
        if node_uuid is None:
            return RetStatus(False, "invalid node uuid.")
        try:
            node = tmp_model.query.filter(tmp_model.node_uuid == node_uuid).first()
        except SQLAlchemyError as e:
            return RetStatus(False, e.message)
        if node is None:
            return RetStatus(False, "nothing be searched.")
        return RetStatus(True)

    """delete node and children"""
    def delete_node(self, node_uuid=None, node=None ):
        tmp_session = self.__session
        tmp_model   = self.__model
        if node:
            try:
                tmp_model.query.filter(tmp_model.root_uuid == node.root_uuid, tmp_model.left>=node.left,tmp_model.right<=node.right).delete()
                tmp_model.query.filter(tmp_model.root_uuid == node.root_uuid, tmp_model.left>node.right).update({tmp_model.left:tmp_model.left-(node.right-node.left)-1})
                tmp_model.query.filter(tmp_model.root_uuid == node.root_uuid, tmp_model.right>node.right).update({tmp_model.right:tmp_model.right-(node.right-node.left)-1})
                tmp_session.commit()
            except SQLAlchemyError as e:
                return RetStatus(False, e.message)
            return RetStatus(True)
        if node_uuid is None:
            return RetStatus(False, "invalid node uuid.")
        else:
            try:
                node = tmp_model.query.filter(tmp_model.node_uuid==node_uuid).one()
            except SQLAlchemyError as e:
                return RetStatus(False, e.message)
            if node is None:
                return RetStatus(False, "invalid node uuid.")
            else:
                try:
                    tmp_model.query.filter(tmp_model.root_uuid == node.root_uuid, tmp_model.left>=node.left,tmp_model.right<=node.right).delete()
                    tmp_model.query.filter(tmp_model.root_uuid == node.root_uuid, tmp_model.left>node.right).update({tmp_model.left:tmp_model.left-(node.right-node.left)-1})
                    tmp_model.query.filter(tmp_model.root_uuid == node.root_uuid, tmp_model.right>node.right).update({tmp_model.right:tmp_model.right-(node.right-node.left)-1})
                    tmp_session.commit()
                except SQLAlchemyError as e:
                    return RetStatus(False, e.message)
        return RetStatus(True)

    """delete multiple nodes"""
    def delete_nodes(self, node_uuids=None):
        if not isinstance(node_uuids, list):
            return RetStatus(False, "invalid node uuids list.")
        else:
            node_error = []
            for uuid in node_uuids:
                ret = self.delete_node(uuid)
                if ret.check() is False:
                    node_error.append(uuid)
            if node_error:
                return RetStatus(False, "some node delete failed.", json.dumps(node_error))
        return RetStatus(True)

    """find one node or many nodes"""
    def find_node(self, node_uuid=None, many=False, parents=False):
        tmp_model   = self.__model
        if node_uuid is None:
            return RetStatus(False, "invalid node uuid.")
        else:
            try:
                node = tmp_model.query.filter(tmp_model.node_uuid==node_uuid).first()
            except SQLAlchemyError as e:
                return RetStatus(False, e.message)
            if many:
                nodes = None
                if parents:
                    try:
                        nodes = tmp_model.query.filter(tmp_model.root_uuid == node.root_uuid, tmp_model.node_uuid==node.parent_uuid).all()
                    except SQLAlchemyError as e:
                        return RetStatus(False, "find parents nodes failed.")
                    return RetStatus(True, data=nodes)
                else:
                    try:
                        nodes = tmp_model.query.filter(tmp_model.root_uuid == node.root_uuid, tmp_model.parent_uuid==node.node_uuid).all()
                    except SQLAlchemyError as e:
                        return RetStatus(False, "find children nodes failed.")
                    return RetStatus(True, data=nodes)
            elif node is None:
                return RetStatus(False, "nothing will be search.")
            else:
                return RetStatus(True, data=node)

    """update node"""
    def update_node(self, node=None):
        tmp_session = self.__session
        if node is None:
            return RetStatus(False, msg="invalid node.")
        else:
            try:
                tmp_session.commit()
            except SQLAlchemyError as e:
                return RetStatus(False, e.message)
            return RetStatus(True)

class TreeMixin:
    node_uuid       = db.Column(db.String(36), primary_key=True)
    root_uuid       = db.Column(db.String(36))
    parent_uuid     = db.Column(db.String(36))
    left            = db.Column(db.Integer, default=0)
    right           = db.Column(db.Integer, default=0)
