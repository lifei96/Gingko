from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
import json
import server.api

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

# on the home page, when put into search bar
@app.route("/search", methods=['GET','POST'])
def search():
    """API that takes in a specific url and assess its credibility
    Parameter: Url
    Returns:
        json object of credibility score and its breakdowns
    """
    searchUrl = request.args.get('websiteAddress')
    data = server.api.get_score(searchUrl)


    if len(data) == 0:
        return render_template('search.html', error = "Please enter a valid website")

    print(data)

    return render_template('search.html', data = json.dumps(data))


# vanilla API
@app.route("/api", methods=['GET'])
def api():
    """API that takes in a specific url and assess its credibility
    Parameter: Url
    Returns:
        json object of credibility score and its breakdowns
    """
    url = request.args.get('url')
    print(url)
    data = server.api.get_score(url)
    print(data)

    if len(data) == 0:
        return "Please enter a valid website!"

    json_str = json.dumps(data, indent=4)
    print(json_str)
    return Response(json_str, mimetype='application/json')


if __name__ == '__main__':
    # app.run()
    app.run(host="0.0.0.0", port=80, threaded=True)
