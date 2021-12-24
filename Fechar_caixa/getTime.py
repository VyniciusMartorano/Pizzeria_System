from datetime import datetime


def getTime(mode):
    """
    :param mode: H = Hour, M = Minute, d = dia, m = Mounth, Y = Year.
    :return: hour or minute or day or mounth or year
    """
    time = ''
    if mode == 'H':
        time = datetime.now().strftime('%H')
        return time
    if mode == 'M':
        time = datetime.now().strftime('%M')
        return time
    if mode == 'S':
        time = datetime.now().strftime('%S')
        return time
    if mode == 'd':
        time = datetime.now().strftime('%d')
        return time
    if mode == 'm':
        time = datetime.now().strftime('%m')
        return time
    if mode == 'Y':
        time = datetime.now().strftime('%Y')
        return time
    else:
        return print('Argumento irregular')