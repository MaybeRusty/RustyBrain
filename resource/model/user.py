from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from common.database import db, basic_opt
from common.schema import ma
from common.ret_status import RetStatus

class User(db.Model, basic_opt):
    __tablename__   = "t_auth_user"
    uuid 			= db.Column(db.String(36), primary_key=True)
    username        = db.Column(db.String(128), nullable=False)
    hash_password   = db.Column(db.String(128), nullable=False)
    login_type      = db.Column(db.Boolean, default=False)
    create_time		= db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @property
    def password(self):
        raise AttributeError("password can't be read.")
    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)
    def confirm_password(self, password):
        return check_password_hash(self.hash_password, password)
    @classmethod
    def find_by_username(cls, username):
        user = None
        try:
            user = cls.query.filter(cls.username == username).first()
        except SQLAlchemyError as e:
            return RetStatus(False, e.message)
        return RetStatus(status=True, data=user)
    @classmethod
    def find_by_uuid(cls, uuid):
        user = None
        try:
            user = cls.query.filter(cls.uuid == uuid).first()
        except SQLAlchemyError as e:
            return RetStatus(False, e.message)
        return RetStatus(True, data=user)
