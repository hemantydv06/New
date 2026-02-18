import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('cleaned_ayurdata.csv')
symptoms_list = pd.read_csv('symptom_list.csv')

st.title("🪔 AyurVaidya Assist")
st.info("❗ Not medical advice - consult doctor")

# Doctor check
if st.checkbox("✅ Seen doctor?"):
    st.error("Follow doctor first")
    st.stop()

# Symptoms
st.header("📋 Your Symptoms")
selected = []
for _, row in symptoms_list.iterrows():
   # ✅ CORRECT - UNIQUE KEYS
    if st.checkbox(row['symptom'], key=f"symptom_{i}"):  # i = loop index

        selected.append(row['symptom'])

if not selected:
    st.stop()

# Smart matching
df['text'] = df['symptoms'].fillna('') + ' ' + df['risk_factors'].fillna('')
tfidf = TfidfVectorizer(max_features=500)
disease_vecs = tfidf.fit_transform(df['text'])
user_vec = tfidf.transform([' '.join(selected)])
scores = cosine_similarity(user_vec, disease_vecs)[0]

# Results
for i in scores.argsort()[-3:][::-1]:
    if scores[i] > 0.1:
        row = df.iloc[i]
        st.markdown(f"**{row['disease']}** ({scores[i]:.0%} match)")
        with st.expander("🌿 Remedy"):
            st.write(f"Herbs: {row['ayurvedic_herbs']}")
            st.write(f"Recipe: {row['formulation']}")

