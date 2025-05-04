from flask import Flask, app, render_template



app = Flask(__name__)

@app.route('/', methods=['GET'])
def inicio():
    return render_template('inicio.html')

if __name__ == '__main__':
    app.run(debug=True)  