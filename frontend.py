import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
from datetime import date, datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="CityOps HRMS", page_icon="🌃", layout="wide")

# ⚠️ REPLACE WITH YOUR ACTUAL RENDER URL
API_URL = "https://hrms-lite-ac8r.onrender.com"

# --- ASSETS (Safe Loader) ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Futuristic City Animations
lottie_city = load_lottieurl("https://lottie.host/8040d77d-741c-4b55-871d-720496839077/1r4i9z6l8o.json") # Smart City
lottie_connection = load_lottieurl("https://lottie.host/5b090740-459d-4786-8152-4740e5317768/0j5Q1k2w2N.json") # Network lines
lottie_scan = load_lottieurl("https://lottie.host/a80d5885-26bf-466d-974a-1017e80f2d9e/9Z9V3X5s4T.json") # Scanner
lottie_success = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# --- CUSTOM CSS (THE "CYBERPUNK CITY" LOOK) ---
st.markdown("""
    <style>
    /* 1. CUSTOM MOUSE CURSOR (Crosshair Style) */
    * {
        cursor: crosshair !important;
    }
    button:hover {
        cursor: pointer !important;
    }

    /* 2. MOVING BACKGROUND ANIMATION */
    @keyframes moveBackground {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        /* High-Res Night City Image */
        background-image: url("https://images.unsplash.com/photo-1519608487953-e999c86e7455?q=80&w=2070&auto=format&fit=crop");
        background-size: 120% 120%; /* Zoomed in slightly to allow movement */
        background-position: center;
        background-attachment: fixed;
        animation: moveBackground 30s ease infinite; /* The "Moving" Effect */
    }
    
    /* 3. GLASS CARDS with NEON GLOW */
    .block-container { padding-top: 2rem; }
    div[data-testid="stExpander"], div.stDataFrame, div.stForm {
        background: rgba(10, 25, 47, 0.85); /* Deep Blue Transparent */
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 12px;
        border: 1px solid rgba(100, 255, 218, 0.3); /* Cyan Border */
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    }
    
    /* Hover Effect on Cards (Glow Intensity) */
    div[data-testid="stExpander"]:hover, div.stForm:hover {
        border-color: #FF6B6B; /* Switch to Neon Orange on hover */
        box-shadow: 0 0 25px rgba(255, 107, 107, 0.4);
        transition: all 0.3s ease;
    }

    /* 4. TYPOGRAPHY (Tech Font) */
    h1, h2, h3 {
        color: #E6F1FF !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px rgba(100, 255, 218, 0.5);
        font-weight: 900;
        letter-spacing: 1px;
    }
    p, label, .stMarkdown, .stRadio label {
        color: #8892b0 !important;
        font-family: 'Verdana', sans-serif;
    }
    
    /* 5. METRICS (Neon Numbers) */
    div[data-testid="stMetricValue"] {
        color: #64FFDA !important; /* Neon Cyan */
        text-shadow: 0 0 15px rgba(100, 255, 218, 0.8);
    }
    div[data-testid="stMetricLabel"] {
        color: #FF6B6B !important; /* Neon Orange */
    }

    /* 6. BUTTONS (Futuristic) */
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.6rem 1.5rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: bold !important;
        clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%); /* Sci-Fi Shape */
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.6);
    }
    
    /* 7. INPUTS (Dark Mode) */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        background-color: #112240 !important;
        color: #64FFDA !important;
        border: 1px solid #233554 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(2, 12, 27, 0.95);
        border-right: 1px solid #233554;
    }
    
    /* Header visibility adjustment */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if lottie_city:
        st_lottie(lottie_city, height=180)
    
    st.markdown("## 🏙️ CITY OPS")
    st.markdown("### URBAN COMMAND CENTER")
    
    menu = st.radio("SYSTEM NAVIGATION", ["Dashboard", "Personnel", "Activity Logs"])
    st.markdown("---")
    st.caption("STATUS: 🟢 NETWORK SECURE")

# --- PAGE 1: DASHBOARD ---
if menu == "Dashboard":
    st.title("📡 SYSTEM OVERVIEW")
    st.markdown("REAL-TIME CITY METRICS")
    
    try:
        emp_res = requests.get(f"{API_URL}/employees/")
        if emp_res.status_code == 200:
            df = pd.DataFrame(emp_res.json())
            
            if not df.empty:
                # Top Level Metrics
                c1, c2 = st.columns(2)
                
                with c1:
                    st.metric("ACTIVE UNITS", len(df), "ONLINE")
                
                with c2:
                    top_dept = df['department'].value_counts().idxmax()
                    st.metric("PRIMARY SECTOR", top_dept)
                
                st.markdown("---")
                
                # Visualizations
                col1, col2 = st.columns([2,1])
                
                with col1:
                    st.subheader("SECTOR ALLOCATION")
                    # Cyberpunk Palette
                    fig = px.pie(df, names='department', hole=0.7, 
                                 color_discrete_sequence=["#64FFDA", "#FF6B6B", "#BD34FE", "#2196F3"])
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", 
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#E6F1FF",
                        showlegend=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("LIVE FEED")
                    if lottie_connection:
                        st_lottie(lottie_connection, height=200)

            else:
                st.info("NO DATA STREAM.")
                if lottie_scan:
                    st_lottie(lottie_scan, height=200)
    except:
        st.error("❌ SIGNAL LOST. CHECK CONNECTION.")

# --- PAGE 2: PERSONNEL ---
elif menu == "Personnel":
    st.title("🕵️ PERSONNEL DATABASE")
    
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
        if st.button("🔄 SYNC DATA"): st.rerun()
        
        try:
            res = requests.get(f"{API_URL}/employees/")
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data)
                    
                    # BONUS: Total Present Calc
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

                    st.dataframe(
                        df[["emp_id_str", "name", "department", "MISSIONS COMPLETE"]], 
                        use_container_width=True, 
                        hide_index=True
                    )
                    
                    with st.expander("⚠️ DISAVOW UNIT (DELETE)"):
                        del_id = st.selectbox("SELECT UNIT ID", df['emp_id_str'])
                        if st.button("CONFIRM TERMINATION"):
                            requests.delete(f"{API_URL}/employees/{del_id}")
                            st.rerun()
        except:
            st.warning("DATABASE ENCRYPTED/UNAVAILABLE")

# --- PAGE 3: ACTIVITY LOGS ---
elif menu == "Activity Logs":
    st.title("🛰️ ACTIVITY LOGS")
    
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
                        # Neon Colors
                        colors = {"Present": "#64FFDA", "Absent": "#FF6B6B"} 
                        fig = px.bar(df_h, x='date', y='status', color='status', 
                                     color_discrete_map=colors, title="OPERATIONAL UPTIME")
                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)", 
                            plot_bgcolor="rgba(0,0,0,0)",
                            font_color="#E6F1FF"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("NO RECORDS FOUND.")
                else:
                    if lottie_scan:
                        st_lottie(lottie_scan, height=200)
    except:
        st.error("DATA LINK SEVERED")
