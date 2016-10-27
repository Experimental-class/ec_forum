# coding:utf8
import pymysql, threading
from ec_forum.id_dealer import gene_id
from config import MyConfig

def get_conn():
    return pymysql.Connect(host='127.0.0.1',user=MyConfig.USERNAME,passwd=MyConfig.PASSWORD,db='ec_forum',charset='utf8')

'''pymysql socket pool'''
socket_limit = 10
socket_pool = []
socket_update = socket_limit

for i in range(socket_limit):
    socket_pool.append(get_conn())


def update_conn():
    global socket_update
    socket_update+=1
    if socket_update >= socket_limit:
        socket_update = 0
    print("[update pymysql connection.. Pipe %s]"%socket_update)
    socket_pool[socket_update] = get_conn()
    global t    #Notice: use global variable!
    t = threading.Timer(7200.0, update_conn)
    t.start()

t = threading.Timer(7200.0, update_conn)
if not MyConfig.TESTING:
    t.start()




class sqlQ(object):

    def get_query_name(self, table, ext='id'):
        query_name = 'u'
        if table == 'ec_article':
            query_name = 't'
        elif table == 'ec_question':
            query_name = 'q'
        elif table == 'ec_comment':
            query_name = 'c'
        elif table == 'ec_answer':
            query_name = 'a'
        elif table == 'ec_reputation':
            query_name = 'r'
        return '%s_%s'%(query_name,ext)


    def id_search(self, ec_id, table='ec_user'):
        '''search existense of an id'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        exist = True
        query_name = self.get_query_name(table)
        sql = "select * from %s where %s=%r;" % (table,query_name,ec_id)
        try:
            cursor.execute(sql)
            rs = cursor.fetchone()
            exist = bool(rs)
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return exist


    def id_select(self, ec_id, table='ec_user'):
        '''select ec_event just by t_id, and extension'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,res = True,()
        query_name = self.get_query_name(table)
        sql = "select * from %s where %s=%r;" % (table,query_name,ec_id)
        try:
            if cursor.execute(sql) == 1:
                rs = cursor.fetchone()
                if bool(rs):
                    err,res = False,rs
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err,res


    def id_delete(self, ec_id, table='ec_user'):
        '''easy ec_event delete'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err = True
        query_name = self.get_query_name(table)
        sql = "delete from %s where %s=%r;" % (table,query_name,ec_id)
        try:
            if cursor.execute(sql) == 1:
                err = False
                conn.commit()
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err


    def signup_insert(self,name,email,psw):
        '''insert without check'''
        conn = socket_pool.pop()
        err,u_id = True,gene_id()
        cursor = conn.cursor()
        while self.id_search(u_id, table='ec_user'):
            u_id = gene_id()
        sql = "insert into ec_user(u_name, u_email, u_psw, u_id, u_email_confirm, u_level, u_reputation, u_articles, u_questions,u_answers,u_watchusers) \
values(%r,%r,%r,%s,0,2,0,'&','&','&','&');" % (name,email,psw,u_id)
        try:
            if cursor.execute(sql) == 1:
                if cursor.rowcount == 1:
                    conn.commit()
                    err = False
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err, u_id


    def signup_select(self, name, method='u_name'):
        '''check if some property exist'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        exist = True
        sql = "select * from ec_user where %s=%r;" % (method, name)
        try:
            cursor.execute(sql)
            rs = cursor.fetchone()
            exist = bool(rs)
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return exist


    def signin_select(self, loginname, method='u_name'):
        '''sign in by name or email to get the tuple'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,res = True,()
        sql = "select * from ec_user where %s=%r;" % (method,loginname)
        try:
            if cursor.execute(sql) == 1:
                rs = cursor.fetchone()
                if bool(rs):
                    err,res = False,rs
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err,res



    def user_update(self, u_id, info):
        '''update the infomation'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err = True
        if len(info) == 0:
            return err
        sql = "update ec_user set "
        for k,v in info.items():
            sql += "%s=%r,"%(k,v)
        sql = sql[:-1] + " where u_id=%r;"%u_id
        # print('sql 206',sql)
        try:
            if cursor.execute(sql) == 1:
                err = False
                conn.commit()
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err


    def article_insert(self, u_id, t_title, t_text, t_tags):
        '''insert an article without check'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,t_id = True,gene_id()
        while self.id_search(t_id, table='ec_article'):
            t_id = gene_id()
        sql = "insert into ec_article(t_id, u_id, t_title, t_text, t_date, t_like, t_comments, t_tags, t_date_latest, t_star) \
        values(%s,%s,%r,%r,now(),0,'',%r, now(),0);"%(t_id, u_id, t_title, t_text, t_tags)
        try:
            if cursor.execute(sql) == 1:
                if cursor.rowcount == 1:
                    conn.commit()
                    err = False
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err,t_id


    def article_select_tag(self, t_tags=''):
        '''select article just by tag'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,res = True,()
        sql = 'select * from ec_article'
        if not bool(t_tags):
            sql += ";"
        else:
            sql += " where "
            for tag in t_tags:
                sql += "t_tags like '%%%s%%' and "%tag
            sql = sql[:-5] + ";"
        try:
            cursor.execute(sql)
            rs = cursor.fetchall()
            if bool(rs):
                err,res = False,rs
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err,res




    def article_update(self, t_id, info, modify=False):
        '''update the infomation'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err = True
        if len(info) == 0:
            return err
        sql = "update ec_article set "
        for k,v in info.items():
            sql += "%s=%r,"%(k,v)
        if modify:
            sql = sql + "t_date_latest=now() where t_id=%r;"%t_id
        else:
            sql = sql[:-1] + " where t_id=%r;"%t_id
        try:
            fs = cursor.execute(sql)
            if fs == 1:
                err = False
                conn.commit()
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err


    def comment_insert(self, ec_type, ec_id, u_id, c_text):
        '''insert an article without check'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,c_id = True,gene_id()
        while self.id_search(c_id, table='ec_comment'):
            c_id = gene_id()
        sql = "insert into ec_comment(c_id, ec_type, ec_id, u_id, c_text, c_date, c_like)\
         values(%s,%r,%s,%s,%r,now(),0);"%(c_id, ec_type, ec_id, u_id, c_text)
        # print('sql.py 145',sql)
        try:
            if cursor.execute(sql) == 1:
                if cursor.rowcount == 1:
                    conn.commit()
                    err = False
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err,c_id


    def reputation_add(self, r_type, ec_type, ec_id, ua_id, ua_rep, ub_id, ub_rep):
        '''insert an article without check'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,r_id = True,gene_id()
        while self.id_search(r_id, table='ec_reputation'):
            r_id = gene_id()
        sql = 'insert into ec_reputation(r_id, r_type, ec_type, ec_id, ua_id, ub_id, ua_rep, ub_rep, r_date)\
        values(%s,%r,%r,%s,%s,%s,%s,%s,now());'%(r_id, r_type, ec_type, ec_id, ua_id, ub_id, ua_rep, ub_rep)
        # print('sql 347',sql)
        try:
            if cursor.execute(sql) == 1:
                if cursor.rowcount == 1:
                    conn.commit()
                    err = False
        except BrokenPipeError as e:
            conn = get_conn()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err, r_id


    def reputation_select(self, r_type, ec_type, ec_id, ua_id, ub_id):
        '''check user star_like event has done or not'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,res = False, ()
        sql = 'select * from ec_reputation where r_type=%r and ec_type=%r and ec_id=%s and ua_id=%s and ub_id=%s;'%(r_type, ec_type, ec_id, ua_id, ub_id)
        try:
            if cursor.execute(sql) == 1:
                rs = cursor.fetchone()
                if bool(rs):
                    res = rs
        except BrokenPipeError as e:
            conn = get_conn()
            err = True
            raise e
        except Exception as e:
            conn.rollback()
            err = True
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err, res

    def reputation_fetch_all(self,u_id):
        '''query user reputation history'''
        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,res = False, ()
        sql = 'select * from ec_reputation where ua_id=%s or ub_id=%s;'%(u_id, u_id)
        try:
            rv = cursor.execute(sql)
            print('ffffffff',rv)
            res = cursor.fetchall()
        except BrokenPipeError as e:
            conn = get_conn()
            err = True
            raise e
        except Exception as e:
            conn.rollback()
            err = True
            raise e
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err, res


