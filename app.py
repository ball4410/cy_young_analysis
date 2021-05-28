import numpy as np
from flask import Flask, render_template, request, jsonify, redirect
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from flask_pymongo import PyMongo

import scrape_espn

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
voting_df = pd.read_csv('./CyYoung_Voting.csv')

mongo = PyMongo(app, uri="mongodb://localhost:27017/cy_app")

@app.route("/")
def home():
    table_df = pd.read_csv("player_options.csv")
    table = table_df.to_html(classes="table table-striped table-sm")
    cy = mongo.db.cy.find_one()
    return render_template("index.html", cy=cy, data=table)

@app.route("/scrape")
def scrape():
    cy = mongo.db.cy
    espn_data = scrape_espn.scrape_all()
    cy.update({},espn_data, upsert=True)
    return redirect("/", code=302)

# @app.route('/dataset')    
# def another_page():    
#     table = pd.DataFrame.from_csv("player_options.csv")
#     return render_template("index.html", data=table.to_html)

@app.route("/predict", methods=["POST"])
def predict():
   
    if request.method == "POST":
        IP = float(request.form["IP"])
        ER = float(request.form["ER"])
        SO = float(request.form["SO"])
        SV = float(request.form["SV"])
        SHO = float(request.form["SHO"])
        W = float(request.form["W"])
        L = float(request.form["L"])

        row = [[IP, ER, SO, SV, SHO, W, L]]
        output = model.predict(row)

        classify = ""
        #y  # 1 apple 2 mandarin 3 orange 4 lemon
        if(output[0] == 1):
            classify = "Cy Young Competitor!"
        elif(output[0] == 0):
            classify = "Not Likely"
   
        return render_template("results.html", classify=classify)


if __name__ == '__main__':
    app.run(debug=True)