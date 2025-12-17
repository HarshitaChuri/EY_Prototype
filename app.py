import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import random
import uuid

# --- 1. PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="Provider Validation Orchestrator | EY Techathon",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GLOBAL STYLING & ASSETS ---
st.markdown("""
<style>
    /* Dark Theme Optimization */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        color: #FFE600; /* EY Yellow accent */
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #cccccc;
        font-style: italic;
        margin-bottom: 20px;
    }
    
    /* Agent Log Box - The "Terminal" Look */
    .agent-log-box {
        background-color: #1E1E1E;
        color: #00FF00;
        font-family: 'Courier New', Courier, monospace;
        padding: 15px;
        border-radius: 8px;
        height: 400px;
        overflow-y: auto;
        border: 1px solid #444;
        box-shadow: inset 0 0 10px #000;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FFE600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Custom Button Styling */
    .stButton>button {
        font-weight: bold;
        border-radius: 8px;
    }
    
    /* Sidebar Logo Adjustment */
    [data-testid="stSidebar"] img {
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER: SIMPLE DATA GENERATOR (Replaces Faker) ---
class SimpleDataGen:
    def __init__(self):
        self.first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
        self.last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
        self.cities = ["Springfield", "Rivertown", "Lakeside", "Fairview", "Madison", "Georgetown", "Arlington", "Bristol", "Clinton", "Franklin"]
        self.states = ["NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH", "MI", "GA"]
        self.streets = ["Main St", "Oak Ave", "Maple Dr", "Cedar Ln", "Washington Blvd", "Park Pl", "Highland Rd", "Elm St", "Sunset Blvd", "Pine St"]

    def first_name(self): return random.choice(self.first_names)
    def last_name(self): return random.choice(self.last_names)
    def city(self): return random.choice(self.cities)
    def state_abbr(self): return random.choice(self.states)
    def building_number(self): return str(random.randint(100, 9999))
    def address(self): return f"{self.building_number()} {random.choice(self.streets)}, {self.city()}, {self.state_abbr()}"
    def phone_number(self): return f"{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    def npi(self): return random.randint(1000000000, 9999999999)
    def uuid4(self): return str(uuid.uuid4())

fake = SimpleDataGen()

# --- 3. BACKEND LOGIC (SIMULATED AGENTS) ---

class AgentSimulator:
    """
    Simulates the 'thinking' process of the multi-agent system.
    This creates the realistic logs shown in the console during the demo.
    """
    def __init__(self):
        self.logs = []

    def log(self, agent_name, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        icon = "🤖"
        if agent_name == "Master Agent": icon = "🧠"
        elif agent_name == "Validation Agent": icon = "🔍"
        elif agent_name == "Enrichment Agent": icon = "🌐"
        elif agent_name == "QA Agent": icon = "🛡️"
        
        return f"[{timestamp}] {icon} <b>{agent_name}:</b> {message}"

    def validate_provider(self, provider_row):
        """
        Runs the logic for a single provider.
        Returns: (Updated Row, List of Log Strings)
        """
        logs = []
        updated_row = provider_row.copy()
        score = 0
        issues = []
        
        # --- PHASE 1: ORCHESTRATION ---
        logs.append(self.log("Master Agent", f"Initiating workflow for <b>{provider_row['Last Name']}, {provider_row['First Name']}</b> (ID: {provider_row['Provider ID']})"))
        time.sleep(0.1)
        logs.append(self.log("Master Agent", "Parsing unstructured input... delegating NPI check to Validation Agent."))

        # --- PHASE 2: VALIDATION AGENT (NPI CHECK) ---
        time.sleep(0.2)
        if provider_row['Phone'] == "000-000-0000":
            logs.append(self.log("Validation Agent", f"<span style='color:#FF4B4B'>❌ NPI Registry Mismatch:</span> Phone '{provider_row['Phone']}' is invalid/disconnected."))
            issues.append("Invalid Phone")
        else:
            logs.append(self.log("Validation Agent", f"✅ NPI Registry Match: Phone {provider_row['Phone']} verified active."))
            score += 40

        # --- PHASE 3: ENRICHMENT AGENT (WEB SEARCH) ---
        time.sleep(0.2)
        if "Old Rd" in provider_row['Address']:
            logs.append(self.log("Master Agent", "⚠️ Address Flagged. Delegating to Enrichment Agent for web verification."))
            time.sleep(0.2)
            logs.append(self.log("Enrichment Agent", f"Scraping 'Google Maps' for: {provider_row['Address']}..."))
            logs.append(self.log("Enrichment Agent", "<span style='color:#FFA500'>⚠️ Location Report:</span> 'Permanently Closed'"))
            
            # Simulate Finding New Address
            new_city = fake.city()
            new_addr = f"{fake.building_number()} Medical Park Dr, {new_city}, {fake.state_abbr()}"
            logs.append(self.log("Enrichment Agent", f"🔍 WEB SEARCH: Found new practice location at <b>{new_addr}</b>"))
            
            updated_row['Address'] = new_addr
            updated_row['Flagged Issues'] = "Address Auto-Corrected"
            logs.append(self.log("Enrichment Agent", "✅ Database Updated with new location."))
            score += 30
            issues.append("Address Updated")
        else:
            logs.append(self.log("Enrichment Agent", "✅ Google Maps Verification: Location confirmed active."))
            score += 40

        # --- PHASE 4: COMPLIANCE/QA (LICENSE CHECK) ---
        time.sleep(0.2)
        try:
            # Check year from the string "YYYY-MM-DD"
            exp_year = int(provider_row['License Expiry'].split('-')[0])
            if exp_year < 2025:
                logs.append(self.log("QA Agent", f"<span style='color:#FF4B4B'>❌ CRITICAL:</span> License expired on {provider_row['License Expiry']}."))
                issues.append("Expired License")
                score = max(0, score - 50) # Heavy penalty
            else:
                logs.append(self.log("QA Agent", f"✅ State Board Verification: License active until {provider_row['License Expiry']}."))
                score += 20
        except:
             pass

        # Final Scoring
        updated_row['Confidence Score'] = min(100, score)
        
        if score >= 80:
            updated_row['Validation Status'] = "Verified"
        elif score >= 50:
            updated_row['Validation Status'] = "Needs Review"
        else:
            updated_row['Validation Status'] = "Rejected"

        if issues:
            updated_row['Flagged Issues'] = ", ".join(issues)
        else:
            updated_row['Flagged Issues'] = "None"
        
        logs.append(self.log("Master Agent", f"🏁 Workflow Complete. Final Confidence Score: <b>{updated_row['Confidence Score']}%</b>"))
        
        return updated_row, logs

def generate_messy_provider_data(num_records=10):
    """Generates the 'Dirty' dataset that needs cleaning."""
    data = []
    for _ in range(num_records):
        # 30% chance of a "messy" record
        is_error = random.random() < 0.3
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        npi = fake.npi()
        
        if is_error:
            # Create a mismatch or invalid data
            address = "123 Old Rd, " + fake.city() # Generic/Wrong address
            phone = "000-000-0000" # Invalid phone
            license_exp = "2023-05-20" # Expired
            status = "Unverified"
        else:
            address = fake.address().replace("\n", ", ")
            phone = fake.phone_number()
            license_exp = "2026-12-31" # Valid
            status = "Unverified"

        data.append({
            "Provider ID": fake.uuid4()[:8],
            "First Name": first_name,
            "Last Name": last_name,
            "NPI": npi,
            "Address": address,
            "Phone": phone,
            "License Expiry": license_exp,
            "Validation Status": status,
            "Confidence Score": 0,
            "Flagged Issues": ""
        })
    
    return pd.DataFrame(data)

# --- 4. SESSION STATE INIT ---
if 'provider_data' not in st.session_state:
    st.session_state['provider_data'] = pd.DataFrame()
if 'agent_logs' not in st.session_state:
    st.session_state['agent_logs'] = []
if 'processing_complete' not in st.session_state:
    st.session_state['processing_complete'] = False

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.markdown("## Provider Validation Orchestrator")
st.sidebar.caption("Autonomous Network Integrity")
st.sidebar.markdown("---")
page = st.sidebar.radio("Module Selection", ["Dashboard", "Data Upload", "Agent Operations", "Compliance Reports", "Settings"])
st.sidebar.markdown("---")
st.sidebar.info("System Status: **ONLINE**\n\nNPI API: Connected 🟢\n\nGoogle Maps API: Connected 🟢")

# --- 6. PAGE LAYOUTS ---

# ==========================================
# PAGE: DASHBOARD
# ==========================================
if page == "Dashboard":
    st.markdown('<p class="main-header">Executive Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time Provider Network Integrity Monitor</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Providers", "2,450", "25 New Today")
    with col2: st.metric("Directory Accuracy", "98.5%", "+12% vs Manual")
    with col3: st.metric("Validation Speed", "1.2s", "Avg per record")
    with col4: st.metric("Cost Savings", "$12,500", "Est. Monthly")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Validation Status")
        # Mock Data for visuals
        chart_data = pd.DataFrame({
            'Status': ['Verified', 'Needs Review', 'Rejected'],
            'Count': [85, 10, 5]
        })
        fig = px.pie(chart_data, values='Count', names='Status', hole=0.4, color_discrete_map={'Verified':'#00FF00', 'Needs Review':'#FFA500', 'Rejected':'#FF0000'})
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("Data Quality Issues Detected")
        # Mock Data
        err_data = pd.DataFrame({
            'Issue': ['Address Mismatch', 'Expired License', 'Invalid Phone', 'Sanctioned Entity'],
            'Count': [120, 45, 30, 2]
        })
        fig2 = px.bar(err_data, x='Issue', y='Count', color='Count', color_continuous_scale='Viridis')
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# PAGE: DATA UPLOAD
# ==========================================
elif page == "Data Upload":
    st.markdown('<p class="main-header">Data Ingestion</p>', unsafe_allow_html=True)
    st.markdown("Upload raw provider rosters (CSV/Excel) or scanned license folders (PDF).")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Drag and drop files here", type=['csv', 'pdf', 'xlsx'])
        
        if uploaded_file is not None or st.button("Simulate Upload for Demo"):
            with st.spinner("Parsing file structure & running OCR on PDFs..."):
                time.sleep(1.5)
                # Generate new messy data
                st.session_state['provider_data'] = generate_messy_provider_data(12) 
                st.session_state['processing_complete'] = False
                st.session_state['agent_logs'] = []
                st.success("✅ File Parsed Successfully! 12 Provider Records Extracted.")
                
    with col2:
        st.info("ℹ️ **OCR Status:** Enabled\n\n**Supported:** Scanned PDFs, Images, CSV\n\n**Parser:** GPT-4o Vision")

    if not st.session_state['provider_data'].empty:
        st.subheader("Preview Extracted Data (Raw)")
        st.dataframe(st.session_state['provider_data'], use_container_width=True)

# ==========================================
# PAGE: AGENT OPERATIONS (THE CORE DEMO)
# ==========================================
elif page == "Agent Operations":
    st.markdown('<p class="main-header">Agent Orchestration Hub</p>', unsafe_allow_html=True)
    
    if st.session_state['provider_data'].empty:
        st.warning("⚠️ No data loaded. Please go to 'Data Upload' to ingest a roster.")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Orchestration Controls")
            st.metric("Records Queued", len(st.session_state['provider_data']))
            
            speed = st.slider("Processing Speed", 0.5, 3.0, 1.0, help="Controls how fast the simulation runs")
            
            if st.button("🚀 START AGENTIC WORKFLOW", type="primary", use_container_width=True):
                st.session_state['processing_complete'] = False
                st.session_state['agent_logs'] = []
                
                # UI Elements for the loop
                progress_bar = st.progress(0)
                status_text = st.empty()
                log_placeholder = st.empty()
                
                simulator = AgentSimulator()
                processed_rows = []
                
                total = len(st.session_state['provider_data'])
                
                # --- MAIN PROCESSING LOOP ---
                for index, row in st.session_state['provider_data'].iterrows():
                    status_text.text(f"Processing Provider {index + 1}/{total}: Dr. {row['Last Name']}...")
                    
                    # Run Logic
                    new_row, logs = simulator.validate_provider(row)
                    processed_rows.append(new_row)
                    
                    # Animate Logs
                    for log in logs:
                        st.session_state['agent_logs'].insert(0, log)
                        log_html = "<br>".join(st.session_state['agent_logs'][:50])
                        log_placeholder.markdown(f'<div class="agent-log-box">{log_html}</div>', unsafe_allow_html=True)
                        time.sleep(0.8 / speed) # Reading time
                    
                    progress_bar.progress((index + 1) / total)
                
                st.session_state['provider_data'] = pd.DataFrame(processed_rows)
                st.session_state['processing_complete'] = True
                status_text.success("✅ Batch Processing Complete!")
                
        with col2:
            st.subheader("Live Agent Thought Process")
            # If logs exist, show them (persisted)
            if st.session_state['agent_logs']:
                log_html = "<br>".join(st.session_state['agent_logs'][:50])
                st.markdown(f'<div class="agent-log-box">{log_html}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="agent-log-box"><i>Waiting for start command...<br>System Ready.</i></div>', unsafe_allow_html=True)

        # RESULTS TABLE (Only shows after processing)
        if st.session_state['processing_complete']:
            st.markdown("---")
            st.subheader("Validation Results")
            
            def highlight_score(val):
                color = '#ff4b4b' if val < 50 else '#ffa500' if val < 80 else '#00ff00'
                return f'color: {color}; font-weight: bold'

            # Apply styling to the dataframe display
            df_display = st.session_state['provider_data'].copy()
            st.dataframe(
                df_display.style.map(highlight_score, subset=['Confidence Score']),
                use_container_width=True
            )

# ==========================================
# PAGE: COMPLIANCE REPORTS
# ==========================================
elif page == "Compliance Reports":
    st.markdown('<p class="main-header">Compliance & Audit Center</p>', unsafe_allow_html=True)
    
    if not st.session_state['processing_complete']:
        st.info("ℹ️ Run the Agent Operation to generate a fresh audit report.")
    else:
        col1, col2 = st.columns(2)
        df = st.session_state['provider_data']
        
        with col1:
            st.success("✅ **Directory Ready for Publish**")
            verified_count = len(df[df['Validation Status'] == 'Verified'])
            st.write(f"Ready Records: **{verified_count}**")
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Verified Directory (CSV)",
                csv,
                "verified_providers_2025.csv",
                "text/csv",
                type="primary"
            )
            
        with col2:
            st.warning("⚠️ **Exception Report (Action Required)**")
            flagged = df[df['Validation Status'] != 'Verified']
            st.write(f"Flagged Records: **{len(flagged)}**")
            
            if not flagged.empty:
                st.download_button(
                    "📥 Download Exceptions Report (CSV)",
                    flagged.to_csv(index=False).encode('utf-8'),
                    "exceptions_report.csv",
                    "text/csv"
                )
        
        st.markdown("---")
        st.subheader("Deep Dive: Flagged Providers")
        if not flagged.empty:
            st.dataframe(flagged)
        else:
            st.write("No flagged providers. Great job!")

# ==========================================
# PAGE: SETTINGS
# ==========================================
elif page == "Settings":
    st.header("System Configuration")
    
    with st.expander("🔐 API Credential Store", expanded=True):
        st.text_input("OpenAI API Key (GPT-4o)", type="password", value="sk-xxxxxxxxxxxxxxxx")
        st.text_input("CMS NPI Registry API Key", type="password", value="xxxxxxxx-xxxx-xxxx")
        st.text_input("Google Maps Platform Key", type="password", value="AIzaSyXXXXXXXXXXXXXXXX")
        st.caption("Keys are encrypted at rest using AES-256.")

    with st.expander("⚙️ Agent Thresholds"):
        st.slider("Auto-Approval Confidence Threshold", 0, 100, 80)
        st.toggle("Strict Mode (Reject if License Expiring < 30 days)", value=True)
        st.toggle("Enable 'Human-in-the-Loop' for Low Confidence", value=True)
