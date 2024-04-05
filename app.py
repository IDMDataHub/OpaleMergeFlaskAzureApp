# #######################################################################################################################
#                                              # === LIBRAIRIES === #
# #######################################################################################################################
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, send_file
import os
import io


#####################################################################
# =========================== CONSTANTES ========================== #
#####################################################################

app = Flask(__name__)


#####################################################################
# ==================== FONCTIONS D'ASSISTANCES ==================== #
#####################################################################

def convert_df(df):
    """
    Convertit un DataFrame pandas en une chaîne d'octets, en utilisant ";" comme séparateur de colonnes,
    et encode le résultat en latin1.

    Parameters:
    - df (pandas.DataFrame): Le DataFrame à convertir.

    Returns:
    - bytes: La chaîne d'octets résultante, encodée en latin1.
    """
    # Utilisation de ";" comme séparateur de colonnes personnalisé
    csv_data = df.to_csv(sep=';', index=False)

    # Encodage des données CSV en utf-8 pour éviter les erreurs liées aux caractères
    encoded_data = csv_data.encode('latin1')

    return encoded_data

@app.route('/', methods=['GET'])
def index():
    """
    Route principale qui affiche la page d'accueil.

    Returns:
    - str: Le contenu HTML de la page d'accueil.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """
    Traite le téléchargement de fichiers CSV, les trie selon l'ordre spécifié par l'utilisateur,
    fusionne les données et envoie le fichier CSV fusionné au client.

    Returns:
    - send_file: Un objet Flask `send_file` contenant le fichier CSV fusionné.
    """
    uploaded_files = request.files.getlist("csv_files[]")
    file_order = request.form.getlist("file_order[]")  # Récupérer l'ordre des fichiers

    # Créer un dictionnaire pour mapper le nom du fichier à son ordre
    file_order_dict = {file.filename: int(order) for file, order in zip(uploaded_files, file_order)}

    # Trier les fichiers téléchargés selon l'ordre spécifié
    uploaded_files.sort(key=lambda file: file_order_dict.get(file.filename, 999))

    # Suite du traitement
    dfs = []

    # Boucle sur chaque fichier téléchargé dans la liste 'uploaded_files'
    first_rows = []  # Ajoutez cette ligne
    for iCpt, uploaded_file in enumerate(uploaded_files):
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

        # # Affiche les 5 premières lignes du DataFrame
        print(f"File {iCpt+1}: {uploaded_file.filename}")
        print(df.head())

        # Stocke le DataFrame dans une variable globale avec un nom unique et ajoute le DataFrame à la liste 'dfs'
        globals()['df%s' % iCpt] = df
        dfs.append(globals()['df%s' % iCpt])

    # Fusionner les dataframes de la liste l horizontalement (en colonnes)
    concat_df = pd.concat(dfs, axis=1)
    concat_df.rename(columns={concat_df.columns[0]: 'initiales_nom'}, inplace=True)

    output = io.BytesIO()
    concat_df.to_csv(output, sep=';', index=False, encoding='latin1')
    output.seek(0)

    # Convert first_rows to HTML string
    return send_file(output, download_name='merged_file.csv', as_attachment=True, mimetype='text/csv')

@app.route('/download', methods=['POST'])
def download_csv():
    """
    Génère un fichier CSV à partir des données soumises et le retourne pour téléchargement.

    Returns:
    - send_file: Un objet Flask `send_file` contenant le fichier CSV généré.
    """
    csv_data = request.form.get("csv_data")
    output = io.BytesIO(csv_data.encode("latin1"))
    return send_file(output, download_name='merged_file.csv', as_attachment=True, mimetype='text/csv')


#####################################################################
# ====================== LANCEMENT DE L'ALGO ====================== #
#####################################################################

if __name__ == '__main__':
    """
    Point d'entrée principal pour l'application Flask. Exécute l'application en mode debug.
    """
    app.run(debug=True)
