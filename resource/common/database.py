from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from common.ret_status import RetStatus

db = SQLAlchemy()

class basic_opt:
	@classmethod
	def ADD(cls, node):
		try:
			db.session.add(node)
			db.session.commit()
		except SQLAlchemyError as e:
			return RetStatus(False, e.message)
		return RetStatus(True, "add success.")
	def DEL(cls, node):
		try:
			db.session.delete(node)
			db.session.commit()
		except SQLAlchemyError as e:
			return RetStatus(False, e.message)
		return RetStatus(True, "delete success.")
	def UPDATE(cls):
		try:
			db.session.commit()
		except SQLAlchemyError as e:
			return RetStatus(False, e.message)
		return RetStatus(True, "update success.")
