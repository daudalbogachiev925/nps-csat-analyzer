import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API = os.getenv("API_URL", "http://api:8000")
st.set_page_config(page_title="NPS/CSAT", layout="wide")
st.title("NPS / CSAT Analyzer")

@st.cache_data(ttl=15)
def fetch(path): return requests.get(f"{API}{path}").json()
@st.cache_data(ttl=15)
def post(path): return requests.post(f"{API}{path}").json()

nps = fetch("/api/analytics/nps")
segments = fetch("/api/analytics/nps/by-segment")
csat = fetch("/api/analytics/csat")
dist = fetch("/api/analytics/distribution?survey_type=nps")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("NPS", nps["nps"])
c2.metric("Promoters", nps["promoters"])
c3.metric("Passives", nps["passives"])
c4.metric("Detractors", nps["detractors"])
c5.metric("CSAT", f"{csat['csat']}%")

st.subheader("Распределение оценок NPS")
if dist["distribution"]:
    dist_df = pd.DataFrame([
        {"score": k, "count": v} for k, v in sorted(dist["distribution"].items())
    ])
    st.plotly_chart(px.bar(dist_df, x="score", y="count"))

st.subheader("NPS по сегментам")
seg_df = pd.DataFrame([{"segment": s, "nps": v["nps"]}
                       for s, v in segments.items()])
if not seg_df.empty:
    st.plotly_chart(px.bar(seg_df, x="segment", y="nps"))

if st.button("Кластеризовать отзывы"):
    st.session_state["topics"] = post("/api/analytics/topics")

if st.button("Только детракторы"):
    st.session_state["topics"] = post("/api/analytics/topics?only_detractors=true")

if "topics" in st.session_state:
    st.subheader("Темы отзывов")
    for t in st.session_state["topics"]:
        st.write(f"**Кластер {t['cluster_id']}** ({t['size']} отзывов, "
                 f"avg score {t['avg_score']})")
        st.write(f"Термины: {', '.join(t['sample_terms'])}")
        st.write(f"Пример: {t['sample']}")
        st.divider()
