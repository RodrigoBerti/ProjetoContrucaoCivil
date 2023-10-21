from urllib import request

import cv2  # Biblioteca OpenCV para processamento de imagem
import pytesseract  # Biblioteca para reconhecimento de texto em imagens
import requests.utils
from flask import render_template, Flask, request, redirect
import mysql.connector as connect, mysql

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='masterkey',
    database='projetoconstrucaocivil',
)

app = Flask(__name__)

materiais = []
# criando pagina
@app.route("/")
def homepage():
    material = get_material()
    return render_template("homepage.html", material=material, materiais=materiais)


@app.route("/login")
def login():
    return render_template('login.html')


def get_material():
    cursor = mydb.cursor()
    cursor.execute('select material.descricao from material')
    meus_materiais = cursor.fetchall()
    return meus_materiais

@app.route("/adicionar",methods=["POST"])
def adicionar_material():
    material= request.form.get('materiais')
    quantidade = request.form.get('quantidade')
    materiais.append(
        {'material':material, 'quantidade':quantidade}
    )
    return redirect("/")

@app.route('/atualizar/<int:index>', methods=['POST'])
def atualizar(index):
    quantidade = request.form.get('quantidade')
    materiais[index]['quantidade'] = quantidade
    return redirect('/')

@app.route('/excluir/<int:index>')
def excluir(index):
    materiais.pop(index)
    return redirect('/')


# 1. Ler a imagem
def ler_imagem(caminho_da_imagem):
    imagem = cv2.imread(caminho_da_imagem)
    return imagem


# oponter onde está o executavel do tesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


# 2. Pré-processamento da imagem (por exemplo, ajuste de brilho/contraste, redimensionamento, binarização)
def preprocessar_imagem(imagem):
    # Implemente aqui o pré-processamento necessário para melhorar a qualidade da imagem
    # Isso pode incluir ajustes de brilho/contraste, remoção de ruído, binarização, etc.
    imagem_processada = imagem
    return imagem_processada


# 3. Reconhecimento de texto na imagem
def extrair_informacoes(imagem_processada2):
    imagem_redimensionada = cv2.resize(imagem_processada2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    texto_extraido = pytesseract.image_to_string(imagem_redimensionada,
                                                 lang='por')  # Reconhecimento de texto em português
    print(texto_extraido)
    return texto_extraido


# 4. Analisar as informações extraídas e extrair as informações desejadas
def analisar_informacoes(texto):
    # Implemente aqui a lógica para extrair as informações específicas que você precisa
    # Isso pode envolver a pesquisa de palavras-chave, regex, análise de estrutura, etc.
    informacoes = {}
    # Exemplo: procurar por palavras-chave como "área", "materiais", "dimensões", etc.
    # e extrair os valores associados a essas palavras
    informacoes['area'] = encontrar_area(texto)
    informacoes['materiais'] = encontrar_materiais(texto)
    informacoes['dimensoes'] = encontrar_dimensoes(texto)
    return informacoes


# Funções de exemplo para encontrar informações específicas no texto
def encontrar_area(texto, area_encontrada=None):
    # Implemente a lógica para encontrar a área da planta
    # Exemplo: usar regex para encontrar números seguidos da palavra "m²"
    return area_encontrada


def encontrar_materiais(texto, materiais_encontrados=None):
    # Implemente a lógica para encontrar informações sobre materiais
    return materiais_encontrados


def encontrar_dimensoes(dimenssao, dimensoes_encontradas=None):
    # Implemente a lógica para encontrar informações sobre dimensões
    return dimensoes_encontradas


# 5. Exibir ou armazenar as informações extraídas
def mostrar_informacoes(informacoes):
    # Implemente aqui a forma como deseja exibir ou armazenar as informações
    print(informacoes)


if __name__ == "__main__":
    caminho_da_imagem = 'Design-sem-nome.png'
    imagem = ler_imagem(caminho_da_imagem)
    imagem_processada = preprocessar_imagem(imagem)
    texto_extraido = extrair_informacoes(imagem_processada)
    informacoes = analisar_informacoes(texto_extraido)
    app.run(host='localhost', debug=True)
