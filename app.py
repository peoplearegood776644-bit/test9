import streamlit as st
import pandas as pd
import time
import plotly.express as px
from datetime import datetime

# --- ADVANCED CONFIGURATION ---
st.set_page_config(
    page_title="AURORA ELITE | Unified Exam System",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LUXURY NEUMORPHIC CSS ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    :root {
        --gold: #D4AF37;
        --dark-bg: #0A0E14;
        --glass: rgba(255, 255, 255, 0.03);
    }

    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #0a0e14);
        font-family: 'Inter', sans-serif;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border-right: 1px solid var(--gold);
    }

    /* Luxury Card Design */
    .quiz-card {
        background: var(--glass);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        margin-bottom: 25px;
        transition: 0.4s ease;
    }
    .quiz-card:hover {
        border-color: var(--gold);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1);
    }

    /* Neon Titles */
    .mega-title {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(to right, #D4AF37, #F9E076);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 45px;
        font-weight: 900;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 10px;
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: var(--gold);
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #B8860B, #D4AF37) !important;
        color: #000 !important;
        border-radius: 50px !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        letter-spacing: 2px;
        border: none !important;
        padding: 0.75rem 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LOGIC (Session State) ---
if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
if 'db_mcqs' not in st.session_state: st.session_state.db_mcqs = []
if 'db_results' not in st.session_state: st.session_state.db_results = []
if 'start_time' not in st.session_state: st.session_state.start_time = None

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#D4AF37; text-align:center;'>AURORA PRO</h2>", unsafe_allow_html=True)
    st.divider()
    page = st.selectbox("Switch Workspace", ["🏠 Student Hall", "🔑 Teacher Vault", "📈 Analytics Hub"])
    
    st.divider()
    st.markdown("### 🛠 System Info")
    st.caption(f"Server Time: {datetime.now().strftime('%H:%M:%S')}")
    st.caption("Encryption: AES-256 Active")

# --- 🏠 STUDENT HALL ---
if page == "🏠 Student Hall":
    st.markdown('<h1 class="mega-title">EXAMINATION HALL</h1>', unsafe_allow_html=True)
    
    if not st.session_state.db_mcqs:
        st.warning("⚠️ The vault is currently locked. Waiting for teacher to broadcast questions.")
        st.info("Tip: Use the mobile link provided by your teacher to access the live session.")
    else:
        with st.form("exam_engine"):
            col1, col2 = st.columns([2, 1])
            with col1:
                name = st.text_input("FULL LEGAL NAME", placeholder="As per ID Card")
            with col2:
                id_num = st.text_input("STUDENT ID (Optional)")

            st.divider()
            
            student_data = {}
            for i, item in enumerate(st.session_state.db_mcqs):
                st.markdown(f"""
                <div class="quiz-card">
                    <span style="color:#D4AF37; font-size:12px;">QUESTION {i+1}</span>
                    <h3 style="margin-top:5px;">{item['Question']}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                options = [item['Option A'], item['Option B'], item['Option C'], item['Option D']]
                student_data[i] = st.radio(f"Select for Q{i+1}", options, key=f"ans_{i}", label_visibility="collapsed")
            
            submit = st.form_submit_button("LOCK ANSWERS & SUBMIT")
            
            if submit:
                if not name:
                    st.error("Access Denied: Name is required for certification.")
                else:
                    score = sum(1 for i, q in enumerate(st.session_state.db_mcqs) if student_data[i] == q['Answer'])
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.session_state.db_results.append({
                        "Timestamp": timestamp,
                        "Student": name,
                        "ID": id_num,
                        "Score": score,
                        "Total": len(st.session_state.db_mcqs),
                        "Percentage": f"{(score/len(st.session_state.db_mcqs))*100:.1f}%"
                    })
                    st.balloons()
                    st.success(f"Final Score Dispatched: {score}/{len(st.session_state.db_mcqs)}")

# --- 🔑 TEACHER VAULT ---
elif page == "🔑 Teacher Vault":
    st.markdown('<h1 class="mega-title">TEACHER COMMAND CENTER</h1>', unsafe_allow_html=True)
    
    password = st.text_input("Enter Master Access Key", type="password")
    if password == "teacher2024":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📤 Question Broadcaster")
            file = st.file_uploader("Drop MCQ Database (CSV)", type="csv")
            if file:
                df = pd.read_csv(file)
                st.session_state.db_mcqs = df.to_dict('records')
                st.success(f"LIVE: {len(df)} questions broadcasted to students.")
        
        with c2:
            st.markdown("### ⚙️ Session Controls")
            if st.button("Emergency Wipe (Clear All Results)"):
                st.session_state.db_results = []
                st.rerun()
            if st.button("Lock Quiz (Close Access)"):
                st.session_state.db_mcqs = []
                st.rerun()
    elif password:
        st.error("Unauthorized Entry Attempt.")

# --- 📈 ANALYTICS HUB ---
elif page == "📈 Analytics Hub":
    st.markdown('<h1 class="mega-title">ANALYTICS HUB</h1>', unsafe_allow_html=True)
    
    admin_key = st.text_input("Enter Admin Credentials", type="password")
    if admin_key == "admin123":
        if not st.session_state.db_results:
            st.info("No data streams detected. Waiting for student submissions.")
        else:
            res_df = pd.DataFrame(st.session_state.db_results)
            
            # --- DASHBOARD METRICS ---
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Submissions", len(res_df))
            avg_score = res_df['Score'].mean()
            m2.metric("Class Average", f"{avg_score:.2f}")
            m3.metric("Top Score", res_df['Score'].max())
            
            st.divider()
            
            # --- DATA VISUALIZATION ---
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### Score Distribution")
                fig = px.histogram(res_df, x="Score", color_discrete_sequence=['#D4AF37'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col_b:
                st.markdown("#### Live Submissions")
                st.dataframe(res_df, use_container_width=True)
            
            # EXPORT FEATURE
            csv_data = res_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 DOWNLOAD PERFORMANCE REPORT", csv_data, "Report.csv", "text/csv")
            
    elif admin_key:
        st.error("Access Revoked.")

# --- FOOTER ---
st.markdown("<br><br><p style='text-align:center; color:gray; font-size:10px;'>AURORA ENGINE v4.0 | BUILT FOR PROFESSIONAL EDUCATORS</p>", unsafe_allow_html=True)
