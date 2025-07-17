import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv(r"./훈련과정_전체데이터_ver3.csv")

# 8자리로 만들고
df['NCS_코드'] = df['NCS_코드'].astype(str).str.zfill(8)

# NCS 코드 4개로 나누어 직종 분류
df['NCS_1'] = df['NCS_코드'].str[0:2]
df['NCS_2'] = df['NCS_코드'].str[2:4]
df['NCS_3'] = df['NCS_코드'].str[4:6]
df['NCS_4'] = df['NCS_코드'].str[6:8]

ncs1_map = {
    '01': '사업관리', '02': '경영/회계/사무', '03': '금융/보험', '04': '교육/자연/사회과학',
    '05': '법률/경찰/소방/교도/국방', '06': '보건/의료', '07': '사회복지/종교', '08': '문화/예술/디자인/방송',
    '09': '운전/운송', '10': '영업판매', '11': '경비/청소', '12': '이용/숙박/여행/오락/스포츠',
    '13': '음식서비스', '14': '건설', '15': '기계', '16': '재료', '17': '화학/바이오',
    '18': '섬유/의복', '19': '전기/전자', '20': '정보통신', '21': '식품가공', '22': '인쇄/목재/가구/공예',
    '23': '환경/에너지/안전', '24': '농림어업'
}
df['NCS_1_분류명'] = df['NCS_1'].map(ncs1_map)

# 수강신청인원 0명인 행 제거
df = df[df['수강신청인원'] > 0].reset_index(drop=True)

# 신청률 계산
df['신청률'] = df['수강신청인원'] / df['정원']

######################################
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
######################################
# 1. 지역별 공급상태 비율 파이차트

def tag_supply_ratio(row):
    if row['신청률'] >= 0.95:
        return '공급 부족'
    elif row['신청률'] < 0.5:
        return '공급 과잉'
    else:
        return '중간'

df['공급상태'] = df.apply(tag_supply_ratio, axis=1)

status_count = (
    df[df['공급상태'] != '중간']
    .groupby(['주소', 'NCS_1', 'NCS_1_분류명', '공급상태', '정원','수강신청인원', '신청률'])
    .size()
    .reset_index(name='count')
)

st.title("서울시 지역별 훈련과정 분석")

# 구 목록을 전체 데이터에서 가져옴
gu_list = sorted(df['주소'].unique())

# 하나의 selectbox로 통합
selected_gu = st.selectbox("구 선택", gu_list)

### 1. 선택한 구의 인기 직종 (수강신청인원 기준) ###
popular_courses = (
    df[df['주소'] == selected_gu]
    .groupby('NCS_1_분류명')['수강신청인원']
    .sum()
    .reset_index()
    .sort_values(by='수강신청인원', ascending=False)
)

# 상위 5개 + 기타
top5 = popular_courses.head(5)
others = popular_courses.iloc[5:]
etc_row = pd.DataFrame([{
    'NCS_1_분류명': '기타',
    '수강신청인원': others['수강신청인원'].sum()
}])

combined = pd.concat([top5, etc_row], ignore_index=True)

# 파이차트 1: 인기 직종 분포
fig_popular = go.Figure(
    data=[go.Pie(
        labels=combined['NCS_1_분류명'],
        values=combined['수강신청인원'],
        hole=0,
        marker=dict(colors=px.colors.qualitative.Pastel)
    )]
)
fig_popular.update_layout(title_text=f"📊 {selected_gu} 인기 직종 분포")

### 2. 선택한 구의 전체 직종 분포 (훈련과정 수 기준) ###
NCS_1_region = df.groupby(['주소', 'NCS_1']).size().reset_index(name='count')
NCS_1_region['NCS_1_명'] = NCS_1_region['NCS_1'].map(ncs1_map)

data_ncs = NCS_1_region[NCS_1_region['주소'] == selected_gu]
data_ncs_sorted = data_ncs.sort_values(by='count', ascending=False)

top7_ncs = data_ncs_sorted.head(5)
etc_count = data_ncs_sorted['count'].iloc[5:].sum()

labels_ncs = list(top5_ncs['NCS_1_명']) + ['기타(etc)']
values_ncs = list(top5_ncs['count']) + [etc_count]

# 파이차트 2: 전체 직종 분포
fig_ncs = go.Figure(
    data=[go.Pie(
        labels=labels_ncs,
        values=values_ncs,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(line=dict(color='white', width=2)),
        sort=False
    )]
)
fig_ncs.update_layout(title=f"🧭 {selected_gu} 직종 분포", height=500)



st.plotly_chart(fig_popular)
st.write('※ 기준: 수강신청인원')

st.plotly_chart(fig_ncs)
st.write('※ 기준: 개설 훈련과정 수')


# # 2개 컬럼 만들기
# col1, col2 = st.columns(2)

# # 왼쪽: 수강신청인원 기준 인기 직종
# with col1:
#     st.subheader(f"📊 {selected_gu} 인기 직종")
#     st.plotly_chart(fig_popular, use_container_width=True)
#     st.caption('※ 기준: 수강신청인원')

# # 오른쪽: 개설과정 수 기준 직종 분포
# with col2:
#     st.subheader(f"🧭 {selected_gu} 직종 분포")
#     st.plotly_chart(fig_ncs, use_container_width=True)
#     st.caption('※ 기준: 개설 훈련과정 수')



