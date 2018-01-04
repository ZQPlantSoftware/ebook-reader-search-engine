# -*- coding: UTF-8 -*-
from whoosh.compat import u, text_type
from whoosh.analysis import Tokenizer, Token
import jieba

class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False,
            keeporiginal=False, removestops=True,
            start_pos=0, start_char=0, mode='', **kwarys):
        assert isinstance(value, text_type), "%r is not unicode" % value
        t = Token(positions, chars, mode=mode, *kwarys)
        seglist = jieba.cut(value, cut_all=False)

        for w in seglist:
            t.original = t.text = w
            t.boost = 1.0
            if positions:
                t.pos = start_pos + value.find(w)
            if chars:
                t.startchar = start_char + value.find(w)
                t.endchar = start_char + value.find(w) + len(w)
            yield t   # 通过生成器返回每个分词结果token

def ChineseAnalyzer():
    return ChineseTokenizer()

#重点在这里，将原先的RegexAnalyzer(ur”([\u4e00-\u9fa5])|(\w+(\.?\w+)*)”),
#改成这句，用中文分词器代替原先的正则表达式解释器。
# analyzer = ChineseAnalyzer()
