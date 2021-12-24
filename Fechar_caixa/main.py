from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
import os
from get_time import getTime
from mounth_verify import verify_mounth



last_mounth = verify_mounth(getTime('m'))
last_day = getTime('d')

import getpass
user = getpass.getuser()
pasta_app = os.path.dirname(fr"C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Entregas\{last_mounth}\{last_day}\\")
# Canvas recebe os argumentos:
# pasta onde vai ser criado o arquivo e tamanho do arquivo
cvn = canvas.Canvas(pasta_app + f'\comanda_entrega{id}.pdf', pagesize=A6)


