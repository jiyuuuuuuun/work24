import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
#import gdown



# 공유 가능한 Google Drive 파일 ID
#file_id = "https://drive.google.com/file/d/1igmexr5uG_-WYiy_tvSKdlmeqzmoH7PM/view?usp=drive_link"  # 공유 링크에서 추출
# 파일 다운로드
#gdown.download(file_id, "df4.csv", quiet=False)


import pandas as pd
import streamlit as st

# 데이터 불러오기
df4 = pd.read_csv(r"C:\Users\alsdu\Downloads\훈련과정_전체데이터_ver3.csv")  



st.title("📊 인기 강좌 분석")
df4['정원_대비_신청률'] = (df4['수강신청인원'] / df4['정원'] * 100).round(1)

top_rate = df4.sort_values('정원_대비_신청률', ascending=False).head(10)
top_count = df4.sort_values('수강신청인원', ascending=False).head(10)

# 신청률 시각화
st.subheader("✅ 정원 대비 신청률 TOP 10")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x='정원_대비_신청률', y='제목', data=top_rate, ax=ax1)
ax1.set_title('정원 대비 신청률 (%)')
st.pyplot(fig1)
s
# 수강신청인원 시각화
st.subheader("✅ 수강신청 인원 TOP 10")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='수강신청인원', y='제목', data=top_count, ax=ax2)
ax2.set_title('수강신청 인원')
st.pyplot(fig2)