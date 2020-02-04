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
    currentDays = datetime.datetime.now().timestamp() - datetime.datetime(datetime.datetime.now().year, 1, 1).timestamp()
    totalDays = datetime.datetime(datetime.datetime.now().year, 12, 31).timestamp() - datetime.datetime(datetime.datetime.now().year, 1, 1).timestamp()
    goal["dayPercent"] = str(round(currentDays / totalDays * 100, 5))
    return Response(json.dumps(goal), mimetype='application/json')


@indexRoute.route('/getWeeks',methods=["POST"])
def getWeeks():
    count = request.form.get("count")
    return Response(WeekReadTimeService.getWeeks(count), mimetype='application/json')


@indexRoute.route('/getReadCountMonthlyByTime',methods=["POST"])
def getReadCountMonthlyByTime():
    startTime = datetime.date.today() - datetime.timedelta(days=365)
    startTime = startTime - datetime.timedelta(days=startTime.day - 1)
    return Response(BookService.getReadCountMonthlyByTime(str(startTime)), mimetype='application/json')


@indexRoute.route('/lastWeekTongji',methods=["POST"])
def lastWeekTongji():
    lastWeekInfo = {}
    now = datetime.datetime.now()
    lastWeekStart = datetime.datetime.strftime(now - datetime.timedelta(days=now.weekday() + 7), "%Y-%m-%d")
    lastWeekEnd = datetime.datetime.strftime(now - datetime.timedelta(days=now.weekday()+1), "%Y-%m-%d")
    weekReadTime = json.loads(WeekReadTimeService.getByStartTime(lastWeekStart))
    if len(weekReadTime) != 0:
        lastWeekInfo["totalReadTime"] = weekReadTime[0]["readMin"]
        lastWeekInfo["avgReadTimeDaily"] = int(weekReadTime[0]["readMin"]) // 7
    lastWeekInfo["startReadBooks"] = json.loads(BookService.getStartReadBooks(lastWeekStart + " 00:00:00", lastWeekEnd + "23:59:59"))
    lastWeekInfo["finishReadBooks"] = json.loads(BookService.getFinishReadBooks(lastWeekStart + " 00:00:00", lastWeekEnd + "23:59:59"))
    return Response(json.dumps(lastWeekInfo), mimetype='application/json')


@indexRoute.route('/getWeekData',methods=["POST"])
def getWeekData():
    week = request.form.get("week")
    weekInfo = {}
    now = datetime.datetime.strptime(week, "%Y-%m-%d")
    startTime = datetime.datetime.strftime(now - datetime.timedelta(days=now.weekday()), "%Y-%m-%d")
    endTime = datetime.datetime.strftime(now + datetime.timedelta(days=6 - now.weekday()), "%Y-%m-%d")
    weekInfo["startTime"] = startTime
    weekInfo["endTime"] = endTime
    weekReadTime = json.loads(WeekReadTimeService.getByStartTime(startTime))
    if len(weekReadTime) != 0:
        weekInfo["totalReadTime"] = weekReadTime[0]["readMin"]
        weekInfo["avgReadTimeDaily"] = int(weekReadTime[0]["readMin"]) // 7
    weekInfo["startReadBooks"] = json.loads(BookService.getStartReadBooks(startTime + " 00:00:00", endTime + "23:59:59"))
    weekInfo["finishReadBooks"] = json.loads(BookService.getFinishReadBooks(startTime + " 00:00:00", endTime + "23:59:59"))
    return Response(json.dumps(weekInfo), mimetype='application/json')
