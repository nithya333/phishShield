from flask import Flask, jsonify, render_template, request, session
import redis
import json
import time
from pymongo import MongoClient
from flask_session import Session

server = Flask(__name__)
redisPort = 6379
redisClient = redis.Redis("localhost", redisPort)

server.config["SESSION_PERMANENT"] = False
server.config["SESSION_TYPE"] = "filesystem"
Session(server)

client = MongoClient("mongodb+srv://nithya3169:6sV97gWqdcKFtAru@cluster0phish.0qs5f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0Phish")
data_base = client["test"]


def check_blacklist_whitelist(input_url):
    # TO-DO
    return -1

def check_in_history(input_url):
    try:
        result = -1
        details = data_base.history.find({"url":input_url})[0]
        print(details)
        if details:
            result = details["status"]
        return result
    except:
        return -1

def add_to_history(url, status):
    status = (int)(status)
    data_base.history.insert_one({'url': url, 'status': status})

# Just for testing purpose without redis
# http://127.0.0.1:5000/add_history?url=https:%2F%2Fwww.youtube.com%2F&status=0 for testing
@server.route("/add_history", methods=["GET"])
def add():
    url = request.args.get('url')
    status = (int)(request.args.get('status'))
    data_base.history.insert_one({'url': url, 'status': status})
    details = data_base.history.find()
    return render_template("view_history.html",details = details)

@server.route("/", methods=["GET"])
def home():
    session.clear() 
    session["ans"] = "unknown"
    return render_template("home.html")

@server.route("/view_history", methods=["GET"])
def dashboard():
    details = data_base.history.find()
    return render_template("view_history.html",details = details)


@server.route("/url_detect",methods=["POST"])
def submitURL():
    data=request.get_json()
    if 'url' not in data:
        return jsonify({'error: no url provided'}),400
    url=data['url']
    print(url)

    # Check in blacklist whitelist
    res1 = check_blacklist_whitelist(url)
    if (res1 == 1):
        session["ans"] = "phishing"
        return jsonify({'url': url, 'prediction': "phishing", 'message': 'Blacklist-Whitelist Detection'})
    elif (res1 == 0):
        session["ans"] = "legit"
        return jsonify({'url': url, 'prediction': "legit", 'message': 'Blacklist-Whitelist Detection'})

    # Check in our history
    res2 = check_in_history(url)
    if (res2 == 1):
        session["ans"] = "phishing"
        return jsonify({'url': url, 'prediction': "phishing", 'message': 'History Detection'})
    elif (res2 == 0):
        session["ans"] = "legit"
        return jsonify({'url': url, 'prediction': "legit", 'message': 'History Detection'})

    # Predict with ML
    url = {"url": data['url']}
    print(url)
    if redisClient:
        redisClient.rpush("UrlQueue", json.dumps(url))
    else:
        print("System error")
    return jsonify({'message': 'URL submitted successfully. Please check back later for the result.'})

@server.route("/result", methods=["GET"])
def get_result():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'no url provided'}), 400

    if (session["ans"] == "phishing"):
        return jsonify({'url': url, 'prediction': "phishing"})
    elif (session["ans"] == "legit"):
        return jsonify({'url': url, 'prediction': "legit"})

    # Retrieve the prediction result from the Redis hash
    prediction = redisClient.hget("url_predictions", url)
    if not prediction:
        return jsonify({'message': 'Prediction is still being processed, please check again later.'}), 202
    
    # Optionally delete the result after retrieval
    redisClient.hdel("url_predictions", url)
    
    if (prediction.decode('utf-8') == "phishing"):
        add_to_history(url, 1)
    elif (prediction.decode('utf-8') == "legit"):
        add_to_history(url, 0)

    return jsonify({'url': url, 'prediction': prediction.decode('utf-8')})

if __name__ == "__main__":
    server.run(debug=True)
