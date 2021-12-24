import win32print
import win32api
import os
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
from getpass import getuser
from mounth_verify import verify_mounth
import sqlite3
from getTime import getTime

data = f'{getTime("d")}/{getTime("m")}/{getTime("Y")}'


user = getuser()
current_mounth = verify_mounth(getTime('m'))
current_day = getTime('d')

caminho = fr'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{current_mounth}\{current_day}\dados{current_day}.db'
conexao = sqlite3.connect(caminho)
cursor = conexao.cursor()
comand = 'SELECT forma_pagamento, valor_total FROM clientes'
cursor.execute(comand)

pix = 0
dinheiro = 0
cartao = 0 

for item in cursor.fetchall():
    forma_pagamento, valor_total = item
    if forma_pagamento == 'PIX':
        pix += float(valor_total)
    elif forma_pagamento == 'DINHEIRO':
        dinheiro += float(valor_total)
    elif forma_pagamento == 'CARTÃO':
        cartao += float(valor_total)




pasta_app = os.path.dirname(fr'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\\')
cvn = canvas.Canvas(pasta_app + rf'\fechar_caixa{current_day}.pdf', pagesize=A6)

cvn.setFont('Times-Bold', 22)
cvn.drawString(10, 380, f'Fechamento De Caixa')
cvn.drawString(10, 350, f'Data: {data}')

cvn.setFont('Times-Bold', 19)
cvn.drawString(10, 320, f'DINHEIRO: R$ {dinheiro}')
cvn.drawString(10, 290, f'CARTÃO: R$ {cartao}')
cvn.drawString(10, 260, f'PIX: R$ {pix}')
cvn.save()

file_path = fr"C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\fechar_caixa{current_day}.pdf"

printers_list = win32print.EnumPrinters(2)
printer = printers_list[0]
win32print.SetDefaultPrinter(printer[2])
win32api.ShellExecute(0, "print", file_path, None, '.', 0)

