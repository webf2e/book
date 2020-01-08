from flask import Blueprint,Response,request
from service import BookService,WeekReadTimeService
import json,datetime
from util.Global import gloVar

indexRoute = Blueprint('indexRoute', __name__)


@indexRoute.route('/getGoal',methods=["POST"])
def getGoal():
    goal = {}
    goal["goal"] = gloVar.goal
    goal["start"] = gloVar.goalStartTime
    goal["end"] = gloVar.goalEndTime
    goal["current"] = int(BookService.getFinishedCount(gloVar.goalStartTime, gloVar.goalEndTime))
    goal["percent"] = str(round(goal["current"] / int(gloVar.goal) * 100, 5))
    return Response(json.dumps(goal), mimetype='application/json')
