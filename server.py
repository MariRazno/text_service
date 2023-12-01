#!/usr/bin/env python3

# imports for momoware server
import os
import sys

import http.server
from http.server import BaseHTTPRequestHandler
import socketserver
import requests
import json
import html
from datetime import datetime

import momotools as momo
from momotools import logging
from momotools import data
logger = logging.Logger.getLogger()


# following code is based on corresponding code in app.py: 
# import modules, load models and define functions
# i.e. all code except starting flask and defining flask endpoints

# imports from icd10
print('INFO: import modules')
import base64
# not neededfrom flask import Flask, request
# already imported import json
import pickle
import numpy as np
# already imported import os

from required_classes import *

print("Here will be the code for processing.")
# CLS_WEIGHTS = {'mlp': 0.3, 'svc': 0.4, 'xgboost': 0.3}

# print('INFO: loading models')
# try:
#     with open('embedder/embedder.pkl', 'rb') as f:
#         embedder = pickle.load(f)
#     print('INFO: embedder loaded')
# except Exception as e:
#     print(f"ERROR: loading embedder failed with: {str(e)}")

# print('Loading classifiers of codes')
# classifiers_codes = {}
# try:
#     for clf_name in os.listdir('classifiers/codes'):
#         if '.' == clf_name[0]:
#             continue
#         with open('classifiers/codes/'+clf_name, 'rb') as f:
#             model = pickle.load(f)
#             classifiers_codes[clf_name.split('.')[0]] = model
#         print(f'INFO: codes classifier {clf_name} loaded')
# except Exception as e:
#     print(f"ERROR: loading classifiers failed with: {str(e)}")

# print('Loading classifiers of groups')
# classifiers_groups = {}
# try:
#     for clf_name in os.listdir('classifiers/groups'):
#         if '.' == clf_name[0]:
#             continue
#         with open('classifiers/groups/'+clf_name, 'rb') as f:
#             model = pickle.load(f)
#             classifiers_groups[clf_name.split('.')[0]] = model
#         print(f'INFO: groups classifier {clf_name} loaded')
# except Exception as e:
#     print(f"ERROR: loading classifiers failed with: {str(e)}")

# print('Loading classifiers in groups')
# groups_models = {}
# try:
#     for clf_name in os.listdir('classifiers/codes_in_groups'):
#         if '.' == clf_name[0]:
#             continue
#         with open('classifiers/codes_in_groups/'+clf_name, 'rb') as f:
#             model = pickle.load(f)
#             group_name = clf_name.replace('_code_clf.pkl', '')
#             groups_models[group_name] = model
#         print(f'INFO: codes classifier for group {group_name} loaded')
# except Exception as e:
#     print(f"ERROR: loading classifiers failed with: {str(e)}")


# def classify_code(text, top_n):
#     embed = [embedder(text)]
#     preds = {}
#     for clf_name in classifiers_codes.keys():
#         model = classifiers_codes[clf_name]
#         probs = model.predict_proba(embed)
#         best_n = np.flip(np.argsort(probs, axis=1,)[0,-top_n:])
#         clf_preds = {str(model.classes_[i]): float(probs[0][i]) for i in best_n}
#         preds[clf_name] = clf_preds
#     return preds


# def classify_group(text, top_n):
#     embed = [embedder(text)]
#     preds = {}
#     for clf_name in classifiers_groups.keys():
#         model = classifiers_groups[clf_name]
#         probs = model.predict_proba(embed)
#         best_n = np.flip(np.argsort(probs, axis=1,)[0,-top_n:])
#         clf_preds = {str(model.classes_[i]): float(probs[0][i]) for i in best_n}
#         preds[clf_name] = clf_preds
#     return preds

# def classify_code_by_group(text, group_name, top_n):
#     embed = [embedder(text)]
#     model = groups_models[group_name]
#     probs = model.predict_proba(embed)
#     best_n = np.flip(np.argsort(probs, axis=1,)[0,-top_n:])

#     top_n_preds = {str(model.classes_[i]): float(probs[0][i]) for i in best_n}
#     top_cls = model.classes_[best_n[0]]
#     all_codes_in_group = model.classes_
#     return top_cls, top_n_preds, all_codes_in_group

