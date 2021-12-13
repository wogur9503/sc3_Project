import os
import json
import csv
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def get():
    return render_template('home.html')

@app.route('/getReport', methods=["POST"])
def report():
    import pandas as pd
    import numpy as np
    from sklearn.svm import SVC
    from category_encoders import OrdinalEncoder
    from sklearn.pipeline import make_pipeline, Pipeline
    from sklearn.model_selection import train_test_split
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import LabelEncoder
    df = pd.read_csv('new_gender.csv')

    features = ['long_hair','forehead_width_cm', 'forehead_height_cm', 'nose_wide',	'nose_long', 'lips_thin', 'distance_nose_to_lip_long']
    target = ['gender']

    # 라벨 인코딩
    label = LabelEncoder()
    df['gender'] = label.fit_transform(df['gender'])

    print(df['gender'], type(df['gender']))
    print(label.classes_)

    # 데이터 분할
    train, test = train_test_split(df, train_size=0.80, test_size=0.20, 
                                    stratify=df[target], random_state=2)

    train, val = train_test_split(train, train_size=0.80, test_size=0.20, 
                                    stratify=train[target], random_state=2) 

    X_train = train[features]
    y_train = train[target]
    X_val = val[features]
    y_val = val[target]
    X_test = test[features]
    y_test = test[target]

    # 파이프 라인
    pipe = Pipeline([
        ('preprocessing', make_pipeline(OrdinalEncoder(), SimpleImputer(strategy='most_frequent'))),
        ('svc', SVC(kernel='rbf', C = 10, gamma = 0.1)) 
    ])

    pipe.fit(X_train, y_train);

    #값 호출하기
    LH = request.form.get('long_hair')
    FWC = request.form.get('forehead_width_cm')
    FHC = request.form.get('forehead_height_cm')
    NW = request.form.get('nose_wide')
    NL = request.form.get('nose_long')
    LT = request.form.get('lips_thin')
    IJ = request.form.get('distance_nose_to_lip_long')
    print("#########################################")
    print("#########################################")
    print("#########################################")
    print(LH, FWC, FHC, NW, NL, LT, IJ)
    print("#########################################")
    print("#########################################")
    print("#########################################")
    final_ft = pd.DataFrame({"long_hair":[LH], "forehead_width_cm":[FWC], "forehead_height_cm":[FHC], "nose_wide":[NW], "nose_long":[NL], "lips_thin":[LT], "distance_nose_to_lip_long":[IJ]})

    y_pred = pipe.predict(final_ft)
    gender = "a"
    if y_pred == 1:
        gender = "Male"
    elif y_pred == 0:
        gender = "Female"
    else:
        gender = "오류"
        
    # return render_template('report.html', gender=gender)
    return jsonify(gender)  

if __name__ == '__main__':
    app.run(debug=True)

