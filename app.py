from flask import Flask
from router.AddBookRouter import addBookRoute
from service import InitService

app = Flask(__name__)
app.register_blueprint(addBookRoute)

InitService.init()

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8030)
