import tweepy
import os,sys
from janome.tokenizer import Tokenizer
from sentiment import tweet2sentiment
from mood_music import mood_search_by_api


CK = os.environ["CONSUMER_KEY"]
CS = os.environ["CONSUMER_SECRET"]
AT = os.environ["ACCESS_TOKEN"]
AS = os.environ["ACCESS_SECRET"]

def main():
    words = []
    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)

    # 直近にリプライしたユーザーの情報を取得
    rep_user = api.mentions_timeline()[0]
    status_id = rep_user.id # ID
    screen_name = rep_user.author.screen_name # 表示名
    # print(status_id,screen_name)
    tweets = api.user_timeline(screen_name,count=10) # リプしたユーザーのつぶやき

    # print("リプ欄{}".format(tweets))

    # ユーザーのタイムラインを形態素解析
    for tweet in tweets:
        t = Tokenizer()
        tokens = t.tokenize(tweet.text, wakati=True)
        words.append(tokens)
    # print(words)

    # センチメント値を計算
    calc = tweet2sentiment()
    sentiment_value = calc.calc_sentiment(tweets=words)

    # 極性を0-1の範囲になるよう変換してspotifyAPIの関数に渡す
    mood_search = mood_search_by_api(0.5*sentiment_value+ 0.5)

    # 結果を受け取る
    result = mood_search.search_by_spotify()
    url = result[2]

    """
    if url == "None":
        url = "視聴urlなし"
    
    print("リプ先{}".format(screen_name))
    """

    # リプする内容
    reply = "@" + str(screen_name) + "こんな曲いかがですか？" + str(result[0]) + " " + str(result[1]) + " " + str(url)

    # リプライ
    api.update_status(status=reply, in_reply_to_status_id=status_id)

if __name__ == "__main__":
    main()







