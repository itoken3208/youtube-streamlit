from typing import Text
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st
import numpy as np
from PIL import Image

st.title("streamlit超入門")
st.write("プログレスバーの表示")
"Start"

latest_iteration = st.empty()#からのiterationを作る
bar = st.progress(0)

import time
for i in range(100):#for文を回すごとに1~100の数字をiに入れる
    latest_iteration.text(f"Iteration{i+1}")#1~100秒までの数字を空のiterationに入れて表示する
    bar.progress(i + 1)
    time.sleep(0.01)
    print(i)
    time.sleep(0.1)
"done"