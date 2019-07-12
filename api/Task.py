from flask_restful import Resource
import logging as logger

class Task(Resource):   # Task class inheriting the Resource class
    def get(self):
        logger.debug("Inside get method")
        ret = {"message":"inside get method"}
        return ret,200
    def post(self):
        logger.debug("Inside post method")
        ret = {"message": "inside post method"}
        return ret, 200
    def put(self):
        logger.debug("Inside put method")
        ret = {"message": "inside put method"}
        return ret, 200
    def delete(self):
        logger.debug("Inside delete method")
        ret = {"message": "inside delete method"}
        return ret, 200