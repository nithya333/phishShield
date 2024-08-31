from flask import Flask, jsonify, render_template, request
import redis
import json
import time

server = Flask(__name__)
redisPort = 6379
redisClient = redis.Redis("localhost", redisPort)

@server.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@server.route("/url_detect", methods=["POST"])
def submitURL():
    data = request.get_json()
    if 'url' not in data:
        return jsonify({'error': 'no url provided'}), 400
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

    # Retrieve the prediction result from the Redis hash
    prediction = redisClient.hget("url_predictions", url)
    if not prediction:
        return jsonify({'message': 'Prediction is still being processed, please check again later.'}), 202
    
    # Optionally delete the result after retrieval
    redisClient.hdel("url_predictions", url)
    
    return jsonify({'url': url, 'prediction': prediction.decode('utf-8')})

if __name__ == "__main__":
    server.run(debug=True)
