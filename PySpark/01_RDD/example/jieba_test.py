# coding:utf8

import jieba

if __name__ == '__main__':
    content = "小明硕士毕业于中国科学院计算所,后在清华大学深造"

    result = jieba.cut(content, True)
    print(list(result))
    print(type(result))

    #
    result2 = jieba.cut(content, False)
    print(list(result2))

    # 搜索引擎模式, 等同于允许二次组合的场景
    result3 = jieba.cut_for_search(content)
    print(",".join(result3))
