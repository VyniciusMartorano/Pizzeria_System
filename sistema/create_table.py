import getpass
from sistema.getTime import getTime
from sistema.mounth_verify import verify_mounth
import sqlite3

def create_table():
    """
    Cria a tabela no local original dela, que serve como base para
    fazer multiplas copias para suas respectivas pastas
    :return:
    """
    user = getpass.getuser()
    last_day = getTime('d')
    last_mounth = verify_mounth(getTime('m'))

    conexao = sqlite3.connect(
        fr'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\original_file\tabela.db')
    cursor = conexao.cursor()
    comand = 'CREATE TABLE IF NOT EXISTS clientes (' \
             'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
             'nome TEXT,' \
             'telefone TEXT,' \
             'hora TEXT,' \
             'entrega TEXT,' \
             'forma_pagamento TEXT,' \
             'valor_total REAL' \
             ')'
    cursor.execute(comand,)
    conexao.commit()
    cursor.close()
    conexao.close()
