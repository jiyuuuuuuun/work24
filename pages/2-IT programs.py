import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

# # --- 1. 샘플 데이터 생성 ---
# # 실제 데이터프레임 'df1_unique'가 있다면 이 부분은 삭제하고 실제 데이터를 사용하세요.
# data = {
#     '3차분류': ['웹개발', '웹개발', '데이터분석', '데이터분석', 'UI/UX', 'UI/UX', '서버관리', '웹개발'],
#     '제목': ['과정A', '과정B', '과정C', '과정D', '과정E', '과정F', '과정G', '과정H'],
#     '만족도점수': [4.5, 4.7, 4.8, 4.6, 4.9, 4.7, 4.3, 4.5],
#     '정원_대비_신청률': [1.2, 1.5, 1.8, 1.3, 2.0, 1.6, 0.9, 1.4],
#     '실제훈련비': [3000000, 3200000, 4500000, 4200000, 3800000, 3500000, 2500000, 3100000],
#     '훈련기간_일': [90, 100, 120, 110, 95, 90, 80, 95]
# }
# df1_unique = pd.DataFrame(data)
# mask = df1_unique['3차분류'].notna()


df1_unique = pd.read_csv("훈련과정_전체데이터_ver4.csv")
mask = df1_unique['3차분류'].notna() # 예시를 위한 마스크

import streamlit as st
import re

# 제목
st.title("정보기술 직무 분류 체계")

# 분류 데이터 정의
categories = {

    "정보기술개발": [
        "SW아키텍처",
        "응용SW엔지니어링",
        "임베디드SW엔지니어링",
        "DB엔지니어링",
        "NW엔지니어링",
        "보안엔지니어링",
        "UI/UX엔지니어링",
        "시스템SW엔지니어링",
        "빅데이터플랫폼구축",
        "핀테크엔지니어링",
        "데이터아키텍처",
        "IoT시스템연동",
        "인프라스트럭쳐아키텍처구축",
        "클라우드솔루션아키텍처",
        "클라우드인프라스트럭쳐엔지니어링",
        "PaaS엔지니어링",
    ],

    "정보기술전략·계획": [
        "정보기술전략",
        "정보기술컨설팅",
        "정보기술기획",
        "SW제품기획",
        "빅데이터분석",
        "IoT융합서비스기획",
        "빅데이터기획",
        "핀테크기술기획",
    ],

    "인공지능": [
        "인공지능플랫폼구축",
        "인공지능서비스기획",
        "인공지능모델링",
        "인공지능서비스운영관리",
        "인공지능서비스구현",
        "인공지능학습데이터구축",
    ],

    "정보보호": [
        "정보보호관리·운영",
        "정보보호진단·분석",
        "보안사고분석대응",
        "정보보호암호·인증",
        "영상정보처리",
        "생체인식(바이오인식)",
        "디지털포렌식",
        "영상정보보안·운영",
        "OT보안",
        "클라우드 보안 관리·운영",
        "정보보호제품 시험·평가",
        "SW공급망보안",
        "모빌리티보안",
    ],


    "정보기술운영": [
        "IT시스템관리",
        "IT기술교육",
        "IT기술지원",
        "빅데이터운영·관리",
        "IoT시스템운영·관리",
        "데이터거래관리",
    ],

    "디지털트윈": [
        "디지털트윈기획",
        "디지털트윈설계",
        "디지털트윈구축",
    ],


    "정보기술관리": [
        "IT프로젝트관리",
        "IT품질보증",
        "IT테스트",
        "IT감리",
    ]
}


# --- 2. 데이터 집계 ---
agg_df = df1_unique[mask].groupby('3차분류').agg(
    훈련_개수=('제목', 'count'),
    만족도점수=('만족도점수', 'mean'),
    정원_대비_신청률=('정원_대비_신청률', 'mean'),
    실제훈련비=('실제훈련비', 'mean'),
    훈련기간_일=('훈련기간_일', 'mean')
).sort_values(by='훈련_개수', ascending=False) # 훈련 개수 순으로 정렬

agg_df['일_평균_훈련비'] = agg_df['실제훈련비'] / agg_df['훈련기간_일']


# --- 3. Streamlit 앱 구성 ---
st.set_page_config(layout="wide")
st.title('📚 IT 프로그램별 훈련 과정 분석')

# --- 4. 메인 막대그래프 (훈련 개수 기준) ---
st.header('프로그램별 훈련 개수')
# 그래프 생성
fig_main = px.bar(
    agg_df,
    x=agg_df.index,
    y='훈련_개수',
    title='2024년도 IT 훈련 과정 수'
)

