from sqlalchemy.exc import SQLAlchemyError

from common.schema import ma
from common.database import db, basic_opt
from common.ret_status import RetStatus
from model.nodetree import NodeTree

node_m2m_info = db.Table('t_relate_nodeinfo',
                         db.Column('info_uuid', db.String(36), db.ForeignKey('NodeInfo.uuid')),
                         db.Column('node_uuid', db.String(36), db.ForeignKey('NodeTree.node_uuid')))

class NodeInfo(db.Model, basic_opt):
    uuid            = db.Column(db.Integer, primary_key=True, autoincress=True)
    age             = db.Column(db.Integer)
    sex             = db.Column(db.Boolean, default=False)
    campuse_id      = db.Column(db.String(60), nullable=False)
    nodes           = db.relationship('NodeTree', secondary=node_m2m_info, lazy='dynamic', backref=db.backref('infos', lazy='joined'))

    @classmethod
    def find_by_uuid(cls, uuid):
        ret = RetStatus(True)
        try:
            ret.data = cls.query.filter(cls.uuid == uuid).first()
        except SQLAlchemyError as e:
            return RetStatus(False, e.message)
        return ret

class OutInfoSchema(ma.Schema):
    class Meta:
        fields = ('age', 'sex', 'campus_id', 'uuid')
