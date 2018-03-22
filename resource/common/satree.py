from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import uuid

from common.database import db
from common.ret_status import RetStatus

class TreeManager:
    def __init__(self, model_obj=None, session=None):
        self.__model   = model_obj
        self.__session = session
    def get_root_node(self):
        tmp_model = self.__model
        ret = RetStatus(status=True)
        try:
            ret.data = tmp_model.query.filter(tmp_model.parent_uuid=="").first()
        except SQLAlchemyError as e:
            ret.restore(msg=e.message)
        return ret
    def add_node(self, node_uuid=None, node=None):
        tmp_session = self.__session
        tmp_model   = self.__model
        ret = RetStatus(status=True)
        if node is None:
            ret.restore(status=False, msg="invalid insert node.")
            return ret
        """add node as root"""
        if node_uuid is None:
            node.node_uuid   = uuid.uuid1()
            node.parent_uuid = ""
            node.left        = 0
            node.right       = 1
            try:
                tmp_session.add(node)
                tmp_session.commit()
            except SQLAlchemyError as e:
                ret.restore(False, e.message)
                return ret
        else:
            try:
                opt_node = tmp_model.query.filter(tmp_model.node_uuid==node_uuid).first()
            except SQLAlchemyError as e:
                ret.restore(False, e.message)
                return ret
            if opt_node is None:
                ret.restore(False, "invalid node_uuid.")
                return ret
            else:
                """add node as the last node of the same level"""
                node.node_uuid   = uuid.uuid1()
                node.parent_uuid = opt_node.node_uuid
                node.left        = opt_node.right
                node.right       = opt_node.right + 1
                try:
                    tmp_model.query.filter(tmp_model.left>opt_node.right).update({tmp_model.left:tmp_model.left+2})
                    tmp_model.query.filter(tmp_model.right>=opt_node.right).update({tmp_model.right:tmp_model.right+2})
                    tmp_session.add(node)
                    tmp_session.commit()
                except SQLAlchemyError as e:
                    ret.restore(False, e.message)
                    return ret
        return ret
    """delete node and children"""
    def delete_node(self, node_uuid=None):
        tmp_session = self.__session
        tmp_model   = self.__model
        ret = RetStatus(status=True)
        if node_uuid is None:
            ret.restore(status=False, msg="invalid node_uuid.")
            return ret
        else:
            node = None
            try:
                node = tmp_model.query.filter(tmp_model.node_uuid==node_uuid).one()
            except SQLAlchemyError as e:
                ret.restore(False, e.message)
                return ret
            if node is None:
                ret.restore(False, "invalid node_uuid.")
                return ret
            else:
                try:
                    tmp_model.query.filter(tmp_model.left>=node.left,tmp_model.right<=node.right).delete()
                    tmp_model.query.filter(tmp_model.left>node.right).update({tmp_model.left:tmp_model.left-(node.right-node.left)-1})
                    tmp_model.query.filter(tmp_model.right>node.right).update({tmp_model.right:tmp_model.right-(node.right-node.left)-1})
                    tmp_session.commit()
                except SQLAlchemyError as e:
                    ret.restore(False, e.message)
                    return ret
        return ret
    def delete_nodes(self, node_uuids=None):
        ret = RetStatus(status=True)
        if not isinstance(node_uuids, list):
            ret.restore(False, "invalid node_uuids.")
            return ret
        else:
            for id in node_uuids:
                self.delete_node(id)
        return ret
    """find one node or many nodes"""
    def find_node(self, node_uuid=None, many=False, parents=False):
        tmp_session = self.__session
        tmp_model   = self.__model
        ret         = RetStatus(True)
        if node_uuid is None:
            ret.restore(False, "invalid node_uuid.")
            return ret
        else:
            try:
                node = tmp_model.query.filter(tmp_model.node_uuid==node_uuid).first()
            except SQLAlchemyError as e:
                ret.restore(False, e.message)
                return ret
            if many:
                nodes = None
                if parents:
                    try:
                        nodes = tmp_model.query.filter(tmp_model.node_uuid==node.parent_uuid).all()
                    except SQLAlchemyError as e:
                        ret.restore(False, "find parents nodes failed.")
                        return ret
                    ret.restore(True, data=nodes)
                    return ret
                else:
                    try:
                        nodes = tmp_model.query.filter(tmp_model.parent_uuid==node.node_uuid).all()
                    except SQLAlchemyError as e:
                        ret.restore(False, "find children nodes failed.")
                        return ret
                    ret.restore(True, data=nodes)
                    return ret
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
    parent_uuid     = db.Column(db.String(36))
    left            = db.Column(db.Integer, default=0)
    right           = db.Column(db.Integer, default=0)
