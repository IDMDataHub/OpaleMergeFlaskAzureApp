#####################################################################
# =========================== LIBRAIRIES ========================== #
#####################################################################

import pandas as pd
import numpy as np
from flask import Flask, render_template, request, send_file
import os
import io


#####################################################################
# ========================= GENERAL INFO ========================== #
#####################################################################

app = Flask(__name__)


#####################################################################
# ===================== ASSISTANCE FUNCTIONS ====================== #
#####################################################################

def convert_df(df):
    """
    Converts a pandas DataFrame to a byte string, using ";" as the column separator,
    and encodes the result in Latin1.

    Parameters:
    - df (pandas.DataFrame): The DataFrame to convert.

    Returns:
    - bytes: The resulting byte string, encoded in Latin1.
    """
    # Use ";" as a custom column separator
    csv_data = df.to_csv(sep=';', index=False)

    # Encoding the CSV data to Latin1 to ensure compatibility with systems that require this encoding
    encoded_data = csv_data.encode('latin1')

    return encoded_data

@app.route('/', methods=['GET'])
def index():
    """
    Main route that displays the homepage.

    Returns:
    - str: The HTML content of the homepage.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """
    Processes the upload of CSV files, sorts them according to the user-specified order,
    merges the data, and sends the merged CSV file back to the client.

    Returns:
    - send_file: A Flask `send_file` object containing the merged CSV file.
    """
    uploaded_files = request.files.getlist("csv_files[]")
    file_order = request.form.getlist("file_order[]")  # Retrieve the file order

    # Create a dictionary to map file name to its order
    file_order_dict = {file.filename: int(order) for file, order in zip(uploaded_files, file_order)}

    # Sort the uploaded files according to the specified order
    uploaded_files.sort(key=lambda file: file_order_dict.get(file.filename, 999))

    dfs = []  # List to hold dataframes for merging

    # Loop through each uploaded file in the 'uploaded_files' list
    first_rows = []  # Add this line
    for iCpt, uploaded_file in enumerate(uploaded_files):
        # Read the CSV file using pandas, specifying the ';' separator and 'latin1' encoding
        df = pd.read_csv(uploaded_file, sep=';', encoding='latin1', engine='python')
        first_rows.append(df.head())

        # Check if the 'initiales_nom' column exists in the DataFrame
        if 'initiales_nom' in df.columns:
            # If 'initiales_nom' exists, set the column as index and add a prefix to each column name
            df.set_index('initiales_nom')
            df = df.add_prefix(str(iCpt+1)+'_')

        # Check if the 'numero_patient' column exists in the DataFrame
        elif 'numero_patient' in df.columns:
            df.rename(columns = {'numero_patient':'initiales_nom'}, inplace = True)
            df.set_index('initiales_nom')
            df = df.add_prefix(str(iCpt+1)+'_')

        # If the first column contains numbers, set the column "initiales_nom" as index and add a prefix to each column name
        elif pd.Series(df.iloc[1, 0]).dtype in (int, float):
            df = df.rename(columns={df.columns[0]: 'initiales_nom'})
            df.set_index('initiales_nom')
            df = df.add_prefix(str(iCpt+1)+'_')

        else:
            # If 'initiales_nom' does not exist, combine the 'last_name' and 'first_name' columns to create the 'initiales_nom' column
            df.insert(0, 'initiales_nom', df['last_name'].astype(str) + df['first_name'].astype(str))
            df.set_index('initiales_nom')
            df = df.add_prefix(str(iCpt+1)+'_')

        # Print the first 5 rows of the DataFrame
        print(f"File {iCpt+1}: {uploaded_file.filename}")
        print(df.head())

        # Store the DataFrame in a global variable with a unique name and append the DataFrame to the 'dfs' list
        globals()['df%s' % iCpt] = df
        dfs.append(globals()['df%s' % iCpt])

    # Merge the DataFrames from the list horizontally (in columns)
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
# ========================== ALGO LAUNCH ========================== #
#####################################################################

if __name__ == '__main__':
    """
    Main entry point for the Flask application. Runs the application in debug mode.
    """
    app.run(debug=True)