# 생성된 그래프의 x축 제목 업데이트
fig_main.update_xaxes(title_text='IT 분류명')

# y축 제목 업데이트
fig_main.update_yaxes(title_text='프로그램 수')

st.plotly_chart(fig_main, use_container_width=True)

# 출력
for category, items in categories.items():
    clean_items = [re.sub(r'\(\d+\)', '', item).strip() for item in items]
    # '빅데이터플랫폼구축'에만 색상 적용
    colored_items = [f"<span style='color:red'>{item}</span>" if item == '빅데이터플랫폼구축' else item for item in clean_items]
    joined_items = ", ".join(colored_items)
    st.markdown(f"**{category}**: {joined_items}", unsafe_allow_html=True)



st.divider()

# --- 5. 모든 Hover 데이터를 그래프로 한 번에 시각화 ---
st.header('주요 지표 전체 비교')
st.markdown('각 주요 지표를 기준으로 모든 분류를 한눈에 비교합니다.')

# 3개의 컬럼을 만들어 각 그래프를 나란히 배치
g_col1, g_col2, g_col3 = st.columns(3)

with g_col1:
    # 만족도 점수 그래프 (높은 순)
    fig1 = px.bar(agg_df.sort_values('만족도점수', ascending=False),
                  x='만족도점수', y=agg_df.sort_values('만족도점수', ascending=False).index, orientation='h',
                  title='⭐ 평균 만족도 점수', labels={'y': '3차 분류'})
    st.plotly_chart(fig1, use_container_width=True)

agg_df['정원_대비_신청률_비율'] = agg_df['정원_대비_신청률'] / 100

with g_col2:
    fig2 = px.bar(
        agg_df.sort_values('정원_대비_신청률_비율', ascending=False),
        x='정원_대비_신청률_비율', y=agg_df.sort_values('정원_대비_신청률_비율', ascending=False).index, orientation='h',
        title='📈 평균 신청률', labels={'y': '3차 분류', '정원_대비_신청률_비율': '평균 신청률'}
    )
    fig2.update_xaxes(tickformat=".0%")
    st.plotly_chart(fig2, use_container_width=True)


with g_col3:
    fig3 = px.bar(
        agg_df.sort_values('일_평균_훈련비', ascending=False),
        x='일_평균_훈련비',
        y=agg_df.sort_values('일_평균_훈련비', ascending=False).index,
        orientation='h',
        title='💰 일 평균 훈련비',
        labels={'y': '3차 분류', '일_평균_훈련비': '일 평균 훈련비(원)'}
    )
    fig3.update_xaxes(tickformat=",.0f")  # 천 단위 쉼표, 소수점 없음
    st.plotly_chart(fig3, use_container_width=True)


st.divider()

# --- 6. 분류별 상세 지표 확인 (훈련 개수 포함) ---
st.header('분류별 상세 지표 확인')

selected_category = st.selectbox(
    '분석할 3차 분류를 선택하세요:',
    options=agg_df.index
)

selected_data = agg_df.loc[selected_category]

# 4개의 컬럼을 만들어 메트릭 표시 (훈련 개수 추가)
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    st.metric(
        label=f"🔢 훈련 개수",
        value=f"{selected_data['훈련_개수']:.0f} 개"
    )

with m_col2:
    st.metric(
        label=f"⭐ 평균 만족도 점수",
        value=f"{selected_data['만족도점수']:.2f} 점"
    )

with m_col3:
    st.metric(
        label=f"📈 평균 신청률",
        value=f"{selected_data['정원_대비_신청률'] :.2f} %"
    )

with m_col4:
    st.metric(
        label=f"💰 일 평균 훈련비",
        value=f"{selected_data['일_평균_훈련비']:,.0f} 원"
    )

# 전체 데이터 테이블 표시 (포맷팅에 '훈련_개수' 추가)
st.subheader(f"'{selected_category}' 분류의 전체 데이터")
st.dataframe(selected_data.to_frame().T.style.format({
    '훈련_개수': '{:,.0f} 개',
    '만족도점수': '{:.2f}',
    '정원_대비_신청률_비율': '{:.2%}',
    '실제훈련비': '{:,.0f} 원',
    '훈련기간_일': '{:.0f} 일',
    '일_평균_훈련비': '{:,.0f} 원'
}), use_container_width=True)
