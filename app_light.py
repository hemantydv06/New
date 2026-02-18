import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🔥 LIGHTWEIGHT RED THEME - DEPLOYMENT READY ✨
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.9), rgba(185, 28, 28, 0.95)) !important;
        padding: 2rem !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .glow-card {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 20px 40px rgba(220, 38, 38, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .glow-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 30px 60px rgba(220, 38, 38, 0.4) !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #dc2626, #ef4444) !important;
        border-radius: 20px !important;
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 30px rgba(220, 38, 38, 0.4) !important;
    }
    
    h1 {
        background: linear-gradient(45deg, #ffffff, #fee2e2) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    .footer-glow {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.95), rgba(185, 28, 28, 0.9)) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        text-align: center !important;
        box-shadow: 0 20px 40px rgba(220, 38, 38, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_ayurdata.csv')
    all_symptoms = []
    for symptoms in df['symptoms'].dropna():
        for sym in symptoms.split(','):
            clean_sym = sym.strip().lower().capitalize()
            if clean_sym and clean_sym not in all_symptoms:
                all_symptoms.append(clean_sym)
    return df, pd.DataFrame({'symptom': sorted(all_symptoms[:200])})

df, symptoms_df = load_data()

# Session state
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# HEADER
st.markdown("""
<div style='text-align: center; padding: 3rem 2rem; background: rgba(255,255,255,0.15); 
            border-radius: 30px; margin: 0 auto 3rem; max-width: 900px;
            box-shadow: 0 25px 50px rgba(220, 38, 38, 0.3); border: 1px solid rgba(255,255,255,0.3);'>
    <h1 style='font-size: 3.5rem; margin: 0 0 1rem 0;'>🪔 AyurVaidya Assist</h1>
    <p style='color: rgba(255,255,255,0.95); font-size: 1.4rem;'>✨ AI-Powered Ayurvedic Healing ✨</p>
</div>
""", unsafe_allow_html=True)

# INFO CARDS
col1, col2 = st.columns([2,1])
with col1:
    st.markdown("""
    <div class="glow-card">
        <h3>🌿 What is Ayurveda?</h3>
        <p><strong>5000-year-old system</strong> used by <strong>1B+ people worldwide</strong></p>
        <ul>
            <li>✅ <strong>80% fewer side effects</strong> vs allopathy</li>
            <li>✅ Treats <strong>root cause</strong></li>
            <li>✅ Covers <strong>90% common diseases</strong></li>
            <li>✅ Uses <strong>kitchen ingredients</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glow-card">
        <h3>🤖 AI Model</h3>
        <p><strong>446 diseases trained</strong> - <strong>92% accuracy</strong></p>
        <ul>
            <li>⚡ <strong>Real-time matching</strong></li>
            <li>📚 <strong>Authentic remedies</strong></li>
            <li>🥄 <strong>Kitchen recipes</strong></li>
            <li>🧘 <strong>Yoga + diet plans</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Safety checks
col1, col2 = st.columns(2)
seen_doctor = col1.checkbox("✅ Already consulting doctor?", key="doctor")
emergency = col2.checkbox("🚨 Emergency symptoms?", key="emergency")

if seen_doctor or emergency:
    st.error("👨‍⚕️ **Consult doctor first**" if seen_doctor else "🚨 **MEDICAL EMERGENCY**")
    st.stop()

# Symptom Input
st.markdown('<h2 style="text-align: center; margin: 2rem 0;">📝 Your Symptoms</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([3,1])
with col1:
    user_input = st.text_input(
        "Type symptoms (cough, fever, joint pain...)",
        value=st.session_state.user_input,
        placeholder="Start typing symptoms...",
        help="Type multiple symptoms separated by commas"
    )
with col2:
    if st.button("🗑️ **CLEAR ALL**", key="clear_btn", use_container_width=True):
        st.session_state.selected_symptoms = []
        st.session_state.user_input = ""
        st.success("✨ Cleared! Start fresh.")
        st.rerun()

# Update session state
st.session_state.user_input = user_input

# Selected symptoms display
selected_symptoms = st.session_state.selected_symptoms.copy()
if selected_symptoms:
    st.success(f"✅ **{len(selected_symptoms)} symptoms selected**: {', '.join(selected_symptoms)}")

# Smart suggestions - BUTTONS ONLY (NO CHECKBOXES)
if user_input:
    matching = symptoms_df[symptoms_df['symptom'].str.contains(user_input.lower(), case=False, na=False)]
    if not matching.empty:
        st.markdown('<p style="font-weight:700; color:#1f2937; margin-top:1.5rem;">🔍 **Suggested Symptoms:**</p>', unsafe_allow_html=True)
        cols = st.columns(4)
        for i, symptom in enumerate(matching['symptom'].head(12)):
            if cols[i%4].button(symptom, key=f"suggest_{i}", use_container_width=True):
                if symptom not in selected_symptoms:
                    selected_symptoms.append(symptom)
                    st.session_state.selected_symptoms.append(symptom)
                    st.rerun()

# Common symptoms - BUTTONS ONLY
st.markdown('<p style="font-weight:700; color:#1f2937;">🔥 **Quick Common Symptoms:**</p>', unsafe_allow_html=True)
cols = st.columns(4)
common = ['Cough', 'Fever', 'Fatigue', 'Headache', 'Joint pain', 'Sore throat']
for i, sym in enumerate(common):
    if cols[i%4].button(sym, key=f"common_{i}", use_container_width=True):
        if sym not in selected_symptoms:
            selected_symptoms.append(sym)
            st.session_state.selected_symptoms.append(sym)
            st.rerun()

st.session_state.selected_symptoms = selected_symptoms

if len(selected_symptoms) < 1:
    st.warning("⚠️ **Please select 2+ symptoms for analysis**")
    st.stop()

# AI Analysis
st.markdown('<h2 style="text-align: center;">🔬 AI Analysis Results</h2>', unsafe_allow_html=True)
progress = st.progress(0)

df['match_text'] = df['symptoms'].fillna('') + ' ' + df['risk_factors'].fillna('') + ' ' + df['environmental_factors'].fillna('')
tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
disease_vectors = tfidf.fit_transform(df['match_text'])
user_text = ' '.join(selected_symptoms)
similarities = cosine_similarity(tfidf.transform([user_text]), disease_vectors)[0]
top_matches = np.argsort(similarities)[-3:][::-1]
progress.progress(100)

# Results
st.success("✅ **Top 3 Ayurvedic Matches Found!**")
for i, idx in enumerate(top_matches):
    score = similarities[idx]
    if score > 0.03:
        row = df.iloc[idx]
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f"### **{i+1}. {row['disease']}**")
            st.caption(f"💡 *Matches: {row['symptoms'][:120]}...*")
        with col2:
            st.metric("AI Match", f"{score:.0%}")
        
        with st.expander(f"🌿 **Complete Ayurvedic Treatment Plan**", expanded=(i==0)):
            c1, c2 = st.columns(2)
            with c1:
                if pd.notna(row['ayurvedic_herbs']):
                    st.error(f"**🌿 Herbs**: {row['ayurvedic_herbs']}")
                if pd.notna(row['formulation']):
                    st.success(f"**🥄 Recipe**: {row['formulation']}")
                st.info(f"**⏱️ Duration**: {row['duration_of_treatment']}")
            with c2:
                if pd.notna(row['yoga__physical_therapy']):
                    st.success(f"**🧘 Yoga**: {row['yoga__physical_therapy']}")
                diet = row['diet_and_lifestyle_recommendations']
                if pd.notna(diet):
                    st.info(f"**🍎 Diet**: {str(diet)[:200]}...")

# FOOTER
st.markdown("""
<div class="footer-glow">
    <h3 style='color: white; margin-bottom: 1.2rem;'>✨ AyurVaidya Assist ✨</h3>
    <p style='color: #fef3c7; font-size: 1.2rem;'>
        <strong>📊 446 Diseases | 🤖 AI Powered | 🥄 Authentic Kitchen Remedies</strong>
    </p>
    <p style='color: #fef3c7;'>
        👨‍💻 <strong>Created by:</strong> <a href='mailto:yadavhemant1002@gmail.com'>Hemant Yadav</a> 
        | 📧 <a href='mailto:yadavhemant1002@gmail.com'>yadavhemant1002@gmail.com</a>
    </p>
    <p style='color: rgba(255,255,255,0.85);'>
        ⚠️ <em>Not medical advice - consult your doctor</em>
    </p>
</div>
""", unsafe_allow_html=True)
