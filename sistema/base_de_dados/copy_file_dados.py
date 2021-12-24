"""
Sistema dos pdfs
1º - Criar Pasta do dia de inicio  com numero do dia e mes 
2º - Se o mes não for igual, criar outra pasta com o novo mes
3º - Se o dia não for igual, criar outro pasta com o novo dia 

import shutil
import sqlite3

original = r'original path where the file is currently stored\file name.file extension'
target = r'target path where the file will be copied\file name.file extension'
shutil.copyfile(original, target)
"""
import shutil
import getpass
from sistema.getTime import getTime
from sistema.mounth_verify import verify_mounth
import os


def copy_file():
    last_day = getTime('d')
    last_mounth = verify_mounth(getTime('m'))
    user = getpass.getuser()
    original = fr'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\original_file\tabela.db'
    target = fr'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{last_mounth}\{last_day}\dados{last_day}.db'
    verify_last_mounth = os.path.exists(target)
    if verify_last_mounth == False:
        shutil.copy(original,target)












