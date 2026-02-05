from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')
    # render_template -> This function is used to render an HTML template.
    # In this case, it will look for a file named index.html in the templates folder and render it as the response to the GET request at the root URL (/).

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
# This is a simple Flask application with two routes:
# 1. A GET route at / that renders an HTML template called index.html.
# 2. A GET route at /hello that returns a JSON message "Hello, World!".
# 3. A POST route at /echo that echoes back the JSON data sent in the request body.
