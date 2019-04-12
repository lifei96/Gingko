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
    print(searchUrl)
    if searchUrl == 'https://www.huffpost.com/entry/michelle-obama-pink-suit_n_5caf82f1e4b0ffefe3ad78f4':
        fake_data = [
            {"id": "Credibility", "score": 92},
            {"id": "Number of Images", "score": 88},
            {"id": "Number of Ads", "score": 76},
            {"id": "Reading Level", "score": 84},
            {"id": "Social Network Links", "score": 71},
            {"id": "Cross-site Citations", "score": 80},
            {"id": "Sentiment", "score": 95},
        ]
    else:
        fake_data = [
            {"id": "Credibility", "score": 27},
            {"id": "Number of Images", "score": 55},
            {"id": "Number of Ads", "score": 20},
            {"id": "Reading Level", "score": 15},
            {"id": "Social Network Links", "score": 33},
            {"id": "Cross-site Citations", "score": 23},
            {"id": "Sentiment", "score": 19},
        ]
    # data = server.api.get_score(searchUrl)
    data = fake_data


    if len(data) == 0:
        return render_template('search.html', error = "Please enter a valid website")

    print(data)

    return render_template('search.html', data = json.dumps(data))



if __name__ == '__main__':
    app.run()
