import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\kimjiyun\Downloads\훈련과정_전체데이터_ver3.csv")

# 8자리로 만들고
df['NCS_코드'] = df['NCS_코드'].astype(str).str.zfill(8)

# NCS 코드 4개로 나누어 직종 분류
df['NCS_1'] = df['NCS_코드'].str[0:2]
df['NCS_2'] = df['NCS_코드'].str[2:4]
df['NCS_3'] = df['NCS_코드'].str[4:6]
df['NCS_4'] = df['NCS_코드'].str[6:8]

ncs1_map = {
    '01': '사업관리',
    '02': '경영/회계/사무',
    '03': '금융/보험',
    '04': '교육/자연/사회과학',
    '05': '법률/경찰/소방/교도/국방',
    '06': '보건/의료',
    '07': '사회복지/종교',
    '08': '문화/예술/디자인/방송',
    '09': '운전/운송',
    '10': '영업판매',
    '11': '경비/청소',
    '12': '이용/숙박/여행/오락/스포츠',
    '13': '음식서비스',
    '14': '건설',
    '15': '기계',
    '16': '재료',
    '17': '화학/바이오',
    '18': '섬유/의복',
    '19': '전기/전자',
    '20': '정보통신',
    '21': '식품가공',
    '22': '인쇄/목재/가구/공예',
    '23': '환경/에너지/안전',
    '24': '농림어업'
}
df['NCS_1_분류명'] = df['NCS_1'].map(ncs1_map)

# 수강신청인원 0명인 행 제거
df = df[df['수강신청인원'] > 0].reset_index(drop=True)

# 인기있는 훈련과정(ncs)
df['신청률'] = df['수강신청인원'] / df['정원']

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# 스트림릿 앱 제목
st.title("2024년 직종별 평균 신청률")

# 직종(NCS_1)별 평균 신청률로 인기 정도 계산
mean_ratio = df.groupby(['NCS_1', 'NCS_1_분류명'])['신청률'].mean().sort_values(ascending=False)

# 라벨 생성
labels = [name for code, name in mean_ratio.index]

# Plotly Figure 생성
fig = go.Figure(data=[
    go.Bar(
        x=labels,
        y=mean_ratio.values,
        marker_color='rgb(79,129,189)'  # seaborn Blues_d 유사 색상
    )
])

# 레이아웃 설정
fig.update_layout(
    title='직종별 평균 신청률',
    xaxis_title='직종분류명',
    yaxis_title='평균 신청률',
    xaxis_tickangle=-90,
    height=600
)

# 스트림릿에 그래프 출력
st.plotly_chart(fig)


# st.plotly_chart(fig)