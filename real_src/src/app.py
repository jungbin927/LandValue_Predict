import nest_asyncio
nest_asyncio.apply()


import streamlit as st
import os
from glob import glob
import pandas as pd

st.sidebar.title("공시지가 시각화 전용 웹페이지")

# 1단계 선택
main_option = st.sidebar.selectbox(
    "1단계: 확인할 시각화 고르기",
    [
        "",
        "1. TableOne, t-SNE, UMAP",
        "2. CCA, 통계분석",
        "3. 머신러닝 성능 확인",
        "4. Odds Ratio, CI, p-value",
        "5. SHAP, LIME",
        "6. Residual 분석",
        "7. 지역별 성능 확인"
    ]
)

# 2단계 목록
sub_option_dict = {
    "1. TableOne, t-SNE, UMAP": ["TableOne", "t-SNE", "UMAP"],
    "2. CCA, 통계분석": ["CCA 결과", "Kruskal-Wallis 검정 결과"],
    "3. 머신러닝 성능 확인": ["다중공선성 미제거 버전", "다중공선성 제거 버전", "적대적 공격 버전"],
    "4. Odds Ratio, CI, p-value": ["오즈비 상위 10개", "오즈비 하위 10개"],
    "5. SHAP, LIME": ["SHAP Summary Plot", "SHAP Dependency Plot", "LIME 전체 기여도"],
    "6. Residual 분석": ["Residual Plot", "QQ Plot", "Actual vs Predicted"],
    "7. 지역별 성능 확인": ["성능 확인하기"]
}

if main_option and main_option in sub_option_dict:
    sub_option = st.sidebar.selectbox("2단계: 세부 시각화 고르기", sub_option_dict[main_option])

    st.title("📊 시각화 결과")

    # ✅ TableOne 결과를 HTML 테이블로 보여줌
    if sub_option == "TableOne":
        table_path = "../real_data/table1_result.xlsx"
        if os.path.exists(table_path):
            try:
                df = pd.read_excel(table_path, index_col=0)  
                st.markdown("#### 📋 TableOne 요약 통계")
                st.markdown(df.to_html(classes="table table-striped", border=0), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"📛 파일을 읽는 도중 오류 발생: {e}")
        else:
            st.warning("❗ TableOne 결과 파일이 존재하지 않습니다.")

    # ✅ SHAP Dependency Plot - 다중 이미지 출력
    elif sub_option == "SHAP Dependency Plot":
        st.subheader("🔍 SHAP Dependency Plot 전체 보기")

        shap_folder = "./image/shap"
        shap_files = sorted(glob(os.path.join(shap_folder, "*_shap_dependency.png")))

        n_cols = 2
        cols = st.columns(n_cols)

        for idx, path in enumerate(shap_files):
            col = cols[idx % n_cols]
            with col:
                varname = os.path.basename(path).replace("_shap_dependency.png", "")
                st.markdown(f"**📌 {varname}**", unsafe_allow_html=True)
                st.image(path, use_container_width=True)

            if (idx + 1) % n_cols == 0:
                cols = st.columns(n_cols)

    # ✅ 나머지 이미지 출력 처리
    else:
        image_map = {
            "t-SNE": "./image/t-sne.png",
            "UMAP": "./image/umap.png",
            "CCA 결과": ["./image/cca_1.png", "./image/cca_2.png"],
            "Kruskal-Wallis 검정 결과": "./image/kruskal.png",
            "다중공선성 미제거 버전": "./image/model_r2.png",
            "다중공선성 제거 버전": "./image/VIF_model_r2.png",
            "적대적 공격 버전": [
                "./image/adversarial_attack1.png",
                "./image/adversarial_attack2.png",
                "./image/adversarial_attack3.png"
            ],
            "오즈비 상위 10개": "./image/glm/GLM_odds_ratio_top10.png",
            "오즈비 하위 10개": "./image/glm/GLM_odds_ratio_under10.png",
            "SHAP Summary Plot": "./image/shap/shap_summary_plot.png",
            "LIME 전체 기여도": "./image/lime_importance_plot.png",
            "Residual Plot": "./image/residuals/Residual_plot.png",
            "QQ Plot": "./image/residuals/QQ_plot.png",
            "Actual vs Predicted": "./image/residuals/Actual_predict_Plot.png",
            "성능 확인하기": "./image/city_model_r2.png"
        }

        file_entry = image_map.get(sub_option)
        file_list = file_entry if isinstance(file_entry, list) else [file_entry]

        for path in file_list:
            if os.path.exists(path):
                st.image(path, use_container_width=True)
            else:
                st.warning(f"❗ 이미지가 존재하지 않아요: {path}")

else:
    st.sidebar.markdown("1단계를 먼저 선택해주세요.")
