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

# --- ASSETS (Safe Loader) ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Stable Space Animations
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
    
    /* 2. GLASSMORPHISM CARDS */
    .block-container { padding-top: 2rem; }
    div[data-testid="stExpander"], div.stDataFrame, div.stForm {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* 3. NEON TEXT */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 0 0 10px #FF2E63, 0 0 20px #FF2E63;
        font-family: 'Courier New', Courier, monospace;
    }
    p, label, .stMarkdown, .stRadio label {
        color: #E0E0E0 !important;
    }

    /* 4. BUTTONS */
    .stButton>button {
        background: transparent !important;
        color: #FF2E63 !important;
        border: 2px solid #FF2E63 !important;
        border-radius: 30px !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
    }
    .stButton>button:hover {
        background: #FF2E63 !important;
        color: white !important;
        box-shadow: 0 0 15px #FF2E63, 0 0 30px #FF2E63;
    }
    
    /* 5. INPUTS */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    
    /* ⚠️ FIXED: We removed the line that hid the header, so you can see the menu arrow now! */
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if lottie_astronaut:
        st_lottie(lottie_astronaut, height=180)
    
    st.markdown("## 🛸 COMMAND CENTER")
    menu = st.radio("", ["Mission Control", "Crew Management", "Flight Logs"])
    st.markdown("---")
    st.info("System Status: 🟢 ONLINE")

# --- PAGE 1: DASHBOARD ---
if menu == "Mission Control":
    st.title("🚀 MISSION CONTROL")
    st.markdown("### HRMS GALACTICA DASHBOARD")
    
    try:
        emp_res = requests.get(f"{API_URL}/employees/")
        if emp_res.status_code == 200:
            df = pd.DataFrame(emp_res.json())
            
            if not df.empty:
                c1, c2 = st.columns(2)
                c1.markdown(f"<h1 style='text-align:center; font-size: 60px;'>{len(df)}</h1><p style='text-align:center'>ACTIVE CREW</p>", unsafe_allow_html=True)
                
                top_dept = df['department'].value_counts().idxmax()
                c2.markdown(f"<h1 style='text-align:center; font-size: 40px;'>{top_dept}</h1><p style='text-align:center'>DOMINANT SECTOR</p>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([2,1])
                with col1:
                    fig = px.pie(df, names='department', title='SECTOR DISTRIBUTION', 
                                 color_discrete_sequence=px.colors.sequential.Plasma, hole=0.5)
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                     if lottie_rocket:
                         st_lottie(lottie_rocket, height=200)

            else:
                st.warning("NO CREW DETECTED.")
    except:
        st.error("COMMUNICATION LINK LOST")

# --- PAGE 2: CREW MANAGEMENT ---
elif menu == "Crew Management":
    st.title("👨‍🚀 CREW MANAGEMENT")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("### ➕ RECRUIT NEW")
        with st.form("add_form"):
            e_id = st.text_input("CREW ID")
            name = st.text_input("FULL NAME")
            email = st.text_input("EMAIL")
            dept = st.selectbox("SECTOR", ["Engineering", "Command", "Operations", "Science"])
            submit = st.form_submit_button("INITIATE UPLOAD")
            
            if submit:
                if e_id and name:
                    res = requests.post(f"{API_URL}/employees/", json={
                        "emp_id_str": e_id, "name": name, "email": email, "department": dept
                    })
                    if res.status_code == 200:
                        st.success("CREW MEMBER REGISTERED")
                        st.rerun()
                    else:
                        st.error("UPLOAD FAILED")

    with c2:
        st.markdown("### 📋 ACTIVE ROSTER & STATS")
        if st.button("🔄 REFRESH"): st.rerun()
        
        try:
            res = requests.get(f"{API_URL}/employees/")
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data)
                    
                    # BONUS: Calculate Total Present Days for each employee
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
                    
                    df['Total Present'] = attendance_counts

                    st.dataframe(df[["emp_id_str", "name", "department", "Total Present"]], use_container_width=True, hide_index=True)
                    
                    with st.expander("🛑 DISCHARGE MEMBER"):
                        del_id = st.selectbox("Select ID", df['emp_id_str'])
                        if st.button("CONFIRM DISCHARGE"):
                            requests.delete(f"{API_URL}/employees/{del_id}")
                            st.rerun()
        except:
            st.error("DATABASE OFFLINE")

# --- PAGE 3: LOGS ---
elif menu == "Flight Logs":
    st.title("🛰️ FLIGHT LOGS")
    
    try:
        res = requests.get(f"{API_URL}/employees/")
        if res.status_code == 200 and res.json():
            emps = res.json()
            emp_map = {e['name']: e['emp_id_str'] for e in emps}
            
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown("### 📡 LOG ENTRY")
                sel_name = st.selectbox("SELECT OFFICER", list(emp_map.keys()))
                sel_id = emp_map[sel_name]
                d = st.date_input("DATE", date.today())
                stat = st.radio("STATUS", ["ON DUTY", "AWOL"], horizontal=True)
                final_stat = "Present" if stat == "ON DUTY" else "Absent"
                
                if st.button("TRANSMIT"):
                    requests.post(f"{API_URL}/attendance/", json={
                        "emp_id_str": sel_id, "date": str(d), "status": final_stat
                    })
                    st.success("LOG UPDATED")

            with col2:
                st.markdown("### 📊 DATA STREAM")
                
                # BONUS: Filter Logic
                filter_mode = st.checkbox("Filter by Date Range?")
                
                hist = requests.get(f"{API_URL}/attendance/{sel_id}")
                if hist.status_code == 200 and hist.json():
                    df_h = pd.DataFrame(hist.json())
                    
                    if filter_mode:
                        start_d = st.date_input("Start Date", date.today())
                        df_h['date'] = pd.to_datetime(df_h['date']).dt.date
                        df_h = df_h[df_h['date'] >= start_d]
                    
                    if not df_h.empty:
                        colors = {"Present": "#00E5FF", "Absent": "#FF2E63"}
                        fig = px.bar(df_h, x='date', y='status', color='status', 
                                     color_discrete_map=colors, title="DUTY CYCLES")
                        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No records found.")
                else:
                    if lottie_galaxy:
                        st_lottie(lottie_galaxy, height=200)
    except:
        st.error("DATA UPLINK FAILED")
