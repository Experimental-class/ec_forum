from flask import request,jsonify
import ec_forum.error as error
import ec_forum.expr as expr
from ec_forum.sql import sqlQ
from ec_forum.salt import encrypt, decrypt
from ec_forum.public import mail_sender
from ec_forum.id_dealer import unpack_id, pack_id 
sqlQ = sqlQ()

def run(app):

    @app.route('/u/query', methods=['POST'])
    def user_query():
        if request.method != 'POST':
            return jsonify(error.requestError)
        u_id = request.values.get('u_id', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)

        '''db'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)

        return jsonify({
            # 'u_id':res[0],
            'u_name':res[1],
            # 'u_psw':res[2],
            'u_email':res[3],
            # 'u_email_confirm':res[4],
            # 'u_level':res[5],
            'u_reputation':res[6],
            'u_realname':res[7],
            'u_blog':res[8],
            'u_github':res[9],
            'u_articles':res[10],
            'u_questions':res[11],
            'u_answers':res[12],
            'u_watchusers':res[13],
            'u_tags':res[14],
            'u_intro': res[15],
        })






    @app.route('/u/update', methods=['POST'])
    #self, uid, psw, rn, bl, gh, waus, tags)
    def user_update():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        u_info = {
            'u_realname':request.values.get('u_realname',''),
            'u_blog':request.values.get('u_blog',''),
            'u_github':request.values.get('u_github',''),
            # 'u_watchusers':request.values.get('u_watchusers',''),
            'u_tags':request.values.get('u_tags',''),
            'u_intro':request.values.get('u_intro',''),
        }
        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        err = sqlQ.user_update(u_id, u_info)
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1','u_id':u_id})






    @app.route('/u/email/verify', methods=['POST'])
    def email_confirm_request():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_email = request.values.get('u_email','')
        u_verify = request.values.get('u_verify','')
        
        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_email == '':
            return jsonify(error.emailEmpty)
        if u_verify == '':
            return jsonify(error.verifyEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)

        '''formate legal'''
        if not expr.validEmail(u_email):
            return jsonify(error.emailIllegal)

        mail_title = '实验班问答交流平台邮箱验证' 
        mail_subject = '以下是您的验证码：\n\n %s\n\n您好！我们收到了来自您的邮箱验证请求，请使用上述验证码来验证您的邮箱归属，如果你从未发送过相关请求，请忽略此邮件。\n\nhave a nice day!\n实验班问答交流平台'%u_verify
        mail_sender(u_email, mail_title, mail_subject)

        return jsonify({'code':'1'})

 




    @app.route('/u/email/confirm', methods=['POST'])
    def email_confirm_pass():

        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        
        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''update info, todo: add rep'''
        err = sqlQ.user_update(u_id, {'u_email_confirm':'1'})
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1'})






    @app.route('/u/email/change', methods=['POST'])
    def email_change():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        u_email = request.values.get('u_email','')
        u_info = {
            'u_email':u_email,
            'u_email_confirm':'0'
        }
        
        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if u_email == '':
            return jsonify(error.emailEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''update info, todo: reduce rep'''
        err = sqlQ.user_update(u_id, u_info)
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1'})
            


    @app.route('/u/watchuser', methods=['POST'])
    def watch_user():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        ua_id = request.values.get('ua_id','')
        u_act = request.values.get('u_act','')

        '''empty'''
        if u_id == '' or ua_id == '':
            return jsonify(error.useridEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.userid_search(ua_id):
            return jsonify(error.watchuserNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''watchid'''
        watch_user_dic = unpack_id(res[13])
        err,res = sqlQ.signin_select(ua_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        be_watched_user_dic = unpack_id(res[13])
        if u_act == '1':
            if str(ua_id) in watch_user_dic[0] or str(u_id) in be_watched_user_dic[1]:
                return jsonify(error.userAlreadyWatched)
            watch_user_dic[0].append(ua_id)
            be_watched_user_dic[1].append(u_id)
        elif u_act == '0':
            if str(ua_id) not in watch_user_dic[0] or str(u_id) not in be_watched_user_dic[1]:
                return jsonify(error.userAlreadyUnwatched)
            watch_user_dic[0].remove(ua_id)
            be_watched_user_dic[1].remove(u_id)
        else:
            return jsonify(error.argsError)
        '''update info'''
        if sqlQ.user_update(u_id, {'u_watchusers': pack_id(watch_user_dic)}):
            return jsonify(error.serverError)
        if sqlQ.user_update(ua_id, {'u_watchusers': pack_id(be_watched_user_dic)}):
            return jsonify(error.serverError)

        return jsonify({'code':'1'})
            
 
