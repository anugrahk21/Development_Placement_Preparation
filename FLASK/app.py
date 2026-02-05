from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    user = {"name":"Anugrah K", "logged_in": True, "hobbies": ["coding", "gaming", "traveling"]}
    return render_template('index.html', user=user)
    # render_template -> This function is used to render an HTML template.
    # In this case, it will look for a file named index.html in the templates folder and render it as the response to the GET request at the root URL (/).

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    error = None

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        comments = request.form.get('comments')

        if not name or not email or not comments:
            error = "All fields are required."
        elif '@' not in email:
            error = "Invalid email address."
        else:
            print(f"Feedback received from {name} ({email}): {comments}")

    return render_template('feedback.html', error=error)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask application in debug mode, no need to run python app.py again and again for changes.
                        # Just refresh the browser to see the changes.


# This is a simple Flask application with four routes:
# 1. A GET route at / that renders an HTML template called index.html.
# 2. A GET route at /hello that returns a JSON message "Hello, World!".
# 3. A POST route at /echo that echoes back the JSON data sent in the request body.
# 4. A GET route at /dashboard that renders an HTML template called dashboard.html.
