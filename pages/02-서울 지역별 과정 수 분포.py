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



##########################
# 지역별 과정 수 분포

import plotly.graph_objects as go

# status_count가 이미 있다고 가정
# status_count = df[df['공급상태'] != '중간'].groupby([...]).size().reset_index(name='count')

st.title("서울시 지역별 과정 수 분포")

def tag_supply_ratio(row):
    if row['신청률'] >= 0.95:
        return '공급 부족'
    elif row['신청률'] < 0.5:
        return '공급 과잉'
    else:
        return '중간'

df['공급상태'] = df.apply(tag_supply_ratio, axis=1)

status_count = (
    df[df['공급상태'] != '중간']  # 중간은 제외
    .groupby(['주소', 'NCS_1', 'NCS_1_분류명', '공급상태', '정원','수강신청인원', '신청률'])
    .size()
    .reset_index(name='count')
)

gu_list = status_count['주소'].unique()
selected_gu = st.selectbox("구를 선택하세요", gu_list)

filtered_df = status_count[status_count['주소'] == selected_gu]

# 공급상태별 합계 계산
supply_status_summary = filtered_df.groupby('공급상태')['count'].sum()

fig = go.Figure(
    data=[go.Pie(
        labels=supply_status_summary.index,
        values=supply_status_summary.values,
        hole=0,  # 도넛 차트로 만들고 싶으면 0.4 등으로 조절
        marker=dict(colors=['#ff6666', '#6699ff'])
    )]
)

fig.update_layout(
    title_text=f"{selected_gu} 구 공급 상태 비율"
)

st.plotly_chart(fig)





##########################
# 지역별 직종 분포


# NCS_1별 수업 개수 계산
NCS_1_region = df.groupby(['주소', 'NCS_1']).size().reset_index(name='count')

# 주소별 구 리스트
gu_list = sorted(NCS_1_region['주소'].unique())

# NCS 코드 → 이름 매핑 (예시)
# 반드시 실제 코드에 맞게 ncs1_map 정의 필요
NCS_1_region['NCS_1_명'] = NCS_1_region['NCS_1'].map(ncs1_map)

# Streamlit UI
st.title("서울시 지역별 직종 분포")

selected_gu = st.selectbox("구를 선택하세요", gu_list)

# 선택된 구 필터링
data = NCS_1_region[NCS_1_region['주소'] == selected_gu]

# 직종별 count 정렬
data_sorted = data.sort_values(by='count', ascending=False)

# 상위 7개
top7 = data_sorted.head(7)

# 기타(etc) 합산
etc_count = data_sorted['count'].iloc[7:].sum()

# labels & values
labels = list(top7['NCS_1_명']) + ['기타(etc)']
values = list(top7['count']) + [etc_count]

# 파이차트 생성
fig1 = go.Figure(
    data=[go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(line=dict(color='white', width=2)),
        sort=False
    )]
)

fig1.update_layout(
    title=f"{selected_gu} 지역 직종 분포",
    height=500
)

# 출력
st.plotly_chart(fig1)
