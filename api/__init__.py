from flask_restful import Api
from app import appInstance
from . TaskPagination import TaskPagination

restServer = Api(appInstance)
restServer.add_resource(TaskPagination,"/api/TaskPagination")
