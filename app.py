from flask import Flask, request, jsonify
from lsystem import LSystem 
import json
app = Flask(__name__)

# def settings_builder()

@app.route('/params/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    js = request.args.get("json", None)

    # For debugging
    print("got params {}".format(js))

    response = {}
 
    if not js:
        response["ERROR"] = "no params found, please enter params."
    else:
        response["CONTENT"] = json.loads(js)

    # Return the response in json format
    return response

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": "Welcome {} to our awesome platform!!".format(name),
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)