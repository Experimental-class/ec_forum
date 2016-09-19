from random import randint

def gene_id(num=12, letter=False, lower=False):
    origin = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    rang = 62
    if letter:
        rang = 62
        if lower:
            rang = 36
    else:
        rang = 10

    res = ''
    for i in range(num):
        res = res + origin[randint(0, rang-1)]

    return res