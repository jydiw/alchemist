from flask import Flask, render_template, request, g, session

import re
import json
import requests
import pickle
# import folium
import numpy as np
import pandas as pd
import chemdataextractor as cde
import pubchempy as pcp

from chempy import balance_stoichiometry
from chempy import Substance
from chempy import Reaction
from chempy.util import periodic

from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

from alchemist.tools import formula_from_name, reaction_predictor

MODELA = pickle.load(open('./data/processed/model_1324.p', 'rb'))
# MODELZ = pickle.load(open('./data/processed/model_z.p', 'rb'))
# stoich_df = pd.read_csv('/data/processed/stoich_df.csv')
# thermo_df = pd.read_csv('/data/processed/thermo_df.csv')


# create flask app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# secret key to perform certain actions
app.secret_key = 'sdfgsdgfdgfgfdgd'

# create index
@app.route('/')
def index():
    return render_template("index.html")

# team information page
# @app.route('/transmuter/')
# def transmuter():

#     return render_template("transmuter.html")


@app.route('/classifier', methods=["POST"])
# prediction function for user input
def classifier():

    if request.method == 'POST':
        bal = 0
        raw_input = request.form['class']
        bal += MODELA.wv.n_similarity(word_tokenize(raw_input), 
                                      word_tokenize('balanced equation'))
        bal -= MODELA.wv.n_similarity(word_tokenize(raw_input),
                                      word_tokenize('electron configuration'))
        if bal > 0:
            processed = cde.doc.Paragraph(raw_input)
            names = [cem.text for cem in processed.cems]
            formulas = [formula_from_name(n) for n in names]
            reaction = f'stoichiometry\n{formulas}'
        else:
            reaction = 'not stoichiometry'
        return render_template("index.html", reaction=reaction)



# predict the products of a chemical reaction
@app.route('/transmuter', methods=["POST"])
def transmuter():

    if request.method == 'POST':

        # use CDE to translate names to formulas
        raw_input = request.form['trans']
        processed = cde.doc.Paragraph(raw_input)
        names = [cem.text for cem in processed.cems]
        formulas = [formula_from_name(n) for n in names]

        # apply all balancing algos
        reaction = reaction_predictor(formulas)

        return render_template("index.html",reaction=reaction)





if __name__ == "__main__":
    app.run(debug=True)
