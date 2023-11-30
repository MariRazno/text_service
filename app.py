print('INFO: import modules')
import base64
from flask import Flask, request
import json
import pickle
import numpy as np
import os

from required_classes import *


CLS_WEIGHTS = {'mlp': 0.3, 'svc': 0.4, 'xgboost': 0.3}

print('INFO: loading models')
try:
    with open('embedder/embedder.pkl', 'rb') as f:
        embedder = pickle.load(f)
    print('INFO: embedder loaded')
except Exception as e:
    print(f"ERROR: loading embedder failed with: {str(e)}")

print('Loading classifiers of codes')
classifiers_codes = {}
try:
    for clf_name in os.listdir('classifiers/codes'):
        if '.' == clf_name[0]:
            continue
        with open('classifiers/codes/'+clf_name, 'rb') as f:
            model = pickle.load(f)
            classifiers_codes[clf_name.split('.')[0]] = model
        print(f'INFO: codes classifier {clf_name} loaded')
except Exception as e:
    print(f"ERROR: loading classifiers failed with: {str(e)}")

print('Loading classifiers of groups')
classifiers_groups = {}
try:
    for clf_name in os.listdir('classifiers/groups'):
        if '.' == clf_name[0]:
            continue
        with open('classifiers/groups/'+clf_name, 'rb') as f:
            model = pickle.load(f)
            classifiers_groups[clf_name.split('.')[0]] = model
        print(f'INFO: groups classifier {clf_name} loaded')
except Exception as e:
    print(f"ERROR: loading classifiers failed with: {str(e)}")

print('Loading classifiers in groups')
groups_models = {}
try:
    for clf_name in os.listdir('classifiers/codes_in_groups'):
        if '.' == clf_name[0]:
            continue
        with open('classifiers/codes_in_groups/'+clf_name, 'rb') as f:
            model = pickle.load(f)
            group_name = clf_name.replace('_code_clf.pkl', '')
            groups_models[group_name] = model
        print(f'INFO: codes classifier for group {group_name} loaded')
except Exception as e:
    print(f"ERROR: loading classifiers failed with: {str(e)}")


def classify_code(text, top_n):
    embed = [embedder(text)]
    preds = {}
    for clf_name in classifiers_codes.keys():
        model = classifiers_codes[clf_name]
        probs = model.predict_proba(embed)
        best_n = np.flip(np.argsort(probs, axis=1,)[0,-top_n:])
        clf_preds = {str(model.classes_[i]): float(probs[0][i]) for i in best_n}
        preds[clf_name] = clf_preds
    return preds


def classify_group(text, top_n):
    embed = [embedder(text)]
    preds = {}
    for clf_name in classifiers_groups.keys():
        model = classifiers_groups[clf_name]
        probs = model.predict_proba(embed)
        best_n = np.flip(np.argsort(probs, axis=1,)[0,-top_n:])
        clf_preds = {str(model.classes_[i]): float(probs[0][i]) for i in best_n}
        preds[clf_name] = clf_preds
    return preds

def classify_code_by_group(text, group_name, top_n):
    embed = [embedder(text)]
    model = groups_models[group_name]
    probs = model.predict_proba(embed)
    best_n = np.flip(np.argsort(probs, axis=1,)[0,-top_n:])

    top_n_preds = {str(model.classes_[i]): float(probs[0][i]) for i in best_n}
    top_cls = model.classes_[best_n[0]]
    all_codes_in_group = model.classes_
    return top_cls, top_n_preds, all_codes_in_group

def get_top_result(preds):
    total_scores = {}
    for clf_name, scores in preds.items():
        clf_name = clf_name.replace('_codes', '').replace('_groups', '')
        for class_name, score in scores.items():
            if class_name in total_scores:
                total_scores[class_name] += CLS_WEIGHTS[clf_name] * score
            else:
                total_scores[class_name] = CLS_WEIGHTS[clf_name] * score

    max_idx = np.array(total_scores.values()).argmax()
    if list(total_scores.values())[max_idx] > 0.5:
        return list(total_scores.keys())[max_idx]
    else:
        return None


app = Flask(__name__)

@app.get("/")
def test_get():
    return {'hello': 'world'}

@app.route("/test", methods=['POST'])
def test():
    data = request.json
    return {'response': data}

@app.route("/predict", methods=['POST'])
def predict_api():
    data = request.json
    base64_bytes = str(data['textB64']).encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    text = sample_string_bytes.decode("ascii")
    top_n = int(data['top_n'])

    if top_n < 1:
        return {'error': 'top_n should be geather than 0'}
    if text.strip() == '':
        return {'error': 'text is empty'}
    
    pred_codes = classify_code(text, top_n)
    pred_groups = classify_group(text, top_n)
    pred_codes_top = get_top_result(pred_codes)
    pred_groups_top = get_top_result(pred_groups)

    message_codes = 'models agree' if pred_codes_top is not None else 'models disagree'
    message_group = 'models agree' if pred_groups_top is not None else 'models disagree'
    result = {
        "icd10": 
            {'result': pred_codes_top, 'details': pred_codes, 'message': message_codes},
        "dx_group":
            {'result': pred_groups_top, 'details': pred_groups, 'message': message_group},
    }
    return result

@app.route("/predict_code", methods=['POST'])
def predict_code_api():
    data = request.json
    base64_bytes = str(data['textB64']).encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    text = sample_string_bytes.decode("ascii")
    top_n = int(data['top_n'])
    group_name = data['dx_group']

    if top_n < 1:
        return {'error': 'top_n should be geather than 0'}
    if text.strip() == '':
        return {'error': 'text is empty'}
    if group_name not in groups_models:
        return {'error': 'have no classifier for the group'}
    
    top_pred_code, pred_codes, all_codes_in_group = classify_code_by_group(text, group_name, top_n)
    result = {
        "icd10":
            {
                'result': top_pred_code, 
                'probability': pred_codes[top_pred_code], 
                'details': pred_codes, 
                'all_codes': all_codes_in_group
            }
    }
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
