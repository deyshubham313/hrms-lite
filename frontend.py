import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="HRMS Galactica", page_icon="🪐", layout="wide")

# ⚠️ REPLACE WITH YOUR ACTUAL RENDER URL
API_URL = "https://hrms-lite-ac8r.onrender.com"

# --- ASSETS ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# Space-Themed Animations
lottie_astronaut = load_lottieurl("https://lottie.host/01303867-5120-41e1-8727-464a4b492372/2F8s6Zg8C6.json")
lottie_rocket = load_lottieurl("https://lottie.host/49348b6c-3101-443f-9130-9b54c86b2458/V55v7l4HlJ.json")
lottie_galaxy = load_lottieurl("https://lottie.host/5690558b-0714-419b-ab83-6d0e806c95c8/pY2tC8QW7r.json")

# --- CUSTOM CSS (THE "PRO" LOOK) ---
st.markdown("""
    <style>
    /* 1. THE SPACE BACKGROUND */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* 2. GLASSMORPHISM CARDS (Transparent Containers) */
    .block-container {
        padding-top: 2rem;
    }
    div[data-testid="stExpander"], div.stDataFrame, div.stForm {
        background: rgba(255, 255, 255, 0.05); /* Very transparent white */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* 3. NEON TEXT & TITLES */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 0 0 10px #FF2E63, 0 0 20px #FF2E63; /* Neon Pink Glow */
        font-family: 'Courier New', Courier, monospace;
    }
    p, label, .stMarkdown {
        color: #E0E0E0 !important;
    }

    /* 4. FUTURISTIC BUTTONS */
    .stButton>button {
        background: transparent !important;
        color: #FF2E63 !important; /* Neon Red text */
        border: 2px solid #FF2E63 !important;
        border-radius: 30px !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: #FF2E63 !important;
        color: white !important;
        box-shadow: 0 0 15px #FF2E63, 0 0 30px #FF2E63; /* Glow on hover */
        transform: scale(1.05);
    }
    
    /* 5. INPUT FIELDS */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 10px;
    }
    
    /* Hide default header */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Dark Glass) ---
with st.sidebar:
    st_lottie(lottie_astronaut, height=180)
    st.markdown("## 🛸 COMMAND CENTER")
    menu = st.radio("", ["Mission Control", "Crew Management", "Flight Logs"])
    
    st.markdown("---")
    st.info("System Status: 🟢 ONLINE")

# --- PAGE 1: DASHBOARD (Mission Control) ---
if menu == "Mission Control":
    st.title("🚀 MISSION CONTROL")
    st.markdown("### HRMS GALACTICA DASHBOARD")
    
    try:
        emp_res = requests.get(f"{API_URL}/employees/")
        if emp_res.status_code == 200:
            df = pd.DataFrame(emp_res.json())
            
            if not df.empty:
                # Metrics using Glass Cards
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"<h1 style='text-align:center; font-size: 60px;'>{len(df)}</h1><p style='text-align:center'>ACTIVE CREW</p>", unsafe_allow_html=True)
                
                top_dept = df['department'].value_counts().idxmax()
                c2.markdown(f"<h1 style='text-align:center; font-size: 40px;'>{top_dept}</h1><p style='text-align:center'>DOMINANT SECTOR</p>", unsafe_allow_html=True)
                
                # Charts
                col1, col2 = st.columns([2,1])
                with col1:
                    # Dark Mode Chart
                    fig = px.pie(df, names='department', title='SECTOR DISTRIBUTION', 
                                 color_discrete_sequence=px.colors.sequential.Plasma, hole=0.5)
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                     st_lottie(lottie_rocket, height=200)

            else:
                st.warning("NO CREW DETECTED. INITIATE RECRUITMENT.")
    except:
        st.error("COMMUNICATION LINK LOST (Check Backend URL)")

# --- PAGE 2: CREW MANAGEMENT ---
elif menu == "Crew Management":
    st.title("👨‍🚀 CREW MANAGEMENT")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("### ➕ RECRUIT NEW")
        with st.form("add_form"):
            e_id = st.text_input("CREW ID (Unique)")
            name = st.text_input("FULL NAME")
            email = st.text_input("COMM FREQUENCY (Email)")
            dept = st.selectbox("SECTOR", ["Engineering", "Command", "Operations", "Science"])
            submit = st.form_submit_button("INITIATE UPLOAD")
            
            if submit:
                if e_id and name:
                    res = requests.post(f"{API_URL}/employees/", json={
                        "emp_id_str": e_id, "name": name, "email": email, "department": dept
                    })
                    if res.status_code == 200:
                        st.balloons()
                        st.success("CREW MEMBER REGISTERED")
                    else:
                        st.error("UPLOAD FAILED")

    with c2:
        st.markdown("### 📋 ACTIVE ROSTER")
        if st.button("🔄 REFRESH ROSTER"): st.rerun()
        
        try:
            res = requests.get(f"{API_URL}/employees/")
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(
                        df[["emp_id_str", "name", "department"]], 
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    with st.expander("🛑 DISCHARGE CREW MEMBER"):
                        del_id = st.selectbox("Select ID", df['emp_id_str'])
                        if st.button("CONFIRM DISCHARGE"):
                            requests.delete(f"{API_URL}/employees/{del_id}")
                            st.rerun()
        except:
            st.error("DATABASE OFFLINE")

# --- PAGE 3: ATTENDANCE (Flight Logs) ---
elif menu == "Flight Logs":
    st.title("🛰️ FLIGHT LOGS (ATTENDANCE)")
    
    try:
        res = requests.get(f"{API_URL}/employees/")
        if res.status_code == 200 and res.json():
            emps = res.json()
            emp_map = {e['name']: e['emp_id_str'] for e in emps}
            
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown("### 📡 LOG STATUS")
                sel_name = st.selectbox("SELECT OFFICER", list(emp_map.keys()))
                sel_id = emp_map[sel_name]
                
                d = st.date_input("LOG DATE", date.today())
                stat = st.radio("STATUS", ["ON DUTY", "AWOL"], horizontal=True)
                
                # Map back to backend expectations
                final_stat = "Present" if stat == "ON DUTY" else "Absent"
                
                if st.button("TRANSMIT LOG"):
                    requests.post(f"{API_URL}/attendance/", json={
                        "emp_id_str": sel_id, "date": str(d), "status": final_stat
                    })
                    st.success("LOG UPDATED")

            with col2:
                st.markdown("### 📊 HISTORICAL DATA")
                hist = requests.get(f"{API_URL}/attendance/{sel_id}")
                if hist.status_code == 200 and hist.json():
                    df_h = pd.DataFrame(hist.json())
                    # Custom colors for Space Theme
                    colors = {"Present": "#00E5FF", "Absent": "#FF2E63"} # Cyan vs Neon Red
                    fig = px.bar(df_h, x='date', y='status', color='status', 
                                 color_discrete_map=colors, title="DUTY CYCLES")
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("NO FLIGHT DATA AVAILABLE")
                    st_lottie(lottie_galaxy, height=200)
    except:
        st.error("DATA UPLINK FAILED")
