from flask import Flask,jsonify,render_template,request
import redis
import json

server=Flask(__name__)
redisPort=6379




redisClient=redis.Redis("localhost",redisPort)

@server.route("/",methods=["GET"])
def home():
    return render_template("home.html")

@server.route("/url_detect",methods=["POST"])
def submitURL():
    data=request.get_json()
    if 'url' not in data:
        return jsonify({'error: no url provided'}),400
    url={"url":data['url']}
    print(url)
    if redisClient:
        redisClient.rpush("UrlQueue",json.dumps(url))
    else:
        print("System error")
    return "hello"
