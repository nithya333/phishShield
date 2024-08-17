# -*- coding: utf-8 -*-
"""phishingEL_v4_integration_without_feat_ext.ipynb

Original file is located at
    https://colab.research.google.com/drive/16Bkly51ePsZBdOaSBSDNpmPuj_YQCeJA
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#import matplotlib.pyplot as plt
#import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import jaccard_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
import sklearn.metrics as metrics
from sklearn.inspection import permutation_importance
from scipy.stats import randint, uniform
import pickle
#import shap
#from xgboost import XGBClassifier
#import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
#from tensorflow.keras.models import Model, Sequential
#from tensorflow.keras.layers import Input, Embedding, Conv1D, Dropout, MaxPooling1D, LSTM, Flatten, Dense, Add
#from keras.callbacks import EarlyStopping, ModelCheckpoint
#from tensorflow.keras.optimizers import Adam
#from keras import regularizers
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.tree import DecisionTreeClassifier, export_graphviz, plot_tree, export_text
#import pydotplus
#from IPython.display import Image, display
import joblib
import json

#import feature_extraction_singleurl as fe_single

def extract(feature_dict):
  relevant_features_notnull = ['length_url', 'length_hostname', 'ip', 'path_extension', 'nb_dots', 'nb_hyphens', 'nb_at', 'nb_qm', 'nb_and', 'nb_eq', 'nb_slash','nb_colon', 'nb_semicolumn', 'nb_www', 'nb_com', 'nb_dslash', 'nb_spl', 'https_token', 'ratio_digits_url', 'ratio_digits_host','tld_in_path', 'tld_in_subdomain', 'abnormal_subdomain', 'nb_subdomains', 'prefix_suffix', 'shortening_service', 'shortest_words_raw','shortest_word_host', 'shortest_word_path', 'longest_words_raw', 'longest_word_host', 'longest_word_path', 'avg_words_raw', 'avg_word_host','avg_word_path', 'phish_hints', 'domain_in_brand', 'suspicious_tld', 'dns_record']
  df=pd.DataFrame([feature_dict])
  df = df[relevant_features_notnull]
  return df


'''  
def check_phish_or_leg(input_url_json):
  relevant_features_notnull = ['length_url', 'length_hostname', 'ip', 'path_extension', 'nb_dots', 'nb_hyphens', 'nb_at', 'nb_qm', 'nb_and', 'nb_eq', 'nb_slash',
                                'nb_colon', 'nb_semicolumn', 'nb_www', 'nb_com', 'nb_dslash', 'nb_spl', 'https_token', 'ratio_digits_url', 'ratio_digits_host',
                                'tld_in_path', 'tld_in_subdomain', 'abnormal_subdomain', 'nb_subdomains', 'prefix_suffix', 'shortening_service', 'shortest_words_raw',
                                'shortest_word_host', 'shortest_word_path', 'longest_words_raw', 'longest_word_host', 'longest_word_path', 'avg_words_raw', 'avg_word_host',
                                'avg_word_path', 'phish_hints', 'domain_in_brand', 'suspicious_tld', 'dns_record']

  df = pd.read_json(input_url_json)
  df = df[relevant_features_notnull]
  # sc = StandardScaler()
  # df = sc.fit_transform(df.T).T
  # # df = sc.fit_transform(df)
  # print(df)

  loaded_rf = joblib.load("rf_phishing_det_3.joblib")
  prediction = loaded_rf.predict(df)

  if prediction[0] == 1:
    print("Phishing")
  else:
    print("Legitimate")

  return prediction[0]
'''

############# Testing locally #############
# features_overall_list = []
# # Example of phishing
# features_overall_list = [{'url': 'http://shadetreetechnology.com/V4/validation/a111aedc8ae390eabcfa130e041a10a4', 'scheme': 'http', 'hostname': 'shadetreetechnology.com', 'path': '/V4/validation/a111aedc8ae390eabcfa130e041a10a4', 'netloc': 'shadetreetechnology.com', 'domain': 'shadetreetechnology', 'subdomains': [''], 'tld': 'com', 'length_url': 77, 'length_hostname': 23, 'ip': 1, 'path_extension': 0, 'nb_dots': 1, 'nb_hyphens': 0, 'nb_at': 0, 'nb_qm': 0, 'nb_and': 0, 'nb_or': 0, 'nb_eq': 0, 'nb_underscore': 0, 'nb_tilde': 0, 'nb_percent': 0, 'nb_slash': 3, 'nb_star': 0, 'nb_colon': 1, 'nb_comma': 0, 'nb_semicolumn': 0, 'nb_dollar': 0, 'nb_space': 0, 'nb_www': 0, 'nb_com': 0, 'nb_dslash': 0, 'nb_spl': 7, 'http_in_path': False, 'https_token': False, 'ratio_digits_url': 0.22077922077922077, 'ratio_digits_host': 0.0, 'punycode': False, 'port': False, 'tld_in_path': False, 'tld_in_subdomain': False, 'abnormal_subdomain': False, 'nb_subdomains': 1, 'prefix_suffix': False, 'random_domain': True, 'shortening_service': False, 'length_words_raw': 70, 'char_repeat': 0, 'shortest_words_raw': 2, 'shortest_word_host': 3, 'shortest_word_path': 2, 'longest_words_raw': 32, 'longest_word_host': 19, 'longest_word_path': 32, 'avg_words_raw': 11.666666666666666, 'avg_word_host': 11.0, 'avg_word_path': 14.666666666666666, 'phish_hints': 0, 'domain_in_brand': False, 'brand_in_subdomain': False, 'brand_in_path': False, 'suspicious_tld': False, 'nb_hyperlinks': 0, 'ratio_intHyperlinks': 0, 'ratio_extHyperlinks': 0, 'ratio_nullHyperlinks': 0, 'ratio_safe_anchors': 0, 'nb_extCSS': 0, 'onmouseover': False, 'right_click_disabled': False, 'empty_title': True, 'domain_in_title': False, 'domain_with_copyright': False, 'whois_registered_domain': False, 'domain_registration_length': 80, 'domain_age': 7238, 'web_traffic': 0, 'dns_record': False, 'google_index': 1, 'sfh': 0, 'iframe': False, 'popup_window': False, 'login_form': None, 'external_favicon': False, 'links_in_tags': 0, 'submit_email': False, 'ratio_intMedia': None, 'ratio_extMedia': None, 'index': 0}]

# # Example of legitimate
# features_overall_list = [{'url': 'http://www.crestonwood.com/router.php', 'scheme': 'http', 'hostname': 'www.crestonwood.com', 'path': '/router.php', 'netloc': 'www.crestonwood.com', 'domain': 'crestonwood', 'subdomains': ['www'], 'tld': 'com', 'length_url': 37, 'length_hostname': 19, 'ip': 0, 'path_extension': 1, 'nb_dots': 3, 'nb_hyphens': 0, 'nb_at': 0, 'nb_qm': 0, 'nb_and': 0, 'nb_or': 0, 'nb_eq': 0, 'nb_underscore': 0, 'nb_tilde': 0, 'nb_percent': 0, 'nb_slash': 1, 'nb_star': 0, 'nb_colon': 1, 'nb_comma': 0, 'nb_semicolumn': 0, 'nb_dollar': 0, 'nb_space': 0, 'nb_www': 1, 'nb_com': 0, 'nb_dslash': 0, 'nb_spl': 7, 'http_in_path': False, 'https_token': False, 'ratio_digits_url': 0.0, 'ratio_digits_host': 0.0, 'punycode': False, 'port': False, 'tld_in_path': False, 'tld_in_subdomain': False, 'abnormal_subdomain': False, 'nb_subdomains': 1, 'prefix_suffix': False, 'random_domain': True, 'shortening_service': False, 'length_words_raw': 30, 'char_repeat': 0, 'shortest_words_raw': 3, 'shortest_word_host': 3, 'shortest_word_path': 3, 'longest_words_raw': 11, 'longest_word_host': 11, 'longest_word_path': 6, 'avg_words_raw': 5.0, 'avg_word_host': 5.666666666666667, 'avg_word_path': 4.5, 'phish_hints': 0, 'domain_in_brand': False, 'brand_in_subdomain': False, 'brand_in_path': False, 'suspicious_tld': False, 'nb_hyperlinks': None, 'ratio_intHyperlinks': None, 'ratio_extHyperlinks': None, 'ratio_nullHyperlinks': None, 'ratio_safe_anchors': None, 'nb_extCSS': None, 'onmouseover': None, 'right_click_disabled': None, 'empty_title': None, 'domain_in_title': None, 'domain_with_copyright': None, 'whois_registered_domain': False, 'domain_registration_length': 36, 'domain_age': 5821, 'web_traffic': 0, 'dns_record': False, 'google_index': 1, 'sfh': None, 'iframe': None, 'popup_window': None, 'login_form': None, 'external_favicon': None, 'links_in_tags': None, 'submit_email': None, 'ratio_intMedia': None, 'ratio_extMedia': None, 'index': 0}]

# json_out = json.dumps(features_overall_list)
# input_url_json = json_out

############ Testing with external .py file ##############
# json_out = fe_single.final_features_extraction(input_url)

# check_phish_or_leg(json_out)
