import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="Nexus AI - HRMS", page_icon="🧠", layout="wide")

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

# AI & Office Animations
lottie_ai_brain = load_lottieurl("https://lottie.host/62650058-299e-4e2e-a50d-88849b2f4f13/zS6A6k8v2h.json") # AI Brain/Tech
lottie_office = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5tl1xxnz.json") # People working
lottie_analytics = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_w51pcehl.json") # Data/Empty
lottie_success = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json") # Checkmark

# --- CUSTOM CSS (THE "SILICON VALLEY" LOOK) ---
st.markdown("""
    <style>
    /* 1. BACKGROUND: Clean Tech White/Blue */
    .stApp {
        background-color: #F8FAFC;
        background-image: linear-gradient(315deg, #F8FAFC 0%, #E2E8F0 74%);
    }
    
    /* 2. MODERN CARDS (Neumorphism/Clean) */
    .block-container { padding-top: 2rem; }
    div[data-testid="stExpander"], div.stDataFrame, div.stForm {
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    /* 3. TYPOGRAPHY (Professional Sans-Serif) */
    h1, h2, h3 {
        color: #1E293B !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    p, label, .stMarkdown, .stRadio label {
        color: #475569 !important;
        font-family: 'Inter', sans-serif;
    }

    /* 4. BUTTONS (Modern Indigo) */
    .stButton>button {
        background-color: #4F46E5 !important; /* Indigo 600 */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #4338CA !important; /* Indigo 700 */
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    /* 5. METRIC CARDS */
    div[data-testid="stMetricValue"] {
        color: #4F46E5 !important;
        font-weight: 800;
    }
    
    /* 6. INPUT FIELDS */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        background-color: #F1F5F9 !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # Show AI Brain animation if loaded, else standard text
    if lottie_ai_brain:
        st_lottie(lottie_ai_brain, height=150)
    else:
        st.title("🧠")
    
    st.markdown("### NEXUS AI")
    st.markdown("Human Resources System v2.0")
    
    menu = st.radio("Menu", ["Dashboard Overview", "Employee Directory", "Attendance Tracker"])
    
    st.markdown("---")
    st.caption("© 2026 Nexus AI Corp")

# --- PAGE 1: DASHBOARD ---
if menu == "Dashboard Overview":
    st.title("📊 Enterprise Dashboard")
    st.markdown("Welcome back, Admin. Here is today's personnel overview.")
    
    try:
        emp_res = requests.get(f"{API_URL}/employees/")
        if emp_res.status_code == 200:
            df = pd.DataFrame(emp_res.json())
            
            if not df.empty:
                # Top Level Metrics
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    st.metric("Total Workforce", len(df), "+2 this week")
                
                with c2:
                    top_dept = df['department'].value_counts().idxmax()
                    st.metric("Largest Dept", top_dept)
                    
                with c3:
                    st.metric("System Status", "Optimal", delta_color="normal")
                
                st.markdown("---")
                
                # Visualizations
                col1, col2 = st.columns([2,1])
                
                with col1:
                    st.subheader("Departmental Distribution")
                    # Professional Color Palette
                    fig = px.pie(df, names='department', hole=0.6, 
                                 color_discrete_sequence=px.colors.qualitative.G10)
                    fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("Team Activity")
                    if lottie_office:
                        st_lottie(lottie_office, height=200)
                    else:
                        st.info("System operational.")
            else:
                st.info("System initialized. No data available.")
                if lottie_analytics:
                    st_lottie(lottie_analytics, height=200)
    except:
        st.error("⚠️ Server Connection Failed. Please check API URL.")

# --- PAGE 2: EMPLOYEE DIRECTORY ---
elif menu == "Employee Directory":
    st.title("👥 Employee Directory")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("Onboard Talent")
        with st.form("add_form"):
            e_id = st.text_input("Employee ID (Unique)")
            name = st.text_input("Full Name")
            email = st.text_input("Corporate Email")
            dept = st.selectbox("Department", ["AI Research", "Engineering", "Product", "Sales", "HR"])
            submit = st.form_submit_button("Create Profile")
            
            if submit:
                if e_id and name:
                    res = requests.post(f"{API_URL}/employees/", json={
                        "emp_id_str": e_id, "name": name, "email": email, "department": dept
                    })
                    if res.status_code == 200:
                        st.success("Profile Created Successfully")
                        if lottie_success:
                            st_lottie(lottie_success, height=60, key="succ_1")
                        st.rerun()
                    else:
                        st.error("Submission Failed. Check duplicate ID.")

    with c2:
        st.subheader("Current Roster")
        
        c_search, c_refresh = st.columns([3,1])
        with c_refresh:
            if st.button("🔄 Refresh"): st.rerun()
            
        try:
            res = requests.get(f"{API_URL}/employees/")
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data)
                    
                    # BONUS: Performance/Attendance Stats
                    # Client-side calculation for "Total Present"
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
                    
                    df['Days Present'] = attendance_counts

                    # Display clean table
                    st.dataframe(
                        df[["emp_id_str", "name", "department", "Days Present"]], 
                        use_container_width=True, 
                        hide_index=True
                    )
                    
                    with st.expander("Administrative Actions (Delete)"):
                        del_id = st.selectbox("Select Employee to Remove", df['emp_id_str'])
                        if st.button("Terminate Profile", type="secondary"):
                            requests.delete(f"{API_URL}/employees/{del_id}")
                            st.rerun()
        except:
            st.warning("Unable to fetch directory data.")

# --- PAGE 3: ATTENDANCE TRACKER ---
elif menu == "Attendance Tracker":
    st.title("📅 Attendance Tracker")
    
    try:
        res = requests.get(f"{API_URL}/employees/")
        if res.status_code == 200 and res.json():
            emps = res.json()
            emp_map = {e['name']: e['emp_id_str'] for e in emps}
            
            col1, col2 = st.columns([1,2])
            with col1:
                st.subheader("Log Entry")
                sel_name = st.selectbox("Select Employee", list(emp_map.keys()))
                sel_id = emp_map[sel_name]
                
                d = st.date_input("Date", date.today())
                stat = st.radio("Status", ["Present", "Remote", "Absent"], horizontal=True)
                
                # Logic: Map "Remote" to "Present" for backend simplicity, or keep consistent
                final_stat = "Absent" if stat == "Absent" else "Present"
                
                if st.button("Submit Log"):
                    requests.post(f"{API_URL}/attendance/", json={
                        "emp_id_str": sel_id, "date": str(d), "status": final_stat
                    })
                    st.success("Entry Logged")
                    if lottie_success:
                        st_lottie(lottie_success, height=50, key="succ_2")

            with col2:
                st.subheader("Analytics")
                
                # BONUS: Filter
                use_filter = st.checkbox("Filter by Date")
                
                hist = requests.get(f"{API_URL}/attendance/{sel_id}")
                if hist.status_code == 200 and hist.json():
                    df_h = pd.DataFrame(hist.json())
                    
                    if use_filter:
                        start_d = st.date_input("From Date", date.today())
                        df_h['date'] = pd.to_datetime(df_h['date']).dt.date
                        df_h = df_h[df_h['date'] >= start_d]
                    
                    if not df_h.empty:
                        # Corporate Colors: Indigo for Present, Gray for Absent
                        colors = {"Present": "#4F46E5", "Absent": "#94A3B8"} 
                        fig = px.bar(df_h, x='date', y='status', color='status', 
                                     color_discrete_map=colors, title="Attendance History")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No records found in this period.")
                else:
                    st.info("No attendance history available.")
    except:
        st.error("Database connection required.")
