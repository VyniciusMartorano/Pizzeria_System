"""
a ideia é adicionar todos os ids a uma lista 
e criar uma variavel com um len(lista).
no caso o id atual é a variavel + 1
"""
def atual_id():
    """
    A função verifica o ultimo id da base de dados do dia atual e soma + 1
    assim retornando o id atual do pedido
    :return: ID atual
    """
    last_day = getTime('d')
    last_mounth = verify_mounth(getTime('m'))
    user = getpass.getuser()

    conexao = sqlite3.connect(fr'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{last_mounth}\{last_day}\dados{last_day}.db')
    cursor = conexao.cursor()

    comand = 'SELECT * FROM clientes'
    cursor.execute(comand,)
    ids_list = []
    for item in cursor.fetchall():
        ids_list.append(item[0])
    if len(ids_list) > 0:
        last_id = ids_list[len(ids_list)-1]
        atual_id = last_id + 1
        cursor.close()
        conexao.close()
        if len(str(atual_id)) == 1:
            atual_id = f'0{atual_id}'
            return str(atual_id)
        return str(atual_id)
    elif len(ids_list) < 1:
        return '01'




