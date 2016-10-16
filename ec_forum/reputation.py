from flask import Flask
import ec_forum.sql as sql

sqlQ = sql.sqlQ()

event = {
    0:{'s':'+1', 'r':0, 'n':'email_confirm'},
    1:{'s':'+0', 'r':0, 'n':'article_add'},
    2:{'s':'+0', 'r':0, 'n':'article_del'},
    3:{'s':'+1', 'r':0, 'n':'article_collected'},
    4:{'s':'+1', 'r':15, 'n':'article_recommended'},
    5:{'s':'', 'r':, 'n':'',},
    6:{'s':'', 'r':, 'n':'',},
    7:{'s':'', 'r':, 'n':'',},
    8:{'s':'', 'r':, 'n':'',},
    9:{'s':'', 'r':, 'n':'',},
    10:{'s':'', 'r':, 'n':'',},
    11:{'s':'', 'r':, 'n':'',},
    12:{'s':'', 'r':, 'n':'',},
    13:{'s':'', 'r':, 'n':'',},
    14:{'s':'', 'r':, 'n':'',},
    15:{'s':'', 'r':, 'n':'',},
    16:{'s':'', 'r':, 'n':'',},
    17:{'s':'', 'r':, 'n':'',},
    18:{'s':'', 'r':, 'n':'',},
    19:{'s':'', 'r':, 'n':'',},
    20:{'s':'', 'r':, 'n':'',},

}

def run(app):

    @app.route('./r/history')
    print(event)
