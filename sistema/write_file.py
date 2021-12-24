import os
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas

"""
PDF de entrega concluido
Fazer manutenção no pdf das pizzas
"""

def cria_pdf_entrega(id,hora,nome,local,telefone,endereco,n_casa,p_referencia,troco,valor_total,forma_pagamento,refri_list):
    """
    :param id: str
    :param hora: str
    :param nome: str
    :param local: str
    :param telefone: str
    :param endereco: str
    :param n_casa: str
    :param p_referencia: str
    :param troco: str
    :param valor_total: str
    :param forma_pagamento: str
    :return: pdf file in day and mounth folder
    """
    from sistema.mounth_verify import verify_mounth
    from sistema.getTime import getTime
    last_mounth = verify_mounth(getTime('m'))
    last_day = getTime('d')
    if '_' in local:
        local = local.replace('_', ' ')
    if troco == '':
        troco = 'R$ 0.00'
    try:
        import getpass
        user = getpass.getuser()
        pasta_app = os.path.dirname(fr"C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Entregas\{last_mounth}\{last_day}\\")
        # Canvas recebe os argumentos:
        # pasta onde vai ser criado o arquivo e tamanho do arquivo
        cvn = canvas.Canvas(pasta_app + f'\comanda_entrega{id}.pdf', pagesize=A6)
        # drawString recebe as posições X e Y e a string
        cvn.setFont('Times-Bold', 23)
        cvn.drawString(10, 390, f'ID: {id:<10}HORA: {hora}')
        cvn.setFont('Times-Bold', 19)
        cvn.drawString(10, 370, f'Nome:')
        cvn.setFont('Times-Roman', 19)
        cvn.drawString(10, 350, f'{nome:<30}')
        cvn.setFont('Times-Bold', 19)
        cvn.drawString(10, 325, f'Contato:')
        cvn.setFont('Times-Roman', 19)
        cvn.drawString(10, 305, f'{telefone:<30}')
        cvn.setFont('Times-Bold', 19)
        cvn.drawString(10, 280, f'Bairro:')
        cvn.setFont('Times-Roman', 17)
        cvn.drawString(10, 260, f'{local:<30}')
        cvn.setFont('Times-Bold', 19)
        cvn.drawString(10, 240, f'Endereço:')
        cvn.setFont('Times-Roman', 17)
        cvn.drawString(10, 220, f'{endereco}, {n_casa}')
        cvn.setFont('Times-Bold', 19)
        cvn.drawString(10, 200, f'Ponto de referência:')
        cvn.setFont('Times-Roman', 16)
        cvn.drawString(10, 180, f'{p_referencia}')
        cvn.setFont('Times-Bold', 19)
        cvn.drawString(10, 150, f'Forma de pagamento:')
        cvn.setFont('Times-Roman', 17)
        cvn.drawString(10, 130, f'{forma_pagamento}')
        cvn.setFont('Times-Bold', 19)
        cvn.drawString(10,110,'Refrigerante(s):')
        cvn.setFont('Times-Bold', 11)
        cont1 = 0
        lista = []
        if len(refri_list) >= 1:
            for item in refri_list:
                split = item.split()
                if '_' in split[0]:
                    x = split[0].replace('_',' ')
                    split[0] = x
                item = f'0{split[1]} {split[0]}'
                lista.append(item)
            if len(lista) == 1:
                cvn.drawString(10, 90, f'{lista[0]}')
            if len(lista) == 2:
                cvn.drawString(10, 90, f'{lista[0]} - {lista[1]}')
            if len(lista) == 3:
                cvn.drawString(10, 90, f'{lista[0]} - {lista[1]} - {lista[2]}')
        else:
            cvn.drawString(10, 90, 'NENHUM')

        cvn.setFont('Times-Bold', 20)
        cvn.drawString(10, 35, f'TROCO: {troco}')
        cvn.setFont('Times-Bold', 25)
        cvn.drawString(10, 10, f'TOTAL: {valor_total}')
        # salva o arquivo
        cvn.save()
    except:
        print('Erro')

#x = ['Coca_Cola_Zero 1','Coca_Cola_Zero 1','Coca_Cola_Zero 1']
#cria_pdf_entrega('01','20h30','Vynicius Martorano','Buzios','0994737634','rua dos carijos','290','mercadinho dasdores','R$ 15.00','R$ 37.00','PIX',x)


