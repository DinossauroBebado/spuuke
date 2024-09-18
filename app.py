from flask import Flask, render_template, request, jsonify, session
import json

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessoes'

# Carregar os enigmas de um arquivo JSON
with open('enigmas.json', 'r', encoding='utf-8') as f:
    enigmas = json.load(f)

# Rota principal que renderiza a página do enigma
@app.route('/')
def index():
    return render_template('index.html')

# Rota para verificar a resposta e retornar o próximo enigma
@app.route('/verificar_resposta', methods=['POST'])
def verificar_resposta():
    username = request.json['username']
    resposta = request.json['resposta']
    
    if 'usuarios' not in session:
        session['usuarios'] = {}

    # Se o usuário é novo, inicialize o progresso
    if username not in session['usuarios']:
        session['usuarios'][username] = 0

    enigma_atual = session['usuarios'][username]

    if enigmas[enigma_atual]['resposta'].lower() == resposta.lower():
        enigma_atual += 1
        session['usuarios'][username] = enigma_atual
        if enigma_atual < len(enigmas):
            return jsonify({'correto': True, 'proximo_enigma': enigmas[enigma_atual]['enigma']})
        else:
            return jsonify({'correto': True, 'mensagem': 'Parabéns! Você resolveu todos os enigmas!'})
    else:
        return jsonify({'correto': False, 'mensagem': 'Resposta incorreta. Tente novamente.'})

# Rota para obter o enigma atual de acordo com o usuário
@app.route('/obter_enigma', methods=['POST'])
def obter_enigma():
    username = request.json['username']
    
    if 'usuarios' not in session:
        session['usuarios'] = {}

    # Se o usuário é novo, inicialize o progresso
    if username not in session['usuarios']:
        session['usuarios'][username] = 0

    enigma_atual = session['usuarios'][username]
    return jsonify({'enigma': enigmas[enigma_atual]['enigma']})

# Rota para exibir o progresso de todos os usuários
@app.route('/progresso')
def progresso():
    if 'usuarios' not in session:
        session['usuarios'] = {}

    usuarios = session['usuarios']

    # Para cada usuário, mostrar o enigma que ele está atualmente ou que resolveu todos.
    progresso_usuarios = {}
    for usuario, enigma_index in usuarios.items():
        if enigma_index < len(enigmas):
            progresso_usuarios[usuario] = f'Está no enigma {enigma_index + 1}: {enigmas[enigma_index]["enigma"]}'
        else:
            progresso_usuarios[usuario] = 'Completou todos os enigmas'

    return render_template('progresso.html', progresso_usuarios=progresso_usuarios)

if __name__ == '__main__':
    app.run(debug=True)
