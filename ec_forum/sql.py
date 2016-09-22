# coding:utf8
import pymysql
from ec_forum.id_dealer import gene_id

conn = pymysql.Connect(
    host = '127.0.0.1',
    user = 'root',
    passwd = '',
    db = 'ec_forum',
    charset = 'utf8'
)

class sqlQ(object):

    def signup_insert(self,name,email,psw):
        u_id = ''
        err = True
        cursor = conn.cursor()
        try:
            u_id = gene_id()
            while self.userid_search(u_id, table='ec_user'):
                u_id = gene_id()
            sql = "insert into ec_user(u_name, u_email, u_psw, u_id, u_email_confirm, u_level, u_reputation) values('%s','%s','%s',%s,0,4,0);" % (name,email,psw,u_id)
            print(sql)
            cursor.execute(sql)
            print(cursor.rowcount)
            if cursor.rowcount == 1:
                err = False
        except Exception as e:
            raise Exception('sign_up failed')
            err = False
        finally:
            cursor.close()
        return err, u_id

    def signup_select(self, name, method='u_name'):
        cursor = conn.cursor()
        exist = True
        try:
            sql = "select * from ec_user where %s='%s'" % (method, name)
            cursor.execute(sql)
            rs = cursor.fetchone()
            # if not bool(rs):
            #    exist = False
            exist = bool(rs)
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return exist

    def userid_search(self, ec_id, table='ec_user'):
        cursor = conn.cursor()
        exist = True
        try:
            sql = "select * from %s where u_id='%s'" % (table,ec_id)
            cursor.execute(sql)
            rs = cursor.fetchone()
            exist = bool(rs)
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return exist

    def signin_select(self, loginname, psw, method='u_name'):
        cursor = conn.cursor()
        err = False
        try:
            sql = "select * from ec_user where %s='%s' and u_psw='%s'" % (method,loginname,psw)
            cursor.execute(sql)
            rs = cursor.fetchone()
            exist = bool(rs)
        except Exception as e:
            raise
        finally:
            cursor.close()
        return err

    def delete():
        pass




if __name__ == '__main__':
    conn = pymysql.Connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            passwd = '',
            db = 'ec_forum',
            charset = 'utf8'
            )
    # cursor = conn.cursor()
    #
    # sql_insert = "insert into user(userid, username) values(9, 'nanako')"
    # sql_update = "update user set username='nana' where userid=9"
    # sql_delete = "delete from user where userid>8"
    #
    # try:
    #     cursor.execute(sql_insert)
    #     print (cursor.rowcount)
    #
    #     cursor.execute(sql_update)
    #     print (cursor.rowcount)
    #
    #     cursor.execute(sql_delete)
    #     print (cursor.rowcount)
    #
    #     conn.commit()
    # except Exception as e:
    #     print(e)
    #     conn.rollback()
    #
    # cursor.close()
    # conn.close()
