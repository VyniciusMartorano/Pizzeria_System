def base_folders():
    import os
    import getpass
    from sistema.date_folders import create_fold_day_and_mounth
    user = getpass.getuser()

    #verificar e criar pastas
    try:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG')
    except:
        ...
    try:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory')
    except:
        ...
    try:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs')
    except:
        ...
    try:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Comanda')
    except:
        ...
    try:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Entregas')
    except:
        ...
    create_fold_day_and_mounth()
    try:
        os.mkdir(rf'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\original_file')
    except:
        ...
