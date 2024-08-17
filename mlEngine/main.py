from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import joblib
import json
import redis
from classify import extract

RedisPort=6379
redisClient =redis.Redis("localhost",RedisPort)


rf_classifier=joblib.load("rf.joblib")

def predict(features_df):
  prediction=rf_classifier.predict(features_df)
  print(prediction)
  return prediction
  
  
if __name__=="__main__":
  while True:
    if(redisClient.llen("paramsQueue")>0):
      json_str=redisClient.lpop("paramsQueue")
      features=extract(json.loads(json.loads(json_str)))
      print(features)
      print(features.head())
      predict(features)
