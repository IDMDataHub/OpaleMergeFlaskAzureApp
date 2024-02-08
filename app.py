#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 09:28:35 2022

@author: maximejacoupy
"""

# #######################################################################################################################
#                                              # === LIBRAIRIES === #
# #######################################################################################################################
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, send_file
import os
import io

app = Flask(__name__)

# #######################################################################################################################
#                                              # === FUNCTIONS === #
# #######################################################################################################################

def convert_df(df):
    """Convertit un DataFrame pandas en une chaîne d'octets encodée en utf-8 avec un séparateur de colonnes personnalisé.
    
    Parameters:
        df (pandas.DataFrame): Le DataFrame à convertir.
        
    Returns:
        bytes: La chaîne d'octets encodée en utf-8 représentant le DataFrame.
    """
    # Utilisation de ";" comme séparateur de colonnes personnalisé
    csv_data = df.to_csv(sep=';', index=False)

    # Encodage des données CSV en utf-8 pour éviter les erreurs liées aux caractères
    encoded_data = csv_data.encode('latin1')

    return encoded_data

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("csv_files[]")
    reference_block = int(request.form.get('reference_block'))

    # Move the reference block to the first position in the list
    uploaded_files.insert(0, uploaded_files.pop(reference_block - 1))

    # Initialisation du DataFrame de concaténation
    concat_df = None

    # Initialise une liste vide pour stocker les DataFrames
    dfs = []

    # Boucle sur chaque fichier téléchargé dans la liste 'uploaded_files'
    first_rows = []  # Ajoutez cette ligne
    for iCpt, uploaded_file in enumerate(uploaded_files):
        # Lit le fichier CSV et stocke le contenu dans un DataFrame
        df = pd.read_csv(uploaded_file, sep=';', encoding='latin1', engine='python')
        first_rows.append(df.head())

        # Vérifie si la colonne 'initiales_nom' existe dans le DataFrame
        if 'initiales_nom' in df.columns:
            # Si 'initiales_nom' existe, défini la colonne comme index et ajoute un préfixe à chaque nom de colonne
            df.set_index('initiales_nom')
            df = df.add_prefix(str(iCpt+1)+'_')

        # Vérifie si la colonne 'numero_patient' existe dans le DataFrame
        elif 'numero_patient' in df.columns:
            df.rename(columns = {'numero_patient':'initiales_nom'}, inplace = True)
            df.set_index('initiales_nom')
            df = df.add_prefix(str(iCpt+1)+'_')

        # Si la première colonne contient des nombres, appelle la colonne "initiales_nom" comme index et ajoute un préfixe à chaque nom de colonne
        elif pd.Series(df.iloc[1, 0]).dtype in (int, float):
            df = df.rename(columns={df.columns[0]: 'initiales_nom'})
            df.set_index('initiales_nom')
            df = df.add_prefix(str(iCpt+1)+'_')

        else:
            # Si 'initiales_nom' n'existe pas, combine les colonnes 'last_name' et 'first_name' pour créer la colonne 'initiales_nom'
            df.insert(0, 'initiales_nom', df['last_name'].astype(str) + df['first_name'].astype(str))
            df.set_index('initiales_nom')
            df = df.add_prefix(str(iCpt+1)+'_')

        # Affiche les 5 premières lignes du DataFrame
        print(f"File {iCpt+1}: {uploaded_file.filename}")
        print(df.head())

        # Stocke le DataFrame dans une variable globale avec un nom unique et ajoute le DataFrame à la liste 'dfs'
        globals()['df%s' % iCpt] = df
        dfs.append(globals()['df%s' % iCpt])

    # Fusionner les dataframes de la liste l horizontalement (en colonnes)
    concat_df = pd.concat(dfs, axis=1)
    # Renommer la première colonne en 'initiales_nom'
    concat_df.rename(columns={concat_df.columns[0]: 'initiales_nom'}, inplace=True)

    # Conversion du DataFrame fusionné en fichier CSV
    output = io.BytesIO()
    concat_df.to_csv(output, sep=';', index=False, encoding='latin1')
    output.seek(0)

    # Convert first_rows to HTML string
    first_rows_html = "<br>".join([f"<h4>File {i+1}: {uploaded_files[i].filename}</h4>{row.to_html()}" for i, row in enumerate(first_rows)])
    return send_file(output, download_name='merged_file.csv', as_attachment=True, mimetype='text/csv')

@app.route('/download', methods=['POST'])
def download_csv():
    csv_data = request.form.get("csv_data")
    output = io.BytesIO(csv_data.encode("latin1"))
    return send_file(output, download_name='merged_file.csv', as_attachment=True, mimetype='text/csv')
    # return send_file(output, download_name='merged_file.csv', as_attachment=True)






if __name__ == '__main__':
    app.run(debug=True)
