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

# from alchemist.tools import formula_from_name, reaction_predictor

model = pickle.load(open('./models/model.p', 'rb'))
stoich_df = pd.read_csv('./data/processed/stoich_df.csv')
thermo_df = pd.read_csv('./data/processed/thermo_df.csv')


# create flask app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# secret key to perform certain actions
app.secret_key = 'sdfgsdgfdgfgfdgd'

# create index
@app.route('/')
def home():
    return render_template("index.html")

# team information page
@app.route('/transmuter/')
def team():

    return render_template("transmuter.html")





# prediction function for user input
def affluency_predictor(to_predict):

    # format the variable
    session_int = int(to_predict.strip())

    # .csv where features needed to model exist
    df = pd.read_csv("../data/Z_cluster.csv")

    # Pandas rearranges column order when saved to .csv so have to put the columns back in correct order
    df = df[['zip_code',
             'cluster_0',
             'cluster_1',
             'cluster_2',
             'cluster_3',
             'cluster_4',
             'cluster_5',
             'cluster_6',
             'cluster_7',
             'cluster_8',
             'cluster_9',
             'cluster_10',
             'cluster_11',
             'cluster_12',
             'cluster_13',
             'cluster_14',
             'cluster_15',
             'cluster_16',
             'cluster_17',
             'cluster_18',
             'cluster_19',
             'cluster_20',
             'cluster_21',
             'cluster_22',
             'cluster_23',
             'cluster_24',
             'cluster_25',
             'cluster_26',
             'cluster_27',
             'cluster_28',
             'cluster_29',
             'cluster_30',
             'cluster_31',
             'cluster_32',
             'cluster_33',
             'cluster_34',
             'cluster_35',
             'cluster_36',
             'cluster_37',
             'cluster_38',
             'cluster_39',
             'cluster_40',
             'cluster_41',
             'cluster_42',
             'cluster_43',
             'cluster_44',
             'cluster_45',
             'cluster_46',
             'cluster_47',
             'cluster_48',
             'cluster_49',
             'cluster_50',
             'cluster_51',
             'cluster_52',
             'cluster_53',
             'cluster_54',
             'cluster_55',
             'cluster_56',
             'cluster_57',
             'cluster_58',
             'cluster_59',
             'cluster_60',
             'cluster_61',
             'cluster_62',
             'cluster_63',
             'cluster_64',
             'cluster_65',
             'cluster_66',
             'cluster_67',
             'cluster_68',
             'cluster_69',
             'cluster_70',
             'cluster_71',
             'cluster_72',
             'cluster_73',
             'cluster_74',
             'cluster_75',
             'cluster_76',
             'cluster_77',
             'cluster_78',
             'cluster_79',
             'cluster_80',
             'cluster_81',
             'cluster_82',
             'cluster_83',
             'cluster_84',
             'cluster_85',
             'cluster_86',
             'cluster_87',
             'cluster_88',
             'cluster_89',
             'cluster_90',
             'cluster_91',
             'cluster_92',
             'cluster_93',
             'cluster_94',
             'cluster_95',
             'cluster_96',
             'cluster_97',
             'cluster_98',
             'cluster_99',
             'cluster_100',
             'cluster_101',
             'cluster_102',
             'cluster_103',
             'cluster_104',
             'cluster_105',
             'cluster_106',
             'cluster_107',
             'cluster_108',
             'cluster_109',
             'cluster_110',
             'cluster_111',
             'cluster_112',
             'cluster_113',
             'cluster_114',
             'cluster_115',
             'cluster_116',
             'cluster_117',
             'cluster_118',
             'cluster_119',
             'cluster_120',
             'cluster_121',
             'cluster_122',
             'cluster_123',
             'cluster_124',
             'cluster_125',
             'cluster_126',
             'cluster_127',
             'cluster_128',
             'cluster_129',
             'cluster_130',
             'cluster_131',
             'cluster_132',
             'cluster_133',
             'cluster_134',
             'cluster_135',
             'cluster_136',
             'cluster_137',
             'cluster_138',
             'cluster_139',
             'cluster_140',
             'cluster_141',
             'cluster_142',
             'cluster_143',
             'cluster_144',
             'cluster_145',
             'cluster_146',
             'cluster_147',
             'cluster_148',
             'cluster_149',
             'cluster_150',
             'cluster_151',
             'cluster_152',
             'cluster_153',
             'cluster_154',
             'cluster_155',
             'cluster_156',
             'cluster_157',
             'cluster_158',
             'cluster_159',
             'cluster_160',
             'cluster_161',
             'cluster_162',
             'cluster_163',
             'cluster_164',
             'cluster_165',
             'cluster_166',
             'cluster_167',
             'cluster_168',
             'cluster_169',
             'cluster_170',
             'cluster_171',
             'cluster_172',
             'cluster_173',
             'cluster_174',
             'cluster_175',
             'cluster_176',
             'cluster_177',
             'cluster_178',
             'cluster_179',
             'cluster_180',
             'cluster_181',
             'cluster_182',
             'cluster_183',
             'cluster_184',
             'cluster_185',
             'cluster_186',
             'cluster_187',
             'cluster_188',
             'cluster_189',
             'cluster_190',
             'cluster_191',
             'cluster_192',
             'cluster_193',
             'cluster_194',
             'cluster_195',
             'cluster_196',
             'cluster_197',
             'cluster_198',
             'cluster_199',
             'cluster_200',
             'cluster_201',
             'cluster_202',
             'cluster_203',
             'cluster_204',
             'cluster_205',
             'cluster_206',
             'cluster_207',
             'cluster_208',
             'cluster_209',
             'cluster_210',
             'cluster_211',
             'cluster_212',
             'cluster_213',
             'cluster_214',
             'cluster_215',
             'cluster_216',
             'cluster_217',
             'cluster_218',
             'cluster_219',
             'cluster_220',
             'cluster_221',
             'cluster_222',
             'cluster_223',
             'cluster_224',
             'cluster_225',
             'cluster_226',
             'cluster_227',
             'cluster_228',
             'cluster_229',
             'cluster_230',
             'cluster_231',
             'cluster_232',
             'cluster_233',
             'cluster_234',
             'cluster_235',
             'cluster_236',
             'cluster_237',
             'cluster_238',
             'cluster_239',
             'cluster_240',
             'cluster_241',
             'cluster_242',
             'cluster_243',
             'cluster_244',
             'cluster_245',
             'cluster_246',
             'cluster_247',
             'cluster_248',
             'cluster_249',
             'cluster_250',
             'cluster_251',
             'cluster_252',
             'cluster_253',
             'cluster_254',
             'cluster_255',
             'cluster_256',
             'cluster_257',
             'cluster_258',
             'cluster_259',
             'cluster_260',
             'cluster_261',
             'cluster_262',
             'cluster_263',
             'cluster_264',
             'cluster_265',
             'cluster_266',
             'cluster_267',
             'cluster_268',
             'cluster_269',
             'cluster_270',
             'cluster_271',
             'cluster_272',
             'cluster_273',
             'cluster_274',
             'cluster_275',
             'cluster_276',
             'cluster_277',
             'cluster_278',
             'cluster_279',
             'cluster_280',
             'cluster_281',
             'cluster_282',
             'cluster_283',
             'cluster_284',
             'cluster_285',
             'cluster_286',
             'cluster_287',
             'cluster_288',
             'cluster_289',
             'cluster_290',
             'cluster_291',
             'cluster_292',
             'cluster_293',
             'cluster_294',
             'cluster_295',
             'cluster_296',
             'cluster_297',
             'cluster_298',
             'cluster_299',
             'price',
             'review_count',
             'rating',
             'price_adj']]

    # create array from dataframe with user zipcode input
    predict_array = df[df['zip_code'] == session_int].drop(columns='zip_code', axis=1)
    print(predict_array)

    # load trained model from pickle
    loaded_model = pickle.load(open("model.p", "rb"))

    # predict on array
    result = loaded_model.predict(predict_array)
    print(result)
    print('------------')

    # create map of zipcode requested
    map_df = pd.read_csv('../data/data_zipcode.csv')
    la_coord = (34.0522, -118.2437)
    maps = folium.Map(location=la_coord, zoom_start=11)

    maps.save('./static/maps.html')

    for each in map_df.iterrows():
        if int(each[1]['zip_code']) == session_int:
            popup_text = folium.Html(f"""
                <strong>Zip Code: {each[1]["zip_code"].astype(int)}</strong>
                </br>Med. 2017 Household Income: ${each[1]["med_agi"].round(3)}
                </br>Predicted Median Income: ${result[0].round(2)}
                </br>Businesses Avg. $ Count: {each[1]["price"].round(3)}
                </br> Number of Businesses: {int(each[1]["count"])}""",
                script=True)

            popup = folium.Popup(popup_text, max_width=2650, show=True)

            coord = (each[1]['latitude'],each[1]['longitude'])

            maps = folium.Map(location=coord, zoom_start=13)


            folium.Marker(
                location = [each[1]['latitude'],each[1]['longitude']],
                popup=popup,
                clustered_marker = True).add_to(maps)

            maps.save('./static/maps.html')




    return result[0]



# process when a question gets submitted
@app.route('/transmuter')
def transmuter():

    if request.method == 'POST':

        # use CDE to translate names to formulas
        raw_input = request.form['rawtext']
        processed = cde.doc.Paragraph(raw_input)
        names = [cem.text for cem in processed.cems]
        formulas = [formula_from_name(n) for n in names]

        # apply all balancing algos
        reaction = reaction_predictor(formulas)

        return render_template("transmuter.html",reaction=reaction)





if __name__ == "__main__":
    app.run(debug=True)
