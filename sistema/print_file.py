
def imprimir(file_path):
    import win32api
    import win32print
    """
    :param file_path: Caminho do arquivo
    :return:
    """
    printers_list = win32print.EnumPrinters(2)
    printer = printers_list[0]
    win32print.SetDefaultPrinter(printer[2])
    win32api.ShellExecute(0, "print", file_path, None, '.', 0)




