from flask import Flask, render_template, request, jsonify, redirect, url_for
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



if __name__ == '__main__':
    app.run()
