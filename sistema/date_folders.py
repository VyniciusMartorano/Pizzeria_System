import os
from sistema.getTime import getTime
import getpass
from sistema.mounth_verify import verify_mounth



def create_fold_day_and_mounth():
    """
    Cria as pastas de dio e mes para armazenamento de dados
    :return: ...
    """
    last_day = getTime('d')
    last_mounth = verify_mounth(getTime('m'))
    user = getpass.getuser()

    verify_mounth_entregas = os.path.exists(fr"C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Entregas\{last_mounth}")
    verify_day_entregas = os.path.exists(fr"C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Entregas\{last_mounth}\{last_day}")

    verify_mounth_comanda = os.path.exists(fr"C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Comanda\{last_mounth}")
    verify_day_comanda = os.path.exists(fr"C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Comanda\{last_mounth}\{last_day}")

    verify_mounth_base_directory = os.path.exists(fr"C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{last_mounth}")
    verify_day_base_directory = os.path.exists(fr"C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{last_mounth}\{last_day}")

    if verify_mounth_entregas == False:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Entregas\{last_mounth}')
        ...
    elif verify_mounth_entregas == True:
        ...

    if verify_day_entregas == False:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Entregas\{last_mounth}\{last_day}')
        ...
    elif verify_day_entregas == True:
        ...

    if verify_mounth_comanda == False:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Comanda\{last_mounth}')
        ...
    elif verify_mounth_comanda == True:
        ...

    if verify_day_comanda == False:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Comanda\{last_mounth}\{last_day}')
        ...
    elif verify_day_comanda == True:
        ...
    if verify_mounth_base_directory == False:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{last_mounth}')
        ...
    elif verify_mounth_base_directory == True:
        ...
    if verify_day_base_directory == False:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{last_mounth}\{last_day}')
        ...






