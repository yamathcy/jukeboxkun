import numpy as np

class tweet2sentiment:

    def __init__(self):

        # 全ての情報を持つdicと単語とセンチメント値のみ保持するdic_valueに格納
        self.sentiment_dic = []
        self.sentiment_dic_value = {}

        # 辞書の読み込み
        with open("./ja_dic.txt") as f:
            # 1行ずつの文字をリストにする
            lines = f.readlines()
            for line in lines:

                # 項目を切り離して格納
                appending = line.split(":")
                self.sentiment_dic.append(appending)

                # 単語:極性値の形で保持
                self.sentiment_dic_value[appending[0]] = float(appending[3].strip("¥n"))


    # センチメント値への変換
    # 形態素解析をする
    # ツイートの全単語のセンチメント値の加算平均を返す
    def calc_sentiment(self,tweets):
        calc = []
        for tweet_words in tweets:
            for tweet_word in tweet_words:
                try:
                    # 平均計算用に極性値を入れる
                    calc.append(self.sentiment_dic_value[tweet_word])

                except KeyError:
                    pass
        result = np.mean(calc)
        print(result)
        return result




