import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
from datetime import date, datetime
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Ethara.AI HRMS", layout="wide")

# ⚠️ REPLACE WITH YOUR ACTUAL RENDER URL
API_URL = "https://hrms-lite-ac8r.onrender.com"

# --- SESSION STATE ---
if 'app_mode' not in st.session_state:
    st.session_state['app_mode'] = 'intro'

# --- ASSETS ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Animations
lottie_city = load_lottieurl("https://lottie.host/8040d77d-741c-4b55-871d-720496839077/1r4i9z6l8o.json")
lottie_connection = load_lottieurl("https://lottie.host/5b090740-459d-4786-8152-4740e5317768/0j5Q1k2w2N.json")
lottie_scan = load_lottieurl("https://lottie.host/a80d5885-26bf-466d-974a-1017e80f2d9e/9Z9V3X5s4T.json")
# Tech Loader
lottie_loader = load_lottieurl("https://lottie.host/b2b95b8d-2911-4712-ba26-1d11394589d9/5q1q6f1e8K.json") 

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* 1. CUSTOM CURSOR */
    * {
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M0,0 L16,0 L32,12 L32,32 L12,32 L0,20 Z" fill="%23222" stroke="%2364FFDA" stroke-width="1"/><circle cx="16" cy="16" r="6" fill="none" stroke="%2364FFDA" stroke-width="2"/></svg>') 0 0, auto !important;
    }
    
    /* 2. BACKGROUND ANIMATION */
    @keyframes moveBackground {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background-image: url("https://images.unsplash.com/photo-1519608487953-e999c86e7455?q=80&w=2070&auto=format&fit=crop");
        background-size: 120% 120%;
        background-position: center;
        background-attachment: fixed;
        animation: moveBackground 40s ease infinite;
    }
    
    /* 3. MENU BUTTON VISIBILITY */
    header[data-testid="stHeader"] {
        background: transparent !important;
        pointer-events: none;
    }
    header[data-testid="stHeader"] > div {
        pointer-events: auto;
    }
    button[kind="header"] {
        color: #64FFDA !important;
        background: rgba(0,0,0,0.5) !important;
        border-radius: 50%;
    }

    /* 4. GLASS CARDS */
    .block-container { padding-top: 3rem; }
    div[data-testid="stExpander"], div.stDataFrame, div.stForm {
        background: rgba(10, 25, 47, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 12px;
        border: 1px solid rgba(100, 255, 218, 0.3);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    }
    
    /* 5. TYPOGRAPHY */
    h1, h2, h3 {
        color: #E6F1FF !important;
        font-family: 'Verdana', sans-serif;
        text-shadow: 0 0 10px rgba(100, 255, 218, 0.5);
    }
    p, label, .stMarkdown, .stRadio label {
        color: #8892b0 !important;
        font-family: 'Verdana', sans-serif;
    }
    
    /* 6. NEON CYBER BUTTONS */
    .stButton>button {
        background: linear-gradient(45deg, #64FFDA, #2196F3) !important;
        color: #0a192f !important;
        border: none !important;
        clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
        font-weight: 900 !important;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(100, 255, 218, 0.5);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(100, 255, 218, 0.9);
        color: white !important;
    }
    
    /* 7. INPUTS */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        background-color: #112240 !important;
        color: #64FFDA !important;
        border: 1px solid #233554 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(2, 12, 27, 0.95);
        border-right: 1px solid #233554;
    }
    
    /* Logo Styling */
    .company-logo {
        font-size: 40px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 5px;
        font-family: 'Verdana', sans-serif;
    }
    .company-sub {
        font-size: 12px;
        color: #64FFDA;
        text-align: center;
        letter-spacing: 3px;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    
    /* INTRO PAGE SPECIFIC */
    .intro-title {
        font-size: 80px;
        font-weight: 900;
        text-align: center;
        background: -webkit-linear-gradient(#64FFDA, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px;
        text-shadow: 0 0 30px rgba(100, 255, 218, 0.3);
    }
    .intro-subtitle {
        font-size: 20px;
        text-align: center;
        color: #E6F1FF;
        letter-spacing: 8px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE LOGIC
# ==========================================

if st.session_state['app_mode'] == 'intro':
    # --- INTRO LANDING PAGE ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    intro_holder = st.empty()
    
    with intro_holder.container():
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div class="intro-title">Ethara.AI</div>', unsafe_allow_html=True)
            st.markdown('<div class="intro-subtitle">ADVANCED HUMAN SYSTEMS</div>', unsafe_allow_html=True)
            
            if lottie_city:
                st_lottie(lottie_city, height=350, key="intro_city")
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            b1, b2, b3 = st.columns([1, 2, 1])
            with b2:
                init_btn = st.button("INITIALIZE SYSTEM", use_container_width=True)
    
    # --- LOADING BAR ANIMATION ---
    if init_btn:
        intro_holder.empty()
        
        with st.empty():
            # Show high-tech loader above bar
            if lottie_loader:
                st_lottie(lottie_loader, height=150, key="loader")
            elif lottie_scan:
                st_lottie(lottie_scan, height=150, key="loader")
                
            # The Loading Bar
            progress_bar = st.progress(0, text="CONNECTING...")
            
            for i in range(100):
                time.sleep(0.02) # Speed of loading
                # Update text at specific percentages for effect
                if i < 40:
                    txt = "CONNECTING..."
                elif i < 80:
                    txt = "VERIFYING CREDENTIALS..."
                else:
                    txt = "ACCESS GRANTED..."
                
                progress_bar.progress(i + 1, text=txt)
            
            time.sleep(0.5) # Short pause at 100%
            
        # Switch to Main App
        st.session_state['app_mode'] = 'main'
        st.rerun()

else:
    # --- MAIN APPLICATION (Sidebar + Pages) ---
    
    with st.sidebar:
        if lottie_city:
            st_lottie(lottie_city, height=180, key="sidebar_city")
        
        st.markdown('<div class="company-logo">Ethara.AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="company-sub">HUMAN RESOURCES</div>', unsafe_allow_html=True)
        
        menu = st.radio("SYSTEM NAVIGATION", ["Dashboard", "Personnel", "Activity Logs"])
        st.markdown("---")
        st.caption("STATUS: NETWORK SECURE")

    # --- PAGE 1: DASHBOARD ---
    if menu == "Dashboard":
        st.title("ETHARA SYSTEM OVERVIEW")
        st.markdown("REAL-TIME METRICS")
        
        try:
            emp_res = requests.get(f"{API_URL}/employees/")
            if emp_res.status_code == 200:
                df = pd.DataFrame(emp_res.json())
                
                if not df.empty:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("ACTIVE UNITS", len(df), "ONLINE")
                    with c2:
                        top_dept = df['department'].value_counts().idxmax()
                        st.metric("PRIMARY SECTOR", top_dept)
                    
                    st.markdown("---")
                    col1, col2 = st.columns([2,1])
                    
                    with col1:
                        st.subheader("SECTOR ALLOCATION")
                        fig = px.pie(df, names='department', hole=0.7, 
                                     color_discrete_sequence=["#64FFDA", "#FF6B6B", "#BD34FE", "#2196F3"])
                        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E6F1FF")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.subheader("LIVE FEED")
                        if lottie_connection:
                            st_lottie(lottie_connection, height=200, key="dash_conn")
                else:
                    st.info("NO DATA STREAM.")
                    if lottie_scan:
                        st_lottie(lottie_scan, height=200, key="dash_scan")
        except:
            st.error("SIGNAL LOST. CHECK CONNECTION.")

    # --- PAGE 2: PERSONNEL ---
    elif menu == "Personnel":
        st.title("PERSONNEL DATABASE")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.subheader("ENLIST UNIT")
            with st.form("add_form"):
                e_id = st.text_input("UNIT ID")
                name = st.text_input("OPERATIVE NAME")
                email = st.text_input("SECURE COMMS (EMAIL)")
                dept = st.selectbox("ASSIGNMENT", ["Cyber Security", "Infrastructure", "Field Ops", "Intel", "Admin"])
                submit = st.form_submit_button("UPLOAD DATA")
                
                if submit:
                    if e_id and name:
                        res = requests.post(f"{API_URL}/employees/", json={
                            "emp_id_str": e_id, "name": name, "email": email, "department": dept
                        })
                        if res.status_code == 200:
                            st.success("UNIT REGISTERED")
                            st.rerun()
                        else:
                            st.error("REGISTRATION ERROR")

        with c2:
            st.subheader("UNIT MANIFEST")
            if st.button("SYNC DATA"): st.rerun()
            
            try:
                res = requests.get(f"{API_URL}/employees/")
                if res.status_code == 200:
                    data = res.json()
                    if data:
                        df = pd.DataFrame(data)
                        attendance_counts = []
                        for eid in df['emp_id_str']:
                            try:
                                att_res = requests.get(f"{API_URL}/attendance/{eid}")
                                if att_res.status_code == 200:
                                    att_data = att_res.json()
                                    present_count = sum(1 for x in att_data if x['status'] == 'Present')
                                    attendance_counts.append(present_count)
                                else:
                                    attendance_counts.append(0)
                            except:
                                attendance_counts.append(0)
                        df['MISSIONS COMPLETE'] = attendance_counts

                        st.dataframe(df[["emp_id_str", "name", "department", "MISSIONS COMPLETE"]], use_container_width=True, hide_index=True)
                        
                        with st.expander("DISAVOW UNIT"):
                            del_id = st.selectbox("SELECT UNIT ID", df['emp_id_str'])
                            if st.button("CONFIRM TERMINATION"):
                                requests.delete(f"{API_URL}/employees/{del_id}")
                                st.rerun()
            except:
                st.warning("DATABASE ENCRYPTED")

    # --- PAGE 3: LOGS ---
    elif menu == "Activity Logs":
        st.title("ACTIVITY LOGS")
        
        try:
            res = requests.get(f"{API_URL}/employees/")
            if res.status_code == 200 and res.json():
                emps = res.json()
                emp_map = {e['name']: e['emp_id_str'] for e in emps}
                
                col1, col2 = st.columns([1,2])
                with col1:
                    st.subheader("UPDATE STATUS")
                    sel_name = st.selectbox("SELECT OPERATIVE", list(emp_map.keys()))
                    sel_id = emp_map[sel_name]
                    d = st.date_input("MISSION DATE", date.today())
                    stat = st.radio("STATUS", ["ACTIVE", "MIA"], horizontal=True)
                    final_stat = "Present" if stat == "ACTIVE" else "Absent"
                    
                    if st.button("TRANSMIT LOG"):
                        requests.post(f"{API_URL}/attendance/", json={
                            "emp_id_str": sel_id, "date": str(d), "status": final_stat
                        })
                        st.success("LOG SECURED")

                with col2:
                    st.subheader("MISSION HISTORY")
                    use_filter = st.checkbox("Apply Time Filter")
                    hist = requests.get(f"{API_URL}/attendance/{sel_id}")
                    if hist.status_code == 200 and hist.json():
                        df_h = pd.DataFrame(hist.json())
                        if use_filter:
                            start_d = st.date_input("Start Date", date.today())
                            df_h['date'] = pd.to_datetime(df_h['date']).dt.date
                            df_h = df_h[df_h['date'] >= start_d]
                        
                        if not df_h.empty:
                            colors = {"Present": "#64FFDA", "Absent": "#FF6B6B"}
                            fig = px.bar(df_h, x='date', y='status', color='status', 
                                         color_discrete_map=colors, title="OPERATIONAL UPTIME")
                            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E6F1FF")
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("NO RECORDS FOUND.")
                    else:
                        if lottie_scan:
                            st_lottie(lottie_scan, height=200, key="log_scan")
        except:
            st.error("DATA LINK SEVERED")