# def get_top_result(preds):
#     total_scores = {}
#     for clf_name, scores in preds.items():
#         clf_name = clf_name.replace('_codes', '').replace('_groups', '')
#         for class_name, score in scores.items():
#             if class_name in total_scores:
#                 total_scores[class_name] += CLS_WEIGHTS[clf_name] * score
#             else:
#                 total_scores[class_name] = CLS_WEIGHTS[clf_name] * score

#     max_idx = np.array(total_scores.values()).argmax()
#     if list(total_scores.values())[max_idx] > 0.5:
#         return list(total_scores.keys())[max_idx]
#     else:
#         return None









# based on momoware server.py: start a http server
#
HOSTNAME = 'localhost'
PORTNO = 8090

class PredictServer(BaseHTTPRequestHandler):

  khiz2id = {}   # map KHIZ on mongo-DB key


  def respond200(self, response_as_string):
    # send response
    self.send_response(200);
    self.send_header('Content-type', 'text')
    self.end_headers()
    self.wfile.write(bytes(response_as_string, "UTF-8"))

  def do_GET(self):
    self.send_response(400)
    self.send_header('Content-type', 'text')
    self.end_headers()
    self.wfile.write(bytes("Kein get moeglich, nur POST", "UTF-8"))
    return

  def do_POST(self):

    print("received request url:" + self.path);
    body_as_string = ''
    url = str(self.path)

    try :

      # read body that is assumed to be base64encoded into text (body_as_sring)
      # and if possible into Dict (requestAsDict)
      content_length = int(self.headers.get('content-length', 0))
      logger.debug("content length:" + str(content_length));
      body = self.rfile.read(content_length)
      body_as_string = body.decode()  # from bytes[] to string ???
      body_as_string = data.atob(body_as_string, "request")
      if len(body_as_string)>0:
        requestAsDict = json.loads(body_as_string)

      # call the handler as defined by the url
      response_as_string = None

      if self.path == "/hello":
        response_as_string = "Hallo aus Microservice helloworld_python um " + str(datetime.now())
        self.respond200(data.btoa(response_as_string, "response"))

      elif self.path == "/echo":
        response = {
          "msg" : "Echo aus Microservice helloworld_python um " + str(datetime.now()),
          "echo" : requestAsDict
        }
        response_as_string =  json.dumps(response)
        response_as_string =  data.btoa(response_as_string, "response")
        self.respond200(response_as_string)
      elif self.path == "/predict":
        #   # this endpoint adapted from icd10/app.py
        #   top_n = requestAsDict['top_n']
        #   text = requestAsDict['text']
        #   if top_n < 1:
        #     return {'error': 'top_n should be geather than 0'}
        #   if text.strip() == '':
        #       return {'error': 'text is empty'}
          
        #   pred_codes = classify_code(text, top_n)
        #   pred_groups = classify_group(text, top_n)
        #   pred_codes_top = get_top_result(pred_codes)
        #   pred_groups_top = get_top_result(pred_groups)
      
        #   message_codes = 'models agree' if pred_codes_top is not None else 'models disagree'
        #   message_group = 'models agree' if pred_groups_top is not None else 'models disagree'
        #   result = {
        #       "icd10": 
        #           {'result': pred_codes_top, 'details': pred_codes, 'message': message_codes},
        #       "dx_group":
        #           {'result': pred_groups_top, 'details': pred_groups, 'message': message_group},
        #   }
          result = {
              "model": 
                  {'result': 0, 'details': 0, 'message': 'testing works'}
            }
          response_as_string =  json.dumps(result)
          response_as_string =  data.btoa(response_as_string, "response")
          self.respond200(response_as_string)
    
      elif self.path == "/predict_group":
        raise Exception("not implemented yet: " + self.path );

      else : # type(response_as_string) == type(None):
        raise Exception("no such url: " + self.path );

    except Exception as e:

      logger.errorTime_(str(e), -2);
      logger.flush()
      self.send_response(400)
      self.send_header('Content-type', 'text')
      self.end_headers()
      self.wfile.write(bytes(str(e), "UTF-8"))
      self.wfile.write(bytes("<pre> request as text: " + str(body_as_string), "UTF-8"))

    return

if __name__ == '__main__':

  # init: set portno if given (otherwise default = 8090
  if len(sys.argv) == 2:
    PORTNO = int(sys.argv[1])

  Handler = PredictServer # http.server.SimpleHTTPRequestHandler
  httpd = socketserver.TCPServer((HOSTNAME, PORTNO), Handler)
  print("start server at port: " + str(PORTNO))
  httpd.serve_forever()
