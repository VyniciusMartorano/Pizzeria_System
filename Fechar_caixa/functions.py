import os
from mounth_verify import verify_mounth
import getpass
from get_time import getTime
import sqlite3


def get_values():
    """
    A função puxa do banco de dados do dia atual os valores para fechamento
    de caixa
    :return: dicionario com os valores de cada item
    """
    day = getTime('d')
    mounth = verify_mounth(getTime('m'))
    user = getpass.getuser()
    folder = fr'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{mounth}\{day}\dados{day}.db'
    if os.path.exists(folder) == False:
        return
    conection = sqlite3.connect(folder)
    cursor = conection.cursor()
    comand = 'SELECT forma_pagamento, valor_total FROM clientes'
    cursor.execute(comand,)
    pix = 0
    dinheiro = 0
    cartao = 0
    for item in cursor.fetchall():
        forma_pagamento, valor_total = item
        if forma_pagamento == 'PIX':
            pix += valor_total
        elif forma_pagamento == 'DINHEIRO':
            dinheiro += valor_total
        elif forma_pagamento == 'CARTÃO':
            cartao += valor_total
    final_key = {'pix':pix,'dinheiro':dinheiro,'cartao':cartao}
    return final_key

