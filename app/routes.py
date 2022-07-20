from flask import request, jsonify
from app import app
from joblib import load

@app.route('/', methods=['GET'])
def apiOverview():
    return {
        'regresi': 'http://localhost:8080/regresi',
        'klasifikasi': 'http://localhost:8080/klasifikasi'
    }

@app.route('/regresi', methods=['POST'])
def regresi():
    # load regression model
    model = load('regresi_rige')
    
    # Take the data
    score_kpu = request.json['score_kpu']
    score_kua = request.json['score_kua']
    score_ppu = request.json['score_ppu']

    # Normalize the score

    # Predict the math score
    math_score = model.predict([score_kpu, score_kua, score_ppu])

    # Reverse the math score to 100 scale

    # Return the score
    return {'result': math_score}

@app.route('/klasifikasi', methods=['POST'])
def klasifikasi():
    # Load classification model
    model = load('klasifikasi_nn')

    # Take the data
    score_bio = request.json["score_bio"] 
    score_fis = request.json["score_fis"] 
    score_kim = request.json["score_kim"] 
    score_kmb = request.json["score_kmb"] 
    score_kpu = request.json["score_kpu"] 
    score_kua = request.json["score_kua"] 
    score_mat = request.json["score_mat"] 
    score_ppu = request.json["score_ppu"]

    # Normalize the score

    # Predict whether will pass or not
    isPass = model.predict([score_bio, score_fis, score_kim, score_kmb, score_kpu, score_kua, score_mat, score_ppu])

    # Return the result
    return {'result': isPass}