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

	@classmethod
	def DEL(cls, node):
		try:
			db.session.delete(node)
			db.session.commit()
		except SQLAlchemyError as e:
			return RetStatus(False, e.message)
		return RetStatus(True, "delete success.")

	@classmethod
	def UPDATE(cls):
		try:
			db.session.commit()
		except SQLAlchemyError as e:
			return RetStatus(False, e.message)
		return RetStatus(True, "update success.")

	@classmethod
	def ROLL_BACK(cls):
		try:
			db.session.rollback()
		except SQLAlchemyError as e:
			return RetStatus(False, e.message)
		return RetStatus(True, "roll back success.")