def cria_pdf_preparo(id,hora,nome,lista_pizzas,refri_list,endereco,n_casa,observacoes):
    import getpass
    from sistema.mounth_verify import verify_mounth
    from sistema.getTime import getTime
    if len(str(id)) == 1:
        id = '0'+id
    last_mounth = verify_mounth(getTime('m'))
    last_day = getTime('d')
    user = getpass.getuser()
    pasta_app = os.path.dirname(fr"C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Comanda\{last_mounth}\{last_day}\\")
    #Canvas recebe os argumentos:
    #pasta onde vai ser criado o arquivo e tamanho do arquivo
    cvn = canvas.Canvas(pasta_app+f'/comanda{id}.pdf',pagesize=A6)
    #drawString recebe as posições X e Y e a string
    cvn.setFont('Times-Bold', 25)
    cvn.drawString(10,390, f'ID: {id:<10}HORA: {hora}')
    cvn.setFont('Times-Roman', 19)
    cvn.drawString(10,350, f'Nome: {nome:}')
    cvn.drawString(10,330, f'{endereco}, {n_casa}')

    cvn.setFont('Times-Bold', 21)
    cvn.drawString(10,300, f'Pizza(s)')
    cvn.setFont('Times-Roman', 16)

    lista_tratada = []
    contador = 0
    for item in lista_pizzas:
        item = item.split()
        tam = len(item)
        contador += 40

        if tam == 8:
            if 'Sem_borda' in item[4]:
                item[4] = 'Nenhuma'
            tamanho = item[0]
            new_item = f'{item[2].replace("_"," ")}'
            lista_tratada.append(new_item)
            cvn.setFont('Times-Bold', 13)
            cvn.drawString(1, 315 - contador, f'{new_item}')
            cvn.setFont('Times-Bold', 13)
            cvn.drawString(1, 315 - contador - 15, f'Tamanho: {tamanho} | Borda: {item[4]}')

        elif tam == 9:
            if 'Sem_borda' in item[5]:
                item[5] = 'Nenhuma'
            tamanho = item[0]
            new_item = f'{item[2].replace("_"," ")} / {item[4].replace("_"," ")} '
            lista_tratada.append(new_item)
            cvn.setFont('Times-Bold', 13)
            cvn.drawString(1, 315 - contador, f'{new_item}')
            cvn.setFont('Times-Bold', 13)
            cvn.drawString(1, 315 - contador - 15, f'Tam: {tamanho} | Borda: {item[5]}')

        elif tam == 12:
            if 'Sem_borda' in item[8]:
                item[8] = 'Nenhuma'
            tamanho = item[0]
            new_item = f'{item[2].replace("_"," ")} / {item[4].replace("_"," ")} / {item[6].replace("_"," ")}'
            lista_tratada.append(new_item)
            cvn.setFont('Times-Bold', 13)
            cvn.drawString(1, 315 - contador, f'{new_item}')
            cvn.setFont('Times-Bold', 13)
            cvn.drawString(1, 315 - contador - 15, f'Tamanho: {tamanho} | Borda: {item[8]}')

    cvn.setFont('Times-Bold', 18)
    cvn.drawString(10, 315 - contador - 45, f'Refrigerante(s)')
    cvn.setFont('Times-Roman', 13)
    lista = []
    if len(refri_list) >= 1:
        for item in refri_list:
            split = item.split()
            if '_' in split[0]:
                x = split[0].replace('-', ' ')
                split[0] = x
            item = f'0{split[1]} {split[0]}'
            lista.append(item)
        if len(lista) == 1:
            cvn.drawString(10, 315 - contador - 65, f'{lista[0]}')
        if len(lista) == 2:
            cvn.drawString(10, 315 - contador - 65, f'{lista[0]} - {lista[1]}')
        if len(lista) == 3:
            cvn.drawString(10, 315 - contador - 65, f'{lista[0]} - {lista[1]} - {lista[2]}')
    else:
        cvn.drawString(10, 315 - contador - 65, f'NENHUM')

    cvn.setFont('Times-Bold', 18)
    cvn.drawString(10, 315 - contador - 85, f'Observações')
    cvn.setFont('Times-Roman', 13)
    cvn.drawString(10, 315 - contador - 105, observacoes)
    cvn.save()