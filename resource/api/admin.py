from flask_restful import Resource, request
import json
import uuid

from common.database import db
from common.ret_status import RetStatus
from model.admin import Admin, BasicSchema

class AdminOpt(Resource):
    def post(self):
        req_json  = json.dumps(request.get_json())
        load_data, errors = BasicSchema().loads(req_json)
        if errors:
            return RetStatus(False, "parse request data failed.").dumps_json()
        ret = Admin.find_by_username(load_data['username'])
        if ret.check() is False:
            return RetStatus(False, "check user's availability failed.").dumps_json()
        elif ret.data is None:
            return RetStatus(False, "username had be used.").dumps_json()
        user = Admin(uuid=uuid.uuid1(), username=load_data['username'], password=load_data['password'], login_type=load_data['login_type'])
        add_ret = Admin.ADD(user)
        if add_ret.check() is False:
            return add_ret.dumps_json()
        return RetStatus(True, "register success.", data=user.uuid).dumps_json()
