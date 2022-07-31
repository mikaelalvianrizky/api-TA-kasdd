from flask import request
from app import app
from joblib import load

from .pass_grade.pg22 import passing_grade

from .pass_grade.bio_pass import bio_grade
from .pass_grade.fis_pass import fis_grade
from .pass_grade.kim_pass import kim_grade
from .pass_grade.mat_pass import mat_grade

from .pass_grade.kmb_pass import kmb_grade
from .pass_grade.kpu_pass import kpu_grade
from .pass_grade.kua_pass import kua_grade
from .pass_grade.ppu_pass import ppu_grade

@app.route('/', methods=['GET'])
def apiOverview():
    return {
        'regresi': 'http://localhost:5000/regresi',
        'klasifikasi': 'http://localhost:5000/klasifikasi'
    }

@app.route('/regresi', methods=['POST'])
def regresi():
    # load regression model
    model = load('./app/regresi_ridge')
    
    # Minimum score
    score_min_kpu=193
    score_min_kua=266
    score_min_mat=219
    score_min_ppu=204

    # Maximum score
    score_max_kpu=881
    score_max_kua=922
    score_max_mat=1123
    score_max_ppu=843

    # Take the data
    score_kpu = request.json['score_kpu']
    score_kua = request.json['score_kua']
    score_ppu = request.json['score_ppu']

    # Normalize the score
    score_kpu = (score_kpu-score_min_kpu)/(score_max_kpu-score_min_kpu)
    score_kua = (score_kua-score_min_kua)/(score_max_kua-score_min_kua)
    score_ppu = (score_ppu-score_min_ppu)/(score_max_ppu-score_min_ppu)

    # Predict the math score
    math_score = model.predict([[score_kpu, score_kua, score_ppu]])

    # Reverse the math score to 100 scale
    math_score = math_score * (score_max_mat-score_min_mat) + score_min_mat
    print(math_score[0])
    # Return the score
    return {'result': math_score[0]}

@app.route('/klasifikasi', methods=['POST'])
def klasifikasi():
    # Get the id_prodi
    id_prodi = request.json["id_prodi"]
    notPass = False

    if request.json["score_bio"] < bio_grade[id_prodi]:
        return {'result': str(notPass)}
    if request.json["score_fis"] < fis_grade[id_prodi]:
        return {'result': str(notPass)}
    if request.json["score_kim"] < kim_grade[id_prodi]:
        return {'result': str(notPass)}
    if request.json["score_mat"] < mat_grade[id_prodi]:
        return {'result': str(notPass)}
    if request.json["score_kmb"] < kmb_grade[id_prodi]:
        return {'result': str(notPass)}
    if request.json["score_kpu"] < kpu_grade[id_prodi]:
        return {'result': str(notPass)}
    if request.json["score_ppu"] < ppu_grade[id_prodi]:
        return {'result': str(notPass)}
    if request.json["score_kua"] < kua_grade[id_prodi]:
        return {'result': str(notPass)}

    # Take the data
    sum_score += request.json["score_bio"] 
    sum_score += request.json["score_fis"] 
    sum_score += request.json["score_kim"] 
    sum_score += request.json["score_kmb"] 
    sum_score += request.json["score_kpu"] 
    sum_score += request.json["score_kua"] 
    sum_score += request.json["score_mat"] 
    sum_score += request.json["score_ppu"]

    # Get the average score
    avg_score = (sum_score)/8

    # Mapping the id_prodi into passing_grade
    pg22 = passing_grade[id_prodi]
    
    if avg_score < pg22: 
        return {'result': str(notPass)}

    # Lulus
    return {'result': str(not notPass)}