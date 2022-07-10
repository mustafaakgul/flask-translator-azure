from flask import Flask, redirect, url_for, request, render_template, session

app = Flask(__name__)


# flash.run


@app.route('/', methods=['GET'])
def index():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
