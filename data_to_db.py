# -*- coding: utf-8 -*- 

import pandas as pd
import sqlite3
import psycopg2
import csv

# 데이터 가져오기 !
df = pd.read_csv("./gender.csv")

# 데이터 저장 !
host="castor.db.elephantsql.com"
database="lxwwlwnu"
user="lxwwlwnu"
password="U0divJFJXpZ-4lXmPi_UPKgNTFruhvDs"

conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS gender;")

cursor.execute("""CREATE TABLE gender
(
                "Id" INT,
                "long_hair" INT,
                "forehead_width_cm" FLOAT,
                "forehead_height_cm" FLOAT,
                "nose_wide"	INT,
                "nose_long"	INT,
                "lips_thin" INT,
                "distance_nose_to_lip_long" INT,
                "gender" VARCHAR(12)
);
""")

## CREATE NEW CSV WITH INDEX COLUMN
df.to_csv('./new_gender.csv')

## COPY ALL VALUES FROM NEW CSV INTO MY DB TABLE
with open ('./new_gender.csv', 'r') as f:
    next(f)
    cursor.copy_from(f, 'gender', sep=',')


conn.commit()