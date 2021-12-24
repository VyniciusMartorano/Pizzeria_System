from sistema.getTime import getTime
from sistema.mounth_verify import verify_mounth
import getpass
import sqlite3

def write_in_table(nome,telefone,hora,entrega,forma_pagamento,valor_total):
    """
    The function 'write_in_table' escreve os dados na base de dados
    :param nome: str
    :param telefone: str
    :param hora: str
    :param entrega: str
    :param forma_pagamento: str
    :param valor_total:
    :return: ...
    """
    #variaveis
    last_day = getTime('d')
    last_mounth = verify_mounth(getTime('m'))
    user = getpass.getuser()

    #start of conection
    conexao = sqlite3.connect(fr'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{last_mounth}\{last_day}\dados{last_day}.db')
    cursor = conexao.cursor()

    comand = f'INSERT INTO clientes (nome,telefone,hora,entrega,forma_pagamento,valor_total) VALUES (?,?,?,?,?,?)'
    cursor.execute(comand,(nome,telefone,hora,entrega,forma_pagamento,valor_total))
    conexao.commit()
    #fim da conexão
    cursor.close()
    conexao.close()
