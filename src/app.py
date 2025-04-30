from flask import Flask, app, request, jsonify



app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)  