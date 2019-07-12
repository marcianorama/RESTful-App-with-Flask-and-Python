from flask import session, request
from flask_restful import Resource
import logging as logger
from flask_pymongo import pymongo
import time
from bson.json_util import dumps
from api import AppUtil

import json

mongo = pymongo.MongoClient("mongodb+srv://shivenpurohit:microsoft12#@urbanpiper-mckcy.mongodb.net/test?retryWrites=true&w=majority")
task = mongo.db.Task

class TaskPagination(Resource):   # Task class inheriting from Resource class

    # get task list for current user
    def get(self):
        if ('username' in session):
            if(session['role'] == 'Store Manager'):
                myCursor = task.find({'originator':session['username']})
            elif(session['role'] == 'Delivery Person'):
                myCursor = task.find({'state':'new'})
            ret = []
            for data in myCursor:
                ret.append(dumps(data))
            return ret,200
        return "You're not logged in"

    # create new task
    def post(self):
        if('username' in session):
            if(request.form['operation']=='create'):
                if(session['role']=='Store Manager'):

                    #create data for inserting into db
                    res = {}
                    res['originated'] = int(round(time.time() * 1000))
                    taskid = 'Task-'+str(res['originated'])
                    res['taskid'] = taskid
                    res['priority'] = request.form['Priority']
                    res['title'] = request.form['Title']
                    res['originator'] = session['username']
                    res['state'] = 'new'

                    # insert into db
                    task.insert(res)
                    # fetch details from db
                    ret = dumps(task.find_one({'taskid':taskid}))
                    return ret, 200
                return "You don't have required access to create task."
        return "You're not logged in"

    def put(self):
        # update task info
        if(request.form['operation'] == 'accepted'):
            if (session['role'] == 'Delivery Person'):
                # accept request
                taskid = request.form["taskid"]
                findquery = {"taskid": taskid}
                res = {}
                res['state'] = 'accepted'; res['assignedto'] = session['username']
                # insert into db
                task.update_one(findquery, {"$set": res})
                # fetch details from db
                ret = dumps(task.find_one({'taskid': taskid}))
            return "You don't have required access to accept task."
        elif(request.form['operation'] == 'declined'):
            if (session['role'] == 'Delivery Person'):
                # declined request
                taskid = request.form["taskid"]
                findquery = {"taskid": taskid}
                res = {}
                res['state'] = 'new'; res['assignedto'] = None
                # insert into db
                task.update_one(findquery, {"$set": res})
                # fetch details from db
                ret = dumps(task.find_one({'taskid': taskid}))
            return "You don't have required decline to accept task."

        elif(request.form['operation'] == 'cancelled'):
            if (session['role'] == 'Store Manager'):
                # cancel request
                taskid = request.form["taskid"]
                findquery = {"taskid": taskid}
                res = {}
                res['state'] = 'cancelled';
                # insert into db
                task.update_one(findquery, {"$set": res})
                # fetch details from db
                ret = dumps(task.find_one({'taskid': taskid}))
            return "You don't have required access to cancel task."

        elif(request.form['operation'] == 'completed'):
            # completed
            myquery = {'taskid': taskid}
            setValue = {'$set': {'state': "completed"}}
            task.update_one(myquery, setValue)

        return ret, 200
    def delete(self):
        id = request.form['taskid']
        query = task.delete_many({"taskid": id})

        ret = {}
        ret['acknowledged'] = query.acknowledged
        ret['deletedCount'] = query.deleted_count

        return ret, 200;

