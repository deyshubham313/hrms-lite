import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="HRMS Lite Pro", page_icon="🚀", layout="wide")

# ⚠️ REPLACE THIS WITH YOUR ACTUAL RENDER URL (NO TRAILING SLASH)
# Example: "https://hrms-backend-xyz.onrender.com"
API_URL = "https://hrms-lite-ac8r.onrender.com" 

# --- ASSETS & STYLING ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Animations
lottie_hr = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5tl1xxnz.json")
lottie_success = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json")
lottie_empty = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_w51pcehl.json")

# Custom CSS for "Premium" Look
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {
        background-color: #4F46E5; color: white; border-radius: 8px; 
        padding: 0.5rem 1rem; border: none; font-weight: bold;
    }
    .stButton>button:hover {background-color: #4338ca;}
    .metric-card {
        background-color: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;
    }
    h1 {color: #1e293b;}
    h2, h3 {color: #334155;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st_lottie(lottie_hr, height=200)
    st.title("🚀 HRMS Lite")
    menu = st.radio("Navigation", ["Dashboard", "Manage Employees", "Attendance"], index=0)
    st.info("💡 Pro Tip: Use the dashboard to visualize team stats.")

# --- PAGE 1: DASHBOARD (The "Wow" Factor) ---
if menu == "Dashboard":
    st.title("📊 HR Overview")
    
    try:
        # Fetch Data
        emp_res = requests.get(f"{API_URL}/employees/")
        employees = emp_res.json() if emp_res.status_code == 200 else []
        df_emp = pd.DataFrame(employees)

        if not df_emp.empty:
            # Metrics Row
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Employees", len(df_emp))
            c1.markdown(f"<div style='background:#e0e7ff;height:5px;border-radius:5px'></div>", unsafe_allow_html=True)
            
            dept_counts = df_emp['department'].value_counts()
            top_dept = dept_counts.idxmax()
            c2.metric("Top Department", top_dept)
            
            # Charts
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("Department Distribution")
                fig = px.pie(df_emp, names='department', title='Employees by Dept', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)
            
            with col_chart2:
                st.subheader("Recent Activity")
                st.info("Attendance data visualization will appear here once records are generated.")
                st_lottie(lottie_empty, height=200)

        else:
            st.warning("No data yet. Go to 'Manage Employees' to start!")
            st_lottie(lottie_empty, height=300)

    except Exception as e:
        st.error(f"Could not connect to backend. Check URL. Error: {e}")

# --- PAGE 2: MANAGE EMPLOYEES ---
elif menu == "Manage Employees":
    st.title("👥 Employee Management")

    with st.container():
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown("### ➕ Add New")
            with st.form("add_emp_form"):
                e_id = st.text_input("Employee ID")
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                dept = st.selectbox("Department", ["Engineering", "HR", "Sales", "Marketing", "Support"])
                submitted = st.form_submit_button("Add Employee")
                
                if submitted:
                    if e_id and name and email:
                        res = requests.post(f"{API_URL}/employees/", json={
                            "emp_id_str": e_id, "name": name, "email": email, "department": dept
                        })
                        if res.status_code == 200:
                            st.success("Success!")
                            st_lottie(lottie_success, height=100, key="success_add")
                        else:
                            st.error(f"Error: {res.json().get('detail')}")
                    else:
                        st.warning("Fill all fields")

        with c2:
            st.markdown("### 📋 Employee List")
            # Refresh Button
            if st.button("🔄 Refresh Data"):
                st.rerun()

            try:
                res = requests.get(f"{API_URL}/employees/")
                if res.status_code == 200:
                    data = res.json()
                    if data:
                        df = pd.DataFrame(data)
                        # Stylized Dataframe
                        st.dataframe(
                            df[["emp_id_str", "name", "department", "email"]],
                            column_config={
                                "emp_id_str": "ID",
                                "name": "Name",
                                "department": st.column_config.TextColumn("Dept", help="Team"),
                                "email": "Contact"
                            },
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        # Delete Section
                        with st.expander("🗑️ Delete Employee"):
                            del_id = st.selectbox("Select ID to Remove", df['emp_id_str'])
                            if st.button("Confirm Delete", type="primary"):
                                requests.delete(f"{API_URL}/employees/{del_id}")
                                st.rerun()
                    else:
                        st.info("No employees found.")
                        st_lottie(lottie_empty, height=200)
            except:
                st.error("Backend offline")

# --- PAGE 3: ATTENDANCE ---
elif menu == "Attendance":
    st.title("📅 Daily Attendance")
    
    try:
        emp_res = requests.get(f"{API_URL}/employees/")
        if emp_res.status_code == 200:
            emps = emp_res.json()
            emp_dict = {e['name']: e['emp_id_str'] for e in emps}
            
            if emps:
                col_left, col_right = st.columns([1, 2])
                
                with col_left:
                    st.markdown("### 📝 Mark Status")
                    sel_name = st.selectbox("Select Employee", list(emp_dict.keys()))
                    sel_id = emp_dict[sel_name]
                    date_picked = st.date_input("Date", date.today())
                    status = st.radio("Status", ["Present", "Absent"], horizontal=True)
                    
                    if st.button("Submit Record"):
                        res = requests.post(f"{API_URL}/attendance/", json={
                            "emp_id_str": sel_id, "date": str(date_picked), "status": status
                        })
                        if res.status_code == 200:
                            st.success("Recorded!")
                            st_lottie(lottie_success, height=100, key="att_success")
                        else:
                            st.error("Failed")

                with col_right:
                    st.markdown(f"### 📜 History: {sel_name}")
                    hist_res = requests.get(f"{API_URL}/attendance/{sel_id}")
                    if hist_res.status_code == 200:
                        hist_data = hist_res.json()
                        if hist_data:
                            df_hist = pd.DataFrame(hist_data)
                            
                            # Interactive Bar Chart for Attendance
                            fig_att = px.bar(df_hist, x='date', y='status', 
                                            color='status', 
                                            color_discrete_map={"Present": "#10B981", "Absent": "#EF4444"},
                                            title="Attendance Timeline")
                            st.plotly_chart(fig_att, use_container_width=True)
                        else:
                            st.info("No records for this employee.")
            else:
                st.warning("Add employees first.")
    except Exception as e:
        st.error(f"Connection Error: {e}")
