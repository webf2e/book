from flask import Flask
from router.AddBookRouter import addBookRoute
from router.IndexRouter import indexRoute
from router.HisRouter import hisRoute
from service import InitService

app = Flask(__name__)
app.register_blueprint(addBookRoute)
app.register_blueprint(indexRoute)
app.register_blueprint(hisRoute)

InitService.init()

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8030)
