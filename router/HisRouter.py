from flask import Blueprint,Response,request
from service import BookService

hisRoute = Blueprint('hisRoute', __name__)


@hisRoute.route('/getByPage',methods=["POST"])
def getByPage():
    pageIndex = int(request.form.get("pageIndex"))
    pageSize = int(request.form.get("pageSize"))
    return Response(BookService.getByPage(pageIndex, pageSize), mimetype='application/json')