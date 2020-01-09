from flask import Blueprint,Response,request
from service import BookService,WeekReadTimeService
import json,datetime
from datetime import timedelta

addBookRoute = Blueprint('addBookRoute', __name__)


@addBookRoute.route('/getNamesLike',methods=["POST"])
def getNamesLike():
    name = request.form.get("name")
    name = str(name).lower()
    return Response(json.dumps(BookService.getNamesLike(name)), mimetype='application/json')


@addBookRoute.route('/getByName',methods=["POST"])
def getByName():
    name = request.form.get("name")
    name = str(name).lower()
    return Response(BookService.getByLowName(name), mimetype='application/json')


@addBookRoute.route('/addBook',methods=["POST"])
def addBook():
    name = request.form.get("name")
    wordCount = request.form.get("wordCount")
    if name is None or name == "":
        return "请填写书名"
    name = str(name).strip()
    lowName = name.lower()
    # 判断是否已经存在，如果已经存在，就不是第一次读
    books = json.loads(BookService.getByLowName(lowName))
    isNew = 1
    if len(books) > 0:
        isNew = 0
        for b in books:
            # 如果结束时间不为空，说明没有看完，不能添加新的
            if b["finishTime"] == "None" or b["finishTime"] == "":
                return "当前这本书还没有读完，请不要重复添加"
    if (wordCount is None or wordCount == "") and len(books) > 0:
        wordCount = books[0]["wordCount"]
    if wordCount is None or wordCount == "":
        wordCount = 0
    BookService.insert(name, lowName, wordCount, isNew)
    return "添加成功"


@addBookRoute.route('/getNotFinishBook',methods=["POST"])
def getNotFinishBook():
    return Response(BookService.getNotFinishBook(), mimetype='application/json')


@addBookRoute.route('/getRecentBookList',methods=["POST"])
def getRecentBookList():
    return Response(BookService.getRecentBookList(), mimetype='application/json')


@addBookRoute.route('/setBookFinished',methods=["POST"])
def setBookFinished():
    id = request.form.get("id")
    BookService.setBookFinished(id)
    return "OK"

@addBookRoute.route('/setWordCount',methods=["POST"])
def setWordCount():
    id = request.form.get("id")
    wordCount = request.form.get("wordCount")
    BookService.setWordCount(id, wordCount)
    return "OK"


@addBookRoute.route('/addWeekTime', methods=["POST"])
def addWeekTime():
    date = request.form.get("date")
    hour = request.form.get("hour")
    min = request.form.get("min")
    if date is None or date == "":
        dt = datetime.datetime.now()
    else:
        dt = datetime.datetime.strptime(date, "%Y%m%d")
    startTime = datetime.datetime.strftime(dt - timedelta(days=dt.weekday()), "%Y-%m-%d")
    endTime = datetime.datetime.strftime(dt + timedelta(days=6-dt.weekday()), "%Y-%m-%d")
    totalMin = str(int(hour) * 60 + int(min))
    weekInDb = json.loads(WeekReadTimeService.getByStartTime(startTime))
    if len(weekInDb) > 0:
        # 存在，会更新
        WeekReadTimeService.update(startTime, totalMin)
    else:
        # 不存在，添加
        WeekReadTimeService.insert(startTime, endTime, totalMin)
    return "OK"