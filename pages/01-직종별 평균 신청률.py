import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv(r"./훈련과정_전체데이터_ver3.csv")

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

# 강좌 수 계산
course_count = df.groupby(['NCS_1', 'NCS_1_분류명']).size()
course_count = course_count.loc[mean_ratio.index]


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

# Plotly Figure 생성
fig = go.Figure()

# 막대: 평균 신청률 + 텍스트: 강좌 수
fig.add_trace(go.Bar(
    x=labels,
    y=mean_ratio,
    name='평균 신청률',
    marker_color='rgb(79,129,189)',
    text=course_count,                # 텍스트로 강좌 수 표시
    textposition='outside',          # 막대 위에 표시
    hovertemplate=
        '<b>%{x}</b><br>' +
        '평균 신청률: %{y:.2f}<br>' +
        '강좌 수: %{text}<extra></extra>'
))

fig.update_layout(
    title='직종별 평균 신청률 및 강좌 수',
    xaxis=dict(title='직종분류명', tickangle=-90),
    yaxis=dict(title='평균 신청률'),
    height=600
)

st.plotly_chart(fig)
