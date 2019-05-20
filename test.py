from sklearn.datasets import load_iris

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.preprocessing.data import minmax_scale

import jieba



def minmax_demo():

    data = [[2, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]]
    minmax = minmax_scale(data)


    print(minmax)


def datasets_demo():

    iris = load_iris()

    print(iris)

    print(iris.feature_names)

    print(iris["DESCR"])

    print(iris.data, iris.data.shape)

    x_train, x_test, y_train, y_test = train_test_split(iris.data,iris.target,test_size=0.2,random_state=22)

    print(x_train,x_test,y_train,y_test)

    return None

def count_demo():

    transfer = CountVectorizer()

    data = ['I like play basketball', 'I do not like play football']

    result = transfer.fit_transform(data)
    print(result.toarray())
    print(transfer.get_feature_names())
    return None


def cut_words(text):

    word = " ".join(list(jieba.cut(text)))
    return word


def tf_demo():
    # tf-idf 衡量一个词的重要程度,进行文本特征抽取

    transfer = TfidfVectorizer()

    data = ['我爱北京天安门，天安门上太阳升']
    data_new = []

    for sent in data:
        data_new.append(cut_words(sent))

    print("this is new data:\n", data_new)


    result = transfer.fit_transform(data_new)
    print(result.toarray())
    print(transfer.get_feature_names())
    return None

if __name__ == "__main__":

   # datasets_demo()

     # count_demo()

     #tf_demo()

     minmax_demo()

