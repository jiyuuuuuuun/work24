import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 불러오기
df = pd.read_csv(r"./훈련과정_전체데이터_ver3.csv")

# NCS 코드 전처리
df['NCS_코드'] = df['NCS_코드'].astype(str).str.zfill(8)
df['NCS_1'] = df['NCS_코드'].str[0:2]
df['NCS_2'] = df['NCS_코드'].str[2:4]
df['NCS_3'] = df['NCS_코드'].str[4:6]
df['NCS_4'] = df['NCS_코드'].str[6:8]

# 분류명 매핑
ncs1_dict = {
    '01': '사업관리', '02': '경영/회계/사무', '03': '금융/보험', '04': '교육/자연/사회과학',
    '05': '법률/경찰/소방/교도/국방', '06': '보건/의료', '07': '사회복지/종교', '08': '문화/예술/디자인/방송',
    '09': '운전/운송', '10': '영업판매', '11': '경비/청소', '12': '이용/숙박/여행/오락/스포츠',
    '13': '음식서비스', '14': '건설', '15': '기계', '16': '재료', '17': '화학/바이오',
    '18': '섬유/의복', '19': '전기/전자', '20': '정보통신', '21': '식품가공',
    '22': '인쇄/목재/가구/공예', '23': '환경/에너지/안전', '24': '농림어업'
}
df['NCS_1_분류명'] = df['NCS_1'].map(ncs1_dict)

# 불필요한 행 제거 및 파생변수 생성
df = df[df['수강신청인원'] > 0].reset_index(drop=True)
df['신청률'] = df['수강신청인원'] / df['정원']

# Streamlit 앱 시작
st.title("1차 직종별 만족도 상위 훈련과정")

# 사용자 선택
selected_name = st.selectbox("1차 직종을 선택하세요", list(ncs1_dict.values()))
selected_code = [code for code, name in ncs1_dict.items() if name == selected_name][0]

# 필터링 및 상위 10개
filtered = df[df['NCS_1'] == selected_code].copy()
top10 = filtered.sort_values(by='만족도점수', ascending=False).head(10)

# 텍스트 출력
st.write(f"### '{selected_name}' 분야의 만족도점수 Top 10")

# 테이블 출력
st.dataframe(
    top10[['제목', '만족도점수', '신청률', '수강신청인원', '정원', '주소']].reset_index(drop=True),
    use_container_width=True
)

# 🔶 Plotly 시각화
fig = px.bar(
    top10,
    x='제목',
    y='만족도점수',
    color='신청률',
    text='만족도점수',
    hover_data={
        '수강신청인원': True,
        '정원': True,
        '신청률': ':.2f',
        '만족도점수': True,
        '제목': False
    },
    labels={'만족도점수': '만족도 점수'},
    title=f"'{selected_name}' 분야 상위 10개 과정 만족도"
)

fig.update_traces(textposition='outside')
fig.update_layout(xaxis_tickangle=-45, height=500)

st.plotly_chart(fig, use_container_width=True)
