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

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""

# --- ASSETS ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None

# Animations
lottie_city = load_lottieurl("https://lottie.host/8040d77d-741c-4b55-871d-720496839077/1r4i9z6l8o.json")
lottie_connection = load_lottieurl("https://lottie.host/5b090740-459d-4786-8152-4740e5317768/0j5Q1k2w2N.json")
lottie_scan = load_lottieurl("https://lottie.host/a80d5885-26bf-466d-974a-1017e80f2d9e/9Z9V3X5s4T.json")
lottie_loader = load_lottieurl("https://lottie.host/b2b95b8d-2911-4712-ba26-1d11394589d9/5q1q6f1e8K.json") 

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* 1. CUSTOM CURSOR */
    * { cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M0,0 L16,0 L32,12 L32,32 L12,32 L0,20 Z" fill="%23222" stroke="%2364FFDA" stroke-width="1"/><circle cx="16" cy="16" r="6" fill="none" stroke="%2364FFDA" stroke-width="2"/></svg>') 0 0, auto !important; }
    
    /* 2. BACKGROUND */
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
    
    /* 3. MENU & BUTTONS */
    header[data-testid="stHeader"] { background: transparent !important; }
    .stButton>button {
        background: linear-gradient(45deg, #64FFDA, #2196F3) !important;
        color: #0a192f !important;
        border: none !important;
        font-weight: 900 !important;
        box-shadow: 0 0 10px rgba(100, 255, 218, 0.5);
    }
    
    /* 4. GLASS CARDS & INPUTS */
    div[data-testid="stExpander"], div.stDataFrame, div.stForm {
        background: rgba(10, 25, 47, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(100, 255, 218, 0.3);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        border-radius: 12px;
        padding: 20px;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        background-color: #112240 !important;
        color: #64FFDA !important;
        border: 1px solid #233554 !important;
    }
    
    /* 5. TYPOGRAPHY */
    h1, h2, h3 { color: #E6F1FF !important; font-family: 'Verdana', sans-serif; text-shadow: 0 0 10px rgba(100, 255, 218, 0.5); }
    p, label { color: #8892b0 !important; font-family: 'Verdana', sans-serif; }
    
    /* INTRO TITLES */
    .intro-title {
        font-size: 70px; font-weight: 900; text-align: center;
        background: -webkit-linear-gradient(#64FFDA, #2196F3);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 20px;
        text-shadow: 0 0 30px rgba(100, 255, 218, 0.3);
    }
    .company-logo { font-size: 30px; font-weight: bold; color: white; text-align: center; font-family: 'Verdana', sans-serif; }
    .company-sub { font-size: 10px; color: #64FFDA; text-align: center; letter-spacing: 3px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. INTRO & LOGIN PAGE
# ==========================================

if not st.session_state['logged_in']:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Placeholder for wiping content later
    login_holder = st.empty()
    
    with login_holder.container():
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div class="intro-title">Ethara.AI</div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align:center; color:#E6F1FF; letter-spacing:4px;">SECURE ACCESS GATEWAY</div>', unsafe_allow_html=True)
            
            if lottie_city:
                st_lottie(lottie_city, height=250, key="intro_city")

            # --- SECURE LOGIN FORM ---
            # Using st.form prevents the page from reloading while you type
            with st.form("login_form"):
                st.markdown("### 🔒 ADMIN CREDENTIALS")
                username = st.text_input("ADMIN ID", placeholder="Enter ID (e.g., admin)")
                password = st.text_input("ACCESS KEY", type="password", placeholder="Enter Password")
                
                # Centered Submit Button
                submitted = st.form_submit_button("INITIALIZE UPLINK", use_container_width=True)
                
                if submitted:
                    if username and password: # Simple check (accepts any input for now)
                        # Store credentials (temporarily)
                        st.session_state['temp_user'] = username
                        st.session_state['auth_success'] = True
                    else:
                        st.error("CREDENTIALS REQUIRED")

    # --- ANIMATION & REDIRECT ---
    if st.session_state.get('auth_success'):
        # Clear the login form
        login_holder.empty()
        
        # Show Loading Sequence
        with st.empty():
            if lottie_loader:
                st_lottie(lottie_loader, height=150, key="loader")
            else:
                st.info("ESTABLISHING CONNECTION...")
                
            progress_bar = st.progress(0, text="HANDSHAKE PROTOCOL INITIATED...")
            for i in range(100):
                time.sleep(0.015)
                if i == 40: txt = "VERIFYING BIOMETRICS..."
                elif i == 80: txt = "ACCESS GRANTED..."
                else: txt = "ENCRYPTING DATA STREAM..."
                progress_bar.progress(i + 1, text=txt)
            
        # Set persistent login state
        st.session_state['logged_in'] = True
        st.session_state['user_name'] = st.session_state['temp_user']
        st.rerun()

# ==========================================
# 2. MAIN APPLICATION (Dashboard)
# ==========================================

else:
    # --- SIDEBAR ---
    with st.sidebar:
        if lottie_city:
            st_lottie(lottie_city, height=150, key="sb_anim")
        
        st.markdown('<div class="company-logo">Ethara.AI</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="company-sub">OPERATOR: {st.session_state["user_name"].upper()}</div>', unsafe_allow_html=True)
        
        menu = st.radio("NAVIGATION", ["Dashboard", "Personnel", "Activity Logs"])
        
        st.markdown("---")
        # Logout Button
        if st.button("TERMINATE SESSION", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

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
                    c1.metric("ACTIVE UNITS", len(df), "ONLINE")
                    c2.metric("PRIMARY SECTOR", df['department'].value_counts().idxmax())
                    
                    st.markdown("---")
                    c_chart, c_feed = st.columns([2,1])
                    with c_chart:
                        fig = px.pie(df, names='department', hole=0.7, color_discrete_sequence=["#64FFDA", "#2196F3", "#FF6B6B"])
                        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E6F1FF")
                        st.plotly_chart(fig, use_container_width=True)
                    with c_feed:
                        st.subheader("LIVE FEED")
                        if lottie_connection: st_lottie(lottie_connection, height=200)
                else:
                    st.info("NO DATA STREAM.")
                    if lottie_scan: st_lottie(lottie_scan, height=200)
        except:
            st.error("SIGNAL LOST. CHECK CONNECTION.")

    # --- PAGE 2: PERSONNEL ---
    elif menu == "Personnel":
        st.title("PERSONNEL DATABASE")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.subheader("ENLIST UNIT")
            with st.form("add_emp_form"): # Use form here too!
                e_id = st.text_input("UNIT ID")
                name = st.text_input("OPERATIVE NAME")
                email = st.text_input("EMAIL")
                dept = st.selectbox("ASSIGNMENT", ["Cyber Security", "Infrastructure", "Field Ops", "Intel", "Admin"])
                submit = st.form_submit_button("UPLOAD DATA")
                
                if submit:
                    if e_id and name:
                        res = requests.post(f"{API_URL}/employees/", json={"emp_id_str": e_id, "name": name, "email": email, "department": dept})
                        if res.status_code == 200:
                            st.success("UNIT REGISTERED")
                            time.sleep(1) # Wait a sec so user sees success
                            st.rerun()
                        else:
                            st.error("ERROR")

        with c2:
            st.subheader("UNIT MANIFEST")
            if st.button("SYNC DATA"): st.rerun()
            try:
                res = requests.get(f"{API_URL}/employees/")
                if res.status_code == 200 and res.json():
                    df = pd.DataFrame(res.json())
                    st.dataframe(df[["emp_id_str", "name", "department"]], use_container_width=True, hide_index=True)
                    
                    with st.expander("DISAVOW UNIT"):
                        del_id = st.selectbox("SELECT ID", df['emp_id_str'])
                        if st.button("CONFIRM DELETE"):
                            requests.delete(f"{API_URL}/employees/{del_id}")
                            st.rerun()
            except:
                st.warning("DATABASE UNREACHABLE")

    # --- PAGE 3: LOGS ---
    elif menu == "Activity Logs":
        st.title("ACTIVITY LOGS")
        try:
            res = requests.get(f"{API_URL}/employees/")
            if res.status_code == 200 and res.json():
                emps = res.json()
                emp_map = {e['name']: e['emp_id_str'] for e in emps}
                
                c1, c2 = st.columns([1,2])
                with c1:
                    st.subheader("LOG ENTRY")
                    sel_name = st.selectbox("OPERATIVE", list(emp_map.keys()))
                    d = st.date_input("DATE", date.today())
                    stat = st.radio("STATUS", ["ACTIVE", "MIA"], horizontal=True)
                    if st.button("TRANSMIT LOG"):
                        requests.post(f"{API_URL}/attendance/", json={"emp_id_str": emp_map[sel_name], "date": str(d), "status": "Present" if stat=="ACTIVE" else "Absent"})
                        st.success("LOGGED")
                
                with c2:
                    st.subheader("HISTORY")
                    hist = requests.get(f"{API_URL}/attendance/{emp_map[sel_name]}")
                    if hist.status_code == 200 and hist.json():
                        df_h = pd.DataFrame(hist.json())
                        fig = px.bar(df_h, x='date', y='status', color='status', color_discrete_map={"Present": "#64FFDA", "Absent": "#FF6B6B"})
                        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E6F1FF")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("NO LOGS")
        except:
            st.error("DATA LINK SEVERED")
