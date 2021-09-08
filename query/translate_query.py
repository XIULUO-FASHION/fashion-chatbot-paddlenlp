# translate query to english

from query import translator_google as googletrans
# import translator_google as googletrans
import pandas as pd
import os

from query import translate_query
# import translate_query
DIC_FILE_DIR = os.path.dirname(translate_query.__file__)

def get_dict(fpath=os.path.join(DIC_FILE_DIR, 'chatbot_labels.csv')):
    df = pd.read_csv(fpath)
    en_ls = list(df['label'])
    zh_ls = list(df['label_zh'])

    return dict(zip(zh_ls, en_ls))


def trans(s):
    gg = googletrans.Google()
    return gg.translate('zh-CN', 'en', s)[0]

def get_trans_query(ls):
    dic = get_dict()

    ls_trans = []
    for word in ls:
        if word:
            if word in dic:
                ls_trans.append(dic[word])
            else:
                ls_trans.append(trans(word))
    
    return ls_trans

def _main():

    ls1 = ['红色', '纯色', '无袖', '长裙']
    ls2 = ['褐色', '碎花', '袖子长点', '夹克']

    print(get_trans_query(ls1))
    print(get_trans_query(ls2))

if __name__ == '__main__':
    _main()
