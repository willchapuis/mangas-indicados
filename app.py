from flask import Flask, render_template, request, redirect, url_for
import os
import json
from openpyxl import load_workbook
from rapidfuzz import fuzz
from werkzeug.utils import secure_filename

app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)
app.config['UPLOAD_FOLDER'] = 'uploads'

DADOS_PATH = "data/obras.json"

# Carrega ou inicia os dados (dicionário simples)
def carregar_dados():
    if not os.path.exists(DADOS_PATH):
        with open(DADOS_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
    try:
        with open(DADOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(DADOS_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return {}

def salvar_dados(dados):
    with open(DADOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# Normaliza nomes para comparação
def normalizar_nome(nome):
    nome = nome.lower().strip()
    nome = nome.replace("***", "").replace("...", "").replace("---", "")
    nome = nome.replace("?", "").replace("!", "").replace(",", "")
    nome = nome.replace("99+", "+99")  # exemplo específico
    nome = ' '.join(nome.split())  # remove espaços duplos
    return nome

# Adiciona nova indicação (lista de nomes)
def adicionar_indicacao(nomes, dados):
    for nome in nomes:
        nome_original = nome.strip()
        if not nome_original:
            continue
        nome_limpo = normalizar_nome(nome_original)

        similar = None
        for existente in dados:
            if fuzz.ratio(nome_limpo, normalizar_nome(existente)) >= 90:
                similar = existente
                break

        if similar:
            dados[similar]['indicacoes'] += 1
        else:
            dados[nome_original] = {
                'indicacoes': 1,
                'status': 'nao_lido'
            }
    salvar_dados(dados)

# Rota principal
@app.route('/')
def index():
    dados = carregar_dados()
    obras = sorted(dados.items(), key=lambda x: -x[1]['indicacoes'])
    return render_template('index.html', obras=obras)

# Upload de .xlsx
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx'):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            wb = load_workbook(path)
            ws = wb.active

            nomes = []
            for row in ws.iter_rows(min_col=1, max_col=1, values_only=True):
                valor = row[0]
                if valor is None:
                    if nomes:
                        adicionar_indicacao(nomes, carregar_dados())
                        nomes = []
                else:
                    nomes.append(str(valor))

            if nomes:
                adicionar_indicacao(nomes, carregar_dados())

            return redirect(url_for('index'))
    return render_template('upload.html')

# Adição manual
@app.route('/adicionar', methods=['POST'])
def adicionar():
    texto = request.form.get('novas_obras', '')
    nomes = texto.strip().splitlines()
    adicionar_indicacao(nomes, carregar_dados())
    return redirect(url_for('index'))

# Atualiza status
@app.route('/atualizar_status/<obra>/<novo_status>', methods=['POST'])
def atualizar_status(obra, novo_status):
    dados = carregar_dados()
    if obra in dados:
        dados[obra]['status'] = novo_status
        salvar_dados(dados)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
