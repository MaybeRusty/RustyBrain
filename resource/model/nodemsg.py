from common.schema import ma
from common.database import db, basic_opt
from model.nodetree import NodeTree

node_m2m_msg = db.Table('t_relate_nodemsg',
                         db.Column('msg_uuid', db.String(36), db.ForeignKey('NodeMsg.uuid')),
                         db.Column('node_uuid', db.String(36), db.ForeignKey('NodeTree.node_uuid')))

class NodeMsg(db.Model, basic_opt):
    uuid            = db.Column(db.Integer, primary_key=True, autoincress=True)
    title           = db.Column(db.String(128), nullable=False)
    msg             = db.Column(db.String(256), nullable=False)
    nodes           = db.relationship('NodeTree', secondary=node_m2m_msg, lazy='dynamic', backref=db.backref('msgs', lazy='joined'))

class OutMsgSchema(ma.Schema):
    class Meta:
        fields = ('title', 'msg', 'uuid')
