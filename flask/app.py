import os
import pandas as pd # Para lidar com CSVs
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey' # MUDE ISSO EM PRODUÇÃO!

FILE_DIRECTORY = './app'

@app.route('/')
def index():
    try:
        items = os.listdir(FILE_DIRECTORY)
        csv_files = [item for item in items if item.endswith('.csv') and os.path.isfile(os.path.join(FILE_DIRECTORY, item))]
        other_files = [item for item in items if not item.endswith('.csv') and os.path.isfile(os.path.join(FILE_DIRECTORY, item))]
        directories = [item for item in items if os.path.isdir(os.path.join(FILE_DIRECTORY, item))]

        return render_template('index.html', csv_files=csv_files, other_files=other_files, directories=directories)
    except FileNotFoundError:
        return "Erro: O diretório configurado não foi encontrado no container. Verifique FILE_DIRECTORY."
    except Exception as e:
        return f"Erro inesperado: {e}"

@app.route('/edit_csv/<path:filename>')
def edit_csv(filename):
    filepath = os.path.join(FILE_DIRECTORY, filename)
    if not os.path.exists(filepath) or not filename.endswith('.csv'):
        flash(f"Arquivo '{filename}' não encontrado ou não é um CSV.")
        return redirect(url_for('index'))
    
    try:
        df = pd.read_csv(filepath)
        # Converte o DataFrame para um formato que possa ser facilmente renderizado no template
        headers = df.columns.tolist()
        data = df.values.tolist()
        return render_template('edit_csv.html', filename=filename, headers=headers, data=data)
    except Exception as e:
        flash(f"Erro ao carregar o CSV '{filename}': {e}")
        return redirect(url_for('index'))

@app.route('/save_csv/<path:filename>', methods=['POST'])
def save_csv(filename):
    filepath = os.path.join(FILE_DIRECTORY, filename)
    if not os.path.exists(filepath) or not filename.endswith('.csv'):
        return jsonify({"success": False, "message": "Arquivo não encontrado ou não é um CSV."}), 404

    try:
        # Pega os dados enviados via AJAX (JSON)
        edited_data = request.json['data'] # Espera um JSON com chave 'data' que é uma lista de listas
        headers = request.json['headers']

        # Cria um novo DataFrame a partir dos dados editados
        df_edited = pd.DataFrame(edited_data, columns=headers)
        
        # Salva o DataFrame de volta no arquivo CSV
        df_edited.to_csv(filepath, index=False)
        return jsonify({"success": True, "message": "CSV salvo com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao salvar o CSV: {e}"}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        return send_from_directory(FILE_DIRECTORY, filename, as_attachment=True)
    except FileNotFoundError:
        flash(f"Arquivo '{filename}' não encontrado.")
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Erro ao baixar o arquivo: {e}")
        return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Nenhum arquivo enviado.')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado.')
        return redirect(url_for('index'))
    if file:
        filepath = os.path.join(FILE_DIRECTORY, file.filename)
        try:
            file.save(filepath)
            flash(f"Arquivo '{file.filename}' enviado com sucesso!")
        except Exception as e:
            flash(f"Erro ao enviar o arquivo: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)