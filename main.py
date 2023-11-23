from flask import Flask, jsonify, request
import oracledb
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)

# Configurações do banco de dados
db_user = os.environ.get("USER")
db_password = os.environ.get("PASS")
db_host = os.environ.get("HOST")
db_port = os.environ.get("PORT")
db_service = os.environ.get("SERVICE")

@app.route('/inserir_artigo', methods=['POST'])
def inserir_artigo():
    """
    Insere um novo artigo no banco de dados.

    Parâmetros:
    - nome (str): Nome do artigo.
    - descricao (str): Descrição do artigo.
    - data_publicacao (str): Data de publicação do artigo.
    - autor (str): Autor do artigo.
    - id_orgao_sistema (int): ID do órgão do sistema relacionado ao artigo.

    Retorna:
    - JSON: {'status': 'Artigo inserido com sucesso!'} se a operação for bem-sucedida,
             {'error': str} se ocorrer algum erro.
    """
    try:
        data = request.get_json()
        nome = data['nome']
        descricao = data['descricao']
        data_publicacao = data['data_publicacao']
        autor = data['autor']
        id_orgao_sistema = data['id_orgao_sistema']

        with oracledb.connect(user=db_user, password=db_password, dsn=f'{db_host}:{db_port}/{db_service}') as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO TB_ARTIGO (ID_ARTIGO, NOME, DESCRICAO, DATA_PUBLICACAO, AUTOR, ID_ORGAO_SISTEMA) VALUES (id_artigo_seq.NEXTVAL , :1, :2, :3, :4, :5)", [nome, descricao, data_publicacao, autor, id_orgao_sistema])
                connection.commit()

        return jsonify({'status': 'Artigo inserido com sucesso!'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/selecionar_artigos', methods=['GET'])
def selecionar_artigos():
    """
    Seleciona todos os artigos no banco de dados.

    Retorna:
    - JSON: Lista de dicionários representando os artigos se a operação for bem-sucedida,
             {'error': str} se ocorrer algum erro.
    """
    try:
        with oracledb.connect(user=db_user, password=db_password, dsn=f'{db_host}:{db_port}/{db_service}') as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TB_ARTIGO")
                result = cursor.fetchall()

        artigos = [{'id_artigo': row[0], 'nome': row[1], 'descricao': row[2], 'data_publicacao': row[3], 'autor': row[4], 'id_orgao_sistema': row[5]} for row in result]

        return jsonify(artigos)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/selecionar_artigo_id', methods=['GET'])
def selecionar_artigo_id():
    """
    Seleciona um artigo com base no ID fornecido.

    Parâmetros:
    - id_artigo (int): ID do artigo a ser recuperado.

    Retorna:
    - JSON: Dicionário representando o artigo se a operação for bem-sucedida,
             {'error': str} se ocorrer algum erro.
    """
    try:
        id_artigo = request.args.get('id_artigo')

        with oracledb.connect(user=db_user, password=db_password, dsn=f'{db_host}:{db_port}/{db_service}') as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM TB_ARTIGO WHERE ID_ARTIGO = {id_artigo}")
                row = cursor.fetchone()

        artigo = {'id_artigo': row[0], 'nome': row[1], 'descricao': row[2], 'data_publicacao': row[3], 'autor': row[4], 'id_orgao_sistema': row[5]}

        return jsonify(artigo)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/selecionar_orgao_sistema', methods=['GET'])
def selecionar_orgao_sistema():
    """
    Seleciona todos os órgãos do sistema no banco de dados.

    Retorna:
    - JSON: Lista de dicionários representando os órgãos do sistema se a operação for bem-sucedida,
             {'error': str} se ocorrer algum erro.
    """
    try:
        with oracledb.connect(user=db_user, password=db_password, dsn=f'{db_host}:{db_port}/{db_service}') as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TB_ORGAO_SISTEMA")
                result = cursor.fetchall()

        orgaos_sistema = [{'id_orgao_sistema': row[0], 'nome': row[1]} for row in result]

        return jsonify(orgaos_sistema)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/selecionar_orgao_sistema_id', methods=['GET'])
def selecionar_orgao_sistema_id():
    """
    Seleciona um órgão do sistema com base no ID fornecido.

    Parâmetros:
    - id_orgao_sistema (int): ID do órgão do sistema a ser recuperado.

    Retorna:
    - JSON: Dicionário representando o órgão do sistema se a operação for bem-sucedida,
             {'error': str} se ocorrer algum erro.
    """
    try:
        id_orgao_sistema = request.args.get('id_orgao_sistema')

        with oracledb.connect(user=db_user, password=db_password, dsn=f'{db_host}:{db_port}/{db_service}') as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM TB_ORGAO_SISTEMA WHERE ID_ORGAO_SISTEMA = '{id_orgao_sistema}'")
                row = cursor.fetchone()

        orgao_sistema = {'id_orgao_sistema': row[0], 'nome': row[1]}

        return jsonify(orgao_sistema)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
