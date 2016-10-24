

event = {
    'email_confirm_pass'           : [+1],
    'email_confirm_change'         : [-1],
    'article_add'                  : [ 0],
    # 'article_del'                  : [ 0],
    'comment_add'                  : [ 0,  0],
    # 'comment_del'                  : [ 0,  0],
    'article_del_other'            : [-1, -1],
    'article_star'                 : [ 0, +1],
    # 'article_star_cancel'          : [ 0, -1],
    'article_recommend'            : [ 0, +1],
    # 'article_recommend_cancel'     : [ 0, -1],
    'comment_like'                 : [ 0,  0],
    # 'comment_like_cancel'          : [ 0,  0],
    'comment_dislike'              : [ 0,  0],
    # 'comment_dislike_cancel'       : [ 0,  0],
}

rule = {
    'comment_like'                 :    1,
    'report'                       :   15,
    'answer_like'                  :   15,
    'question_like'                :   15,
    'article_like'                 :   15,
    'tag_edit'                     :  100,
    'answer_dislike'               :  125,
    'question_dislike'             :  125,
    'question_edit'                :  200,
    'answer_edit'                  :  200,
    'question_close'               : 1000,
    'tag_new'                      : 1500,
    'answer_delete'                : 3000,
    'question_delete'              : 5000,
}
