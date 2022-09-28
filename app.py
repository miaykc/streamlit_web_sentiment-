# R11142006
# 葉凱晴

# this python file uses the following encoding: utf-8

import pandas as pd
import streamlit as st 
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from snownlp import SnowNLP



# s = SnowNLP(u'今天是週六。')
# s.words
# s = SnowNLP(u'我喜歡語言學')

# s.han

# text_1 = "人生好難啊。"
# s_1 = SnowNLP(text_1)
# text_2 = "人生好難啊，要怎樣才能每天開心得活著呢？"
# s_2 = SnowNLP(text_2)
# print(s_1.sentiments)
# print(s_2.sentiments)

# text_3 = SnowNLP(u'時間不夠用，每天還是努力學習。也許我是傻蛋，但我有一天會成功')
# sent = text_3.sentences
# for sen in sent:
#     s_3 = SnowNLP(sen)
#     print(s_3.sentiments)

st.set_page_config(layout="wide")


# Fxn (functions)
def convert_to_df(sentiment):
    sentiment_dict = {'polarity':sentiment.sentiments,'subjectivity':sentiment.tags}

    sentiment_df = pd.DataFrame(sentiment_dict.items(),columns=['metric','value'])
    return sentiment_df

def analyze_token_sentiment(docx):
    analyzer = SentimentIntensityAnalyzer()
    pos_list = []
    neg_list = []
    neu_list = []

    sNLP_txt = SnowNLP(docx)

    for sNLP_word in sNLP_txt.words:
        if SnowNLP(sNLP_word).sentiments >= 0.5:
            pos_list.append(sNLP_word)

        elif (SnowNLP(sNLP_word).sentiments >= 0.5) & (SnowNLP(sNLP_word).sentiments > 0):
            neg_list.append(sNLP_word)
        else:
            neg_list.append(sNLP_word)

    result = {'正面詞語':pos_list,'負面詞語':neg_list,'中立詞語':neu_list}
    return result



def main():
    st.title("～情緒分析小幫手～")
    st.subheader("這句話到底是正面還是負面呢？讓小幫手來替你分析!")

    menu = ["首頁", "關於"]
    choice = st.sidebar.selectbox("目錄", menu)
    
    if choice == "首頁":
        st.subheader("首頁")
        with st.form(key='nlpForm'):
            raw_text = st.text_area("請輸入文字...")
            submit_button = st.form_submit_button(label='進行分析')
        
        # layout
        coll,col2 = st.columns(2)
        if submit_button:

            with coll:
                st.info("情緒分數")
                sNLP_text = SnowNLP(raw_text) # 為什麼不能打(raw_text).sentiment
                st.write(sNLP_text.sentiments)
                

                # Emoji
                if sNLP_text.sentiments > 0.5:
                    st.markdown("情感概率: 正面 :smiley: ")
                elif sNLP_text.semtiments < 0.5:
                    st.markdown("情感概率: 負面 :angry: ")
                else:
                    st.markdown("情感概率: 中立 :neutral: ")
                
                # #Dataframe
                # result_df = convert_to_df(sentiments)
                # st.dataframe(result_df)

                # # #visaulization
                # c = alt.Chart(result_df).mark_bar().encode(x='metric',y='value',color='metric')
                
                # st.altair_chart(c,use_container_width=True)
            
                 

            with col2:
                st.info("詞語分析")

                token_sentiments = analyze_token_sentiment(raw_text)
                st.write(token_sentiments)




    
    else:
        st.subheader("關於")


if __name__ == '__main__':
    main()


