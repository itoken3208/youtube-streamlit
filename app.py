import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title("米国株可視化アプリ")

st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定して下さい
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider("日数",1,50,20)
st.write(f"""
###過去 **{days}日間**のGAFA株価
""")


@st.cache
def get_data(days,tickers):#get_data関数を定義、引数にdaysとtickersを使用
    df = pd.DataFrame()#空のデータフレームを用意
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])#tkrをTickerと定義、引数のTickersのリストにcompanyを入れるcompanyの値を実行する
        hist =tkr.history(period=f"{days}d")#ここで株価を取得する
        hist.index = hist.index.strftime("%d%B %Y")#日、月、年の順番に変更
        hist = hist[["Close"]]#終わり値を表示
        hist.columns = [company]
        hist = hist.T
        hist.index.name = "Name"#nameの欄を作る
        df = pd.concat([df,hist])#空のデータフレームとhistに入っている値を連結
    return df

st.sidebar.write(""""
## 株価の範囲指定
""")
ymin,ymax = st.sidebar.slider(
    "範囲を指定して下さい",
    0.0,3500.0, (0.0,3500.0)
)

days = 20
tickers = {       #辞書型tickersを作成、はaaplとfbが入る
    "apple":"AAPL",
    "facebook":"FB",
    "google":"googl",
    "microsoft":"MSFT",
    "netflix":"NFLX",
    "amazon":"AMZN"
}
df = get_data(days,tickers)
companies = st.multiselect(
    "会社名を選択してください",
    list(df.index),
    ["google","amazon","facebook","apple"]
)

if not companies:
    st.error("少なくとも1社は選んでください。")
else:
    data = df.loc[companies]
    st.write("### 株価 (USD",data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["Date"]).rename(
        columns = {"value":"Stock Prices(USD"}
    )

    chart = (
        alt.Chart(data)#alt.Chartの引数にdataを渡す
        .mark_line(opacity = 0.8,clip=True)#opacityで透明度を表す
        .encode(
            x = "Date:T",#x軸を設定、Tは時間
            y = alt.Y("Stock Prices(USD):Q",stack=None,scale=alt.Scale(domain=[120,200])),
            color = "Name:N"   
        )
    )
    st.altair_chart(chart, use_container_width=True)

