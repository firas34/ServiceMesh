from flask import Flask
import os
app = Flask(__name__)

@app.route('/applyRule')
def applyRule():
    stream = os.popen('kubectl apply -f rule.yaml')
    return stream.read()


if __name__ == "__main__":
	app.run(port=9090)
