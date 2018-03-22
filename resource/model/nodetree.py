import datetime

from common.database import db
from common.schema import ma
from common.satree import TreeMixin

class NodeTree(db.Model, TreeMixin):
    __tablename__   = "t_data_nodetree"
    title           = db.Column(db.String(128), nullable=False)
    is_student      = db.Column(db.Boolean, default=False)
    identity_coding = db.Column(db.String(128), default="")
    c_time          = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class ReqNodeSchema(ma.Schema):
    class Meta:
        fields = ('title', 'is_student', 'identity_coding')

class RspNodeSchema(ma.Schema):
    class Meta:
        fields = ('title', 'node_uuid', 'identity_coding')
