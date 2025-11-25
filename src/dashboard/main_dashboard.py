# # # # # src/dashboard/main_dashboard.py

# # # # import os
# # # # import time
# # # # import streamlit as st

# # # # from src.dashboard.admin_dashboard import render_admin_dashboard
# # # # from src.dashboard.citizen_dashboard import render_citizen_dashboard

# # # # ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
# # # # AUTH_STATUS_KEY = "auth_status"


# # # # def _inject_base_css() -> None:
# # # #     """Medical-themed CSS with clean, professional color scheme."""
# # # #     st.markdown(
# # # #         """
# # # #         <style>
# # # #         /* Import medical-grade professional font */
# # # #         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

# # # #         /* Global styles */
# # # #         * {
# # # #             font-family: 'Poppins', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
# # # #         }

# # # #         /* Root variables - Medical color scheme */
# # # #         :root {
# # # #             --primary-blue: #4A90E2;
# # # #             --secondary-blue: #5CA4E8;
# # # #             --light-blue: #E8F4FF;
# # # #             --dark-blue: #2C5F8D;
# # # #             --accent-teal: #4ECDC4;
# # # #             --accent-green: #52D17C;
# # # #             --accent-orange: #FF9F68;
# # # #             --accent-red: #FF6B6B;
# # # #             --bg-light: #F5F9FC;
# # # #             --bg-white: #FFFFFF;
# # # #             --text-dark: #2C3E50;
# # # #             --text-medium: #546E7A;
# # # #             --text-light: #78909C;
# # # #             --border-color: #E0E7ED;
# # # #         }

# # # #         /* Main background */
# # # #         .stApp {
# # # #             background: linear-gradient(135deg, #E8F4FF 0%, #F5F9FC 100%);
# # # #         }

# # # #         /* Block container */
# # # #         .block-container {
# # # #             padding-top: 2.5rem;
# # # #             padding-bottom: 2.5rem;
# # # #             max-width: 1400px;
# # # #         }

# # # #         /* Sidebar styling - Medical theme */
# # # #         section[data-testid="stSidebar"] {
# # # #             background: linear-gradient(180deg, #2C5F8D 0%, #1A4470 100%);
# # # #             border-right: 3px solid var(--primary-blue);
# # # #         }

# # # #         section[data-testid="stSidebar"] * {
# # # #             color: #2C3E50 !important;
# # # #         }

# # # #         section[data-testid="stSidebar"] .stMarkdown h3 {
# # # #             color: #2C3E50 !important;
# # # #             border-bottom: 2px solid var(--accent-teal);
# # # #             padding-bottom: 0.5rem;
# # # #             margin-bottom: 1rem;
# # # #         }

# # # #         /* Title styling */
# # # #         h1 {
# # # #             font-size: 3.2rem !important;
# # # #             font-weight: 800 !important;
# # # #             color: var(--dark-blue) !important;
# # # #             margin-bottom: 0.5rem !important;
# # # #             letter-spacing: -0.5px;
# # # #         }

# # # #         h2 {
# # # #             font-size: 2.4rem !important;
# # # #             font-weight: 700 !important;
# # # #             color: #2C3E50 !important;
# # # #             margin-bottom: 1rem !important;
# # # #         }

# # # #         h3 {
# # # #             font-size: 1.9rem !important;
# # # #             font-weight: 600 !important;
# # # #             color: #2C3E50 !important;
# # # #             margin-bottom: 1rem !important;
# # # #         }

# # # #         h4 {
# # # #             font-size: 1.5rem !important;
# # # #             font-weight: 600 !important;
# # # #             color: #2C3E50 !important;
# # # #         }

# # # #         /* Paragraph and text sizing */
# # # #         p, .stMarkdown, .stText, div, span, label {
# # # #             font-size: 1.15rem !important;
# # # #             line-height: 1.7 !important;
# # # #             color: #2C3E50 !important;
# # # #         }

# # # #         /* Larger labels */
# # # #         label {
# # # #             font-weight: 600 !important;
# # # #             font-size: 1.2rem !important;
# # # #             color: #2C3E50 !important;
# # # #         }

# # # #         /* Caption text */
# # # #         .stCaption {
# # # #             font-size: 1.1rem !important;
# # # #             color: #2C3E50 !important;
# # # #         }

# # # #         /* Button styling - Medical primary button */
# # # #         .stButton > button {
# # # #             background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
# # # #             color: white;
# # # #             border: none;
# # # #             border-radius: 12px;
# # # #             padding: 1rem 2.5rem;
# # # #             font-size: 1.25rem !important;
# # # #             font-weight: 700;
# # # #             transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
# # # #             box-shadow: 0 6px 20px rgba(74, 144, 226, 0.35);
# # # #             letter-spacing: 0.3px;
# # # #         }

# # # #         .stButton > button:hover {
# # # #             transform: translateY(-3px);
# # # #             box-shadow: 0 12px 28px rgba(74, 144, 226, 0.45);
# # # #             background: linear-gradient(135deg, var(--secondary-blue) 0%, var(--primary-blue) 100%);
# # # #         }

# # # #         .stButton > button:active {
# # # #             transform: translateY(-1px);
# # # #         }

# # # #         /* Input fields - Medical style */
# # # #         .stTextInput > div > div > input,
# # # #         .stNumberInput > div > div > input,
# # # #         .stSelectbox > div > div > select {
# # # #             font-size: 1.15rem !important;
# # # #             border-radius: 10px !important;
# # # #             border: 2px solid var(--border-color) !important;
# # # #             background: var(--bg-white) !important;
# # # #             padding: 0.75rem 1rem !important;
# # # #             transition: all 0.3s ease;
# # # #             color: #2C3E50 !important;
# # # #         }

# # # #         .stTextInput > div > div > input:focus,
# # # #         .stNumberInput > div > div > input:focus,
# # # #         .stSelectbox > div > div > select:focus {
# # # #             border-color: var(--primary-blue) !important;
# # # #             box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.1) !important;
# # # #         }

# # # #         /* Slider styling - Medical blue */
# # # #         .stSlider > div > div > div {
# # # #             background: linear-gradient(90deg, var(--accent-teal) 0%, var(--primary-blue) 100%) !important;
# # # #         }

# # # #         .stSlider > div > div > div > div {
# # # #             background: var(--bg-white) !important;
# # # #             border: 3px solid var(--primary-blue) !important;
# # # #             box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
# # # #         }

# # # #         /* Alert boxes - Medical theme */
# # # #         .stAlert {
# # # #             border-radius: 14px;
# # # #             border-left: 5px solid;
# # # #             font-size: 1.15rem !important;
# # # #             padding: 1.3rem 1.5rem;
# # # #             transition: transform 0.2s ease;
# # # #             backdrop-filter: blur(10px);
# # # #         }

# # # #         .stAlert:hover {
# # # #             transform: translateX(3px);
# # # #         }

# # # #         /* Success - Medical green */
# # # #         .stSuccess {
# # # #             background: linear-gradient(135deg, rgba(82, 209, 124, 0.15) 0%, rgba(82, 209, 124, 0.05) 100%) !important;
# # # #             border-left-color: var(--accent-green) !important;
# # # #             color: #2D7A4D !important;
# # # #         }

# # # #         /* Warning - Medical orange */
# # # #         .stWarning {
# # # #             background: linear-gradient(135deg, rgba(255, 159, 104, 0.15) 0%, rgba(255, 159, 104, 0.05) 100%) !important;
# # # #             border-left-color: var(--accent-orange) !important;
# # # #             color: #C16320 !important;
# # # #         }

# # # #         /* Error - Medical red */
# # # #         .stError {
# # # #             background: linear-gradient(135deg, rgba(255, 107, 107, 0.15) 0%, rgba(255, 107, 107, 0.05) 100%) !important;
# # # #             border-left-color: var(--accent-red) !important;
# # # #             color: #C13C3C !important;
# # # #         }

# # # #         /* Info - Medical blue */
# # # #         .stInfo {
# # # #             background: linear-gradient(135deg, rgba(74, 144, 226, 0.15) 0%, rgba(74, 144, 226, 0.05) 100%) !important;
# # # #             border-left-color: var(--primary-blue) !important;
# # # #             color: var(--dark-blue) !important;
# # # #         }

# # # #         /* Metric cards - Medical dashboard style */
# # # #         [data-testid="stMetric"] {
# # # #             background: var(--bg-white);
# # # #             padding: 1.5rem;
# # # #             border-radius: 14px;
# # # #             box-shadow: 0 4px 12px rgba(44, 95, 141, 0.08);
# # # #             border: 1px solid var(--border-color);
# # # #             transition: all 0.3s ease;
# # # #         }

# # # #         [data-testid="stMetric"]:hover {
# # # #             box-shadow: 0 8px 24px rgba(44, 95, 141, 0.15);
# # # #             transform: translateY(-3px);
# # # #         }

# # # #         [data-testid="stMetricValue"] {
# # # #             font-size: 2.4rem !important;
# # # #             font-weight: 800 !important;
# # # #             color: var(--primary-blue) !important;
# # # #         }

# # # #         [data-testid="stMetricLabel"] {
# # # #             font-size: 1.2rem !important;
# # # #             font-weight: 600 !important;
# # # #             color: #2C3E50 !important;
# # # #         }

# # # #         [data-testid="stMetricDelta"] {
# # # #             font-size: 1.05rem !important;
# # # #         }

# # # #         /* Expander - Medical style */
# # # #         .streamlit-expanderHeader {
# # # #             font-size: 1.25rem !important;
# # # #             font-weight: 600 !important;
# # # #             border-radius: 10px;
# # # #             background: var(--bg-white) !important;
# # # #             border: 2px solid var(--border-color) !important;
# # # #             padding: 1rem 1.5rem !important;
# # # #             transition: all 0.3s ease;
# # # #         }

# # # #         .streamlit-expanderHeader:hover {
# # # #             background: var(--light-blue) !important;
# # # #             border-color: var(--primary-blue) !important;
# # # #         }

# # # #         /* Radio buttons - Medical style */
# # # #         .stRadio > label {
# # # #             font-size: 1.3rem !important;
# # # #             font-weight: 700 !important;
# # # #             color: #2C3E50 !important;
# # # #         }

# # # #         .stRadio > div {
# # # #             font-size: 1.15rem !important;
# # # #             gap: 1rem;
# # # #         }

# # # #         .stRadio > div > label {
# # # #             background: var(--bg-white);
# # # #             padding: 0.8rem 1.5rem;
# # # #             border-radius: 10px;
# # # #             border: 2px solid var(--border-color);
# # # #             transition: all 0.3s ease;
# # # #         }

# # # #         .stRadio > div > label:hover {
# # # #             border-color: var(--primary-blue);
# # # #             background: var(--light-blue);
# # # #         }

# # # #         /* Dataframe styling */
# # # #         .dataframe {
# # # #             font-size: 1.1rem !important;
# # # #             border-radius: 12px !important;
# # # #         }

# # # #         .dataframe th {
# # # #             background: var(--primary-blue) !important;
# # # #             color: white !important;
# # # #             font-weight: 700 !important;
# # # #             font-size: 1.15rem !important;
# # # #             padding: 1rem !important;
# # # #         }

# # # #         .dataframe td {
# # # #             padding: 0.9rem !important;
# # # #             font-size: 1.1rem !important;
# # # #         }

# # # #         /* Form styling */
# # # #         .stForm {
# # # #             background: var(--bg-white);
# # # #             padding: 2rem;
# # # #             border-radius: 16px;
# # # #             border: 2px solid var(--border-color);
# # # #             box-shadow: 0 8px 24px rgba(44, 95, 141, 0.08);
# # # #         }

# # # #         /* Divider */
# # # #         hr {
# # # #             margin: 2.5rem 0;
# # # #             border: none;
# # # #             height: 2px;
# # # #             background: linear-gradient(90deg, transparent 0%, var(--primary-blue) 50%, transparent 100%);
# # # #             opacity: 0.3;
# # # #         }

# # # #         /* Animation */
# # # #         @keyframes fadeIn {
# # # #             from { opacity: 0; transform: translateY(15px); }
# # # #             to { opacity: 1; transform: translateY(0); }
# # # #         }

# # # #         .element-container {
# # # #             animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
# # # #         }

# # # #         /* Login container - Medical theme */
# # # #         .login-container {
# # # #             display: flex;
# # # #             justify-content: center;
# # # #             align-items: center;
# # # #             min-height: 65vh;
# # # #             padding: 2rem;
# # # #         }

# # # #         .login-box {
# # # #             background: var(--bg-white);
# # # #             padding: 3.5rem;
# # # #             border-radius: 20px;
# # # #             box-shadow: 0 20px 60px rgba(44, 95, 141, 0.15);
# # # #             max-width: 500px;
# # # #             width: 100%;
# # # #             border: 2px solid var(--border-color);
# # # #         }

# # # #         .login-title {
# # # #             font-size: 2.4rem !important;
# # # #             font-weight: 800 !important;
# # # #             text-align: center;
# # # #             margin-bottom: 2rem !important;
# # # #             color: var(--dark-blue) !important;
# # # #         }

# # # #         .login-subtitle {
# # # #             font-size: 1.2rem !important;
# # # #             text-align: center;
# # # #             color: #2C3E50 !important;
# # # #             margin-bottom: 2rem !important;
# # # #         }

# # # #         /* Medical icon styling */
# # # #         .medical-icon {
# # # #             font-size: 1.4rem;
# # # #             margin-right: 0.5rem;
# # # #         }

# # # #         /* Card containers */
# # # #         .medical-card {
# # # #             background: var(--bg-white);
# # # #             border-radius: 16px;
# # # #             padding: 2rem;
# # # #             box-shadow: 0 6px 20px rgba(44, 95, 141, 0.1);
# # # #             border: 1px solid var(--border-color);
# # # #             transition: all 0.3s ease;
# # # #         }

# # # #         .medical-card:hover {
# # # #             box-shadow: 0 12px 32px rgba(44, 95, 141, 0.15);
# # # #             transform: translateY(-5px);
# # # #         }

# # # #         /* Download button */
# # # #         .stDownloadButton > button {
# # # #             background: linear-gradient(135deg, var(--accent-teal) 0%, var(--accent-green) 100%);
# # # #             color: white;
# # # #             border: none;
# # # #             border-radius: 12px;
# # # #             padding: 0.9rem 2rem;
# # # #             font-size: 1.15rem !important;
# # # #             font-weight: 600;
# # # #             box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
# # # #         }

# # # #         .stDownloadButton > button:hover {
# # # #             transform: translateY(-2px);
# # # #             box-shadow: 0 8px 20px rgba(78, 205, 196, 0.4);
# # # #         }

# # # #         /* Tabs styling */
# # # #         .stTabs [data-baseweb="tab-list"] {
# # # #             gap: 1rem;
# # # #         }

# # # #         .stTabs [data-baseweb="tab"] {
# # # #             font-size: 1.2rem !important;
# # # #             font-weight: 600 !important;
# # # #             padding: 1rem 2rem;
# # # #             border-radius: 10px;
# # # #             color: #2C3E50 !important;
# # # #         }

# # # #         .stTabs [aria-selected="true"] {
# # # #             background: var(--primary-blue) !important;
# # # #             color: white !important;
# # # #         }
# # # #         </style>
# # # #         """,
# # # #         unsafe_allow_html=True,
# # # #     )


# # # # def admin_login_section() -> bool:
# # # #     """Medical-themed centered login form."""

# # # #     if st.session_state.get(AUTH_STATUS_KEY) is True:
# # # #         st.sidebar.success("✅ Authenticated as Health Authority")
# # # #         if st.sidebar.button("🚪 Logout", use_container_width=True):
# # # #             st.session_state[AUTH_STATUS_KEY] = False
# # # #             st.rerun()
# # # #         return True

# # # #     # Centered login UI
# # # #     st.markdown('<div class="login-container">', unsafe_allow_html=True)

# # # #     col1, col2, col3 = st.columns([1, 2, 1])

# # # #     with col2:
# # # #         st.markdown('<div class="login-box">', unsafe_allow_html=True)

# # # #         # Medical icon
# # # #         st.markdown(
# # # #             """
# # # #             <div style='text-align: center; margin-bottom: 2rem;'>
# # # #                 <div style='font-size: 4rem;'>🏥</div>
# # # #             </div>
# # # #             """,
# # # #             unsafe_allow_html=True,
# # # #         )

# # # #         st.markdown(
# # # #             '<h2 class="login-title">Health Authority Portal</h2>',
# # # #             unsafe_allow_html=True,
# # # #         )
# # # #         st.markdown(
# # # #             '<p class="login-subtitle">Secure access for authorized personnel</p>',
# # # #             unsafe_allow_html=True,
# # # #         )

# # # #         with st.form("admin_login_form"):
# # # #             pw = st.text_input(
# # # #                 "🔐 Administrator Password",
# # # #                 type="password",
# # # #                 placeholder="Enter secure password",
# # # #             )
# # # #             st.markdown("<br>", unsafe_allow_html=True)
# # # #             submitted = st.form_submit_button(
# # # #                 "🔓 Access Dashboard", use_container_width=True
# # # #             )

# # # #             if submitted:
# # # #                 if pw == ADMIN_PASSWORD:
# # # #                     st.session_state[AUTH_STATUS_KEY] = True
# # # #                     st.success("✅ Authentication successful! Redirecting...")
# # # #                     # st.balloons()
# # # #                     time.sleep(1)
# # # #                     st.rerun()
# # # #                 else:
# # # #                     st.error("❌ Invalid credentials. Access denied.")
# # # #                     st.session_state[AUTH_STATUS_KEY] = False

# # # #         st.markdown("</div>", unsafe_allow_html=True)

# # # #         # Hint box
# # # #         st.info("💡 **Demo Access**: Default password is 'admin123'")

# # # #     st.markdown("</div>", unsafe_allow_html=True)

# # # #     return False


# # # # def main() -> None:
# # # #     st.set_page_config(
# # # #         page_title="Health Risk Monitoring Portal",
# # # #         page_icon="🏥",
# # # #         layout="wide",
# # # #         initial_sidebar_state="expanded",
# # # #     )
# # # #     _inject_base_css()

# # # #     # Main header with medical theme
# # # #     st.markdown(
# # # #         """
# # # #         <div style='text-align: center; padding: 2rem 0 1rem 0;'>
# # # #             <div style='font-size: 4.5rem; margin-bottom: 1rem;'>🏥</div>
# # # #         </div>
# # # #         """,
# # # #         unsafe_allow_html=True,
# # # #     )

# # # #     st.title("Environmental Health Risk Monitoring Portal")
# # # #     st.markdown(
# # # #         """
# # # #         <p style='font-size: 1.35rem; color: #2C3E50; text-align: center;
# # # #                   margin-bottom: 2.5rem; font-weight: 500;'>
# # # #         Real-time monitoring and personalized risk assessment system for environmental health hazards
# # # #         </p>
# # # #         """,
# # # #         unsafe_allow_html=True,
# # # #     )
# # # #     st.markdown("---")

# # # #     # Sidebar navigation
# # # #     st.sidebar.markdown("### 🎯 Navigation")
# # # #     role = st.sidebar.radio(
# # # #         "Select Dashboard View:",
# # # #         ["👤 Citizen Dashboard", "🏛️ Health Authority Dashboard"],
# # # #         index=0,
# # # #     )

# # # #     st.sidebar.markdown("---")
# # # #     st.sidebar.markdown("### 📊 System Status")
# # # #     st.sidebar.info("🌍 **Cities**: 5 locations monitored")
# # # #     st.sidebar.success("✅ **Status**: System operational")
# # # #     st.sidebar.info("🔄 **Updates**: Real-time data sync")

# # # #     if role.startswith("👤 Citizen"):
# # # #         render_citizen_dashboard()

# # # #     elif role.startswith("🏛️ Health"):
# # # #         if admin_login_section():
# # # #             render_admin_dashboard()


# # # # if __name__ == "__main__":
# # # #     main()
# # # # src/dashboard/main_dashboard.py

# # # import os
# # # import time
# # # import streamlit as st

# # # from src.dashboard.admin_dashboard import render_admin_dashboard
# # # from src.dashboard.citizen_dashboard import render_citizen_dashboard

# # # ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
# # # AUTH_STATUS_KEY = "auth_status"


# # # def _inject_base_css() -> None:
# # #     """Professional medical-themed CSS with improved readability."""
# # #     st.markdown(
# # #         """
# # #         <style>
# # #         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

# # #         * {
# # #             font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
# # #         }

# # #         :root {
# # #             --primary: #2563EB;
# # #             --primary-dark: #1E40AF;
# # #             --primary-light: #3B82F6;
# # #             --secondary: #10B981;
# # #             --danger: #EF4444;
# # #             --warning: #F59E0B;
# # #             --bg-main: #F8FAFC;
# # #             --bg-card: #FFFFFF;
# # #             --text-primary: #1E293B;
# # #             --text-secondary: #475569;
# # #             --text-light: #78909C;
# # #             --border: #E2E8F0;
# # #         }

# # #         .stApp {
# # #             background: var(--bg-main);
# # #         }

# # #         .block-container {
# # #             padding: 3rem 2rem;
# # #             max-width: 1400px;
# # #         }

# # #         /* Sidebar */
# # #         section[data-testid="stSidebar"] {
# # #             background: linear-gradient(180deg, #1E40AF 0%, #1E3A8A 100%);
# # #             border-right: none;
# # #         }

# # #         section[data-testid="stSidebar"] * {
# # #             color: #2C3E50 !important;
# # #         }

# # #         section[data-testid="stSidebar"] h3 {
# # #             color: #2C3E50 !important;
# # #             font-size: 1.1rem !important;
# # #             font-weight: 700 !important;
# # #             border-bottom: 2px solid rgba(255,255,255,0.2);
# # #             padding-bottom: 0.75rem;
# # #             margin-bottom: 1rem;
# # #         }

# # #         section[data-testid="stSidebar"] .stRadio > label {
# # #             color: #2C3E50 !important;
# # #             font-size: 1rem !important;
# # #             font-weight: 600 !important;
# # #         }

# # #         /* Typography */
# # #         h1 {
# # #             font-size: 2.75rem !important;
# # #             font-weight: 800 !important;
# # #             color: #2C3E50 !important;
# # #             letter-spacing: -0.02em;
# # #             margin-bottom: 0.5rem !important;
# # #         }

# # #         h2 {
# # #             font-size: 2rem !important;
# # #             font-weight: 700 !important;
# # #             color: #2C3E50 !important;
# # #         }

# # #         h3 {
# # #             font-size: 1.5rem !important;
# # #             font-weight: 700 !important;
# # #             color: #2C3E50 !important;
# # #         }

# # #         h4 {
# # #             font-size: 1.25rem !important;
# # #             font-weight: 600 !important;
# # #             color: #2C3E50 !important;
# # #         }

# # #         p, div, span, label {
# # #             font-size: 1rem !important;
# # #             color: #2C3E50 !important;
# # #             line-height: 1.6;
# # #         }

# # #         label {
# # #             font-weight: 600 !important;
# # #             color: #2C3E50 !important;
# # #             font-size: 0.95rem !important;
# # #         }

# # #         .stCaption {
# # #             font-size: 0.875rem !important;
# # #             color: #2C3E50 !important;
# # #         }

# # #         /* Buttons */
# # #         .stButton > button {
# # #             background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
# # #             color: white !important;
# # #             border: none;
# # #             border-radius: 8px;
# # #             padding: 0.75rem 2rem;
# # #             font-size: 1rem !important;
# # #             font-weight: 600;
# # #             transition: all 0.2s;
# # #             box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
# # #         }

# # #         .stButton > button:hover {
# # #             transform: translateY(-2px);
# # #             box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
# # #         }

# # #         /* Inputs */
# # #         .stTextInput > div > div > input,
# # #         .stNumberInput > div > div > input,
# # #         .stSelectbox > div > div > select {
# # #             font-size: 0.95rem !important;
# # #             border: 2px solid var(--border) !important;
# # #             border-radius: 8px !important;
# # #             padding: 0.625rem 0.875rem !important;
# # #             color: #2C3E50 !important;
# # #             background: white !important;
# # #         }

# # #         .stTextInput > div > div > input:focus,
# # #         .stNumberInput > div > div > input:focus,
# # #         .stSelectbox > div > div > select:focus {
# # #             border-color: var(--primary) !important;
# # #             box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
# # #         }

# # #         /* Sliders */
# # #         .stSlider > div > div > div {
# # #             background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%) !important;
# # #         }

# # #         /* Alerts */
# # #         .stSuccess {
# # #             background: rgba(16, 185, 129, 0.1) !important;
# # #             border-left: 4px solid var(--secondary) !important;
# # #             color: #065F46 !important;
# # #             font-size: 0.95rem !important;
# # #         }

# # #         .stError {
# # #             background: rgba(239, 68, 68, 0.1) !important;
# # #             border-left: 4px solid var(--danger) !important;
# # #             color: #991B1B !important;
# # #             font-size: 0.95rem !important;
# # #         }

# # #         .stWarning {
# # #             background: rgba(245, 158, 11, 0.1) !important;
# # #             border-left: 4px solid var(--warning) !important;
# # #             color: #92400E !important;
# # #             font-size: 0.95rem !important;
# # #         }

# # #         .stInfo {
# # #             background: rgba(37, 99, 235, 0.1) !important;
# # #             border-left: 4px solid var(--primary) !important;
# # #             color: #1E3A8A !important;
# # #             font-size: 0.95rem !important;
# # #         }

# # #         /* Metrics */
# # #         [data-testid="stMetric"] {
# # #             background: white;
# # #             padding: 1.25rem;
# # #             border-radius: 12px;
# # #             border: 1px solid var(--border);
# # #             box-shadow: 0 1px 3px rgba(0,0,0,0.05);
# # #         }

# # #         [data-testid="stMetricValue"] {
# # #             font-size: 2rem !important;
# # #             font-weight: 800 !important;
# # #             color: var(--primary) !important;
# # #         }

# # #         [data-testid="stMetricLabel"] {
# # #             font-size: 0.875rem !important;
# # #             font-weight: 600 !important;
# # #             color: #2C3E50 !important;
# # #             text-transform: uppercase;
# # #             letter-spacing: 0.05em;
# # #         }

# # #         /* Expander */
# # #         .streamlit-expanderHeader {
# # #             font-size: 1rem !important;
# # #             font-weight: 600 !important;
# # #             background: white !important;
# # #             border: 1px solid var(--border) !important;
# # #             border-radius: 8px;
# # #         }

# # #         /* Radio */
# # #         .stRadio > div > label {
# # #             background: white;
# # #             padding: 0.625rem 1rem;
# # #             border-radius: 8px;
# # #             border: 2px solid var(--border);
# # #             margin-right: 0.5rem;
# # #         }

# # #         .stRadio > div > label:has(input:checked) {
# # #             border-color: var(--primary);
# # #             background: rgba(37, 99, 235, 0.05);
# # #         }

# # #         /* Dataframe */
# # #         .dataframe th {
# # #             background: var(--primary) !important;
# # #             color: white !important;
# # #             font-weight: 700 !important;
# # #             font-size: 0.875rem !important;
# # #         }

# # #         /* Tabs */
# # #         .stTabs [data-baseweb="tab"] {
# # #             font-size: 1rem !important;
# # #             font-weight: 600 !important;
# # #             color: #2C3E50 !important;
# # #         }

# # #         .stTabs [aria-selected="true"] {
# # #             color: var(--primary) !important;
# # #             border-bottom-color: var(--primary) !important;
# # #         }

# # #         hr {
# # #             margin: 2rem 0;
# # #             border: none;
# # #             height: 1px;
# # #             background: var(--border);
# # #         }
# # #         </style>
# # #         """,
# # #         unsafe_allow_html=True,
# # #     )


# # # def admin_login_section() -> bool:
# # #     """Centered login form for admin access."""

# # #     if st.session_state.get(AUTH_STATUS_KEY) is True:
# # #         st.sidebar.success("✅ Authenticated")
# # #         if st.sidebar.button("🚪 Logout", use_container_width=True):
# # #             st.session_state[AUTH_STATUS_KEY] = False
# # #             st.rerun()
# # #         return True

# # #     # Center the login box
# # #     st.markdown("<br><br><br>", unsafe_allow_html=True)

# # #     col1, col2, col3 = st.columns([1, 1.5, 1])

# # #     with col2:
# # #         st.markdown(
# # #             """
# # #             <div style='background: white; padding: 3rem; border-radius: 16px;
# # #                         box-shadow: 0 10px 40px rgba(0,0,0,0.08); border: 1px solid #E2E8F0;'>
# # #                 <div style='text-align: center; margin-bottom: 2rem;'>
# # #                     <div style='font-size: 4rem; margin-bottom: 1rem;'>🏥</div>
# # #                     <h2 style='color: #2C3E50; margin: 0; font-size: 1.75rem; font-weight: 800;'>
# # #                         Health Authority Portal
# # #                     </h2>
# # #                     <p style='color: #2C3E50; margin-top: 0.5rem; font-size: 1rem;'>
# # #                         Secure access for authorized personnel
# # #                     </p>
# # #                 </div>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # #         with st.form("admin_login_form"):
# # #             pw = st.text_input(
# # #                 "🔐 Password",
# # #                 type="password",
# # #                 placeholder="Enter administrator password",
# # #             )
# # #             st.markdown("<br>", unsafe_allow_html=True)
# # #             submitted = st.form_submit_button(
# # #                 "Access Dashboard", use_container_width=True
# # #             )

# # #             if submitted:
# # #                 if pw == ADMIN_PASSWORD:
# # #                     st.session_state[AUTH_STATUS_KEY] = True
# # #                     st.success("✅ Authentication successful!")
# # #                     time.sleep(1)
# # #                     st.rerun()
# # #                 else:
# # #                     st.error("❌ Invalid credentials")
# # #                     st.session_state[AUTH_STATUS_KEY] = False

# # #         st.info("💡 Demo password: admin123")

# # #     return False


# # # def main() -> None:
# # #     st.set_page_config(
# # #         page_title="Health Risk Monitoring Portal",
# # #         page_icon="🏥",
# # #         layout="wide",
# # #         initial_sidebar_state="expanded",
# # #     )
# # #     _inject_base_css()

# # #     # Header
# # #     st.markdown(
# # #         """
# # #         <div style='text-align: center; padding: 1rem 0;'>
# # #             <div style='font-size: 3.5rem; margin-bottom: 0.5rem;'>🏥</div>
# # #         </div>
# # #         """,
# # #         unsafe_allow_html=True,
# # #     )

# # #     st.title("Environmental Health Risk Monitoring Portal")
# # #     st.markdown(
# # #         """
# # #         <p style='font-size: 1.125rem; color: #2C3E50; text-align: center;
# # #                   margin-bottom: 2rem; font-weight: 500;'>
# # #         Advanced monitoring and personalized risk assessment for environmental health
# # #         </p>
# # #         """,
# # #         unsafe_allow_html=True,
# # #     )
# # #     st.markdown("---")

# # #     # Sidebar
# # #     st.sidebar.markdown("### Navigation")
# # #     role = st.sidebar.radio(
# # #         "Select View:",
# # #         ["👤 Citizen Dashboard", "🏛️ Health Authority"],
# # #         index=0,
# # #     )

# # #     st.sidebar.markdown("---")
# # #     st.sidebar.markdown("### System Status")
# # #     st.sidebar.info("🌍 **5** cities monitored")
# # #     st.sidebar.success("✅ System operational")
# # #     st.sidebar.info("🔄 Real-time sync active")

# # #     if role.startswith("👤"):
# # #         render_citizen_dashboard()
# # #     elif role.startswith("🏛️"):
# # #         if admin_login_section():
# # #             render_admin_dashboard()


# # # if __name__ == "__main__":
# # #     main()
# # import os
# # import time
# # import streamlit as st

# # from src.dashboard.admin_dashboard import render_admin_dashboard
# # from src.dashboard.citizen_dashboard import render_citizen_dashboard

# # ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
# # AUTH_STATUS_KEY = "auth_status"


# # def _inject_base_css() -> None:
# #     """Modern professional CSS with enhanced color scheme."""
# #     st.markdown(
# #         """
# #         <style>
# #         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

# #         * {
# #             font-family: 'Inter', sans-serif;
# #         }

# #         :root {
# #             --primary: #0066FF;
# #             --primary-dark: #0052CC;
# #             --secondary: #00C896;
# #             --danger: #FF4757;
# #             --warning: #FFA502;
# #             --bg-main: #F7F9FC;
# #             --bg-card: #FFFFFF;
# #             --text-primary: #1E293B;
# #             --text-secondary: #475569;
# #             --border: #E2E8F0;
# #             --shadow: 0 2px 8px rgba(0,0,0,0.08);
# #         }

# #         .stApp {
# #             background: var(--bg-main);
# #         }

# #         .block-container {
# #             padding: 2rem 3rem;
# #             max-width: 1400px;
# #         }

# #         /* Modern Sidebar */
# #         section[data-testid="stSidebar"] {
# #             background: linear-gradient(180deg, #1A365D 0%, #0F172A 100%);
# #             border-right: 1px solid rgba(255,255,255,0.1);
# #         }

# #         section[data-testid="stSidebar"] * {
# #             color: #2C3E50 !important;
# #         }

# #         section[data-testid="stSidebar"] h3 {
# #             font-size: 1.1rem !important;
# #             font-weight: 700 !important;
# #             text-transform: uppercase;
# #             letter-spacing: 1px;
# #             border-bottom: 2px solid rgba(255,255,255,0.2);
# #             padding-bottom: 0.75rem;
# #             margin: 1.5rem 0 1rem 0;
# #         }

# #         section[data-testid="stSidebar"] .stRadio > label {
# #             font-size: 0.95rem !important;
# #             font-weight: 600 !important;
# #         }

# #         section[data-testid="stSidebar"] .stRadio > div > label {
# #             background: rgba(255,255,255,0.08);
# #             padding: 0.75rem 1rem;
# #             border-radius: 8px;
# #             margin-bottom: 0.5rem;
# #             transition: all 0.3s;
# #             border: 1px solid transparent;
# #         }

# #         section[data-testid="stSidebar"] .stRadio > div > label:hover {
# #             background: rgba(255,255,255,0.12);
# #             border-color: rgba(255,255,255,0.2);
# #         }

# #         section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
# #             background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
# #             border-color: #0066FF;
# #             box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
# #         }

# #         /* Typography */
# #         h1 {
# #             font-size: 3rem !important;
# #             font-weight: 800 !important;
# #             color: #2C3E50 !important;
# #             margin-bottom: 0.5rem !important;
# #         }

# #         h2 {
# #             font-size: 2.25rem !important;
# #             font-weight: 700 !important;
# #             color: #2C3E50 !important;
# #         }

# #         h3 {
# #             font-size: 1.75rem !important;
# #             font-weight: 700 !important;
# #             color: #2C3E50 !important;
# #             margin: 2rem 0 1rem 0 !important;
# #         }

# #         h4 {
# #             font-size: 1.35rem !important;
# #             font-weight: 600 !important;
# #             color: #2C3E50 !important;
# #         }

# #         p, div, span, label {
# #             font-size: 1.05rem !important;
# #             color: #2C3E50 !important;
# #             line-height: 1.6;
# #         }

# #         label {
# #             font-weight: 600 !important;
# #             color: #2C3E50 !important;
# #             font-size: 1rem !important;
# #         }

# #         .stCaption {
# #             font-size: 0.9rem !important;
# #             color: #718096 !important;
# #         }

# #         /* Modern Buttons */
# #         .stButton > button {
# #             background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
# #             color: white !important;
# #             border: none;
# #             border-radius: 10px;
# #             padding: 0.85rem 2.5rem;
# #             font-size: 1.05rem !important;
# #             font-weight: 700;
# #             transition: all 0.3s;
# #             box-shadow: 0 4px 14px rgba(0, 102, 255, 0.3);
# #             letter-spacing: 0.3px;
# #         }

# #         .stButton > button:hover {
# #             transform: translateY(-2px);
# #             box-shadow: 0 8px 20px rgba(0, 102, 255, 0.4);
# #         }

# #         /* Inputs */
# #         .stTextInput > div > div > input,
# #         .stNumberInput > div > div > input,
# #         .stSelectbox > div > div > select {
# #             font-size: 1rem !important;
# #             border: 2px solid var(--border) !important;
# #             border-radius: 10px !important;
# #             padding: 0.75rem 1rem !important;
# #             color: #2C3E50 !important;
# #             background: white !important;
# #             transition: all 0.3s;
# #         }

# #         .stTextInput > div > div > input:focus,
# #         .stNumberInput > div > div > input:focus,
# #         .stSelectbox > div > div > select:focus {
# #             border-color: var(--primary) !important;
# #             box-shadow: 0 0 0 4px rgba(0, 102, 255, 0.1) !important;
# #         }

# #         /* Sliders */
# #         .stSlider > div > div > div {
# #             background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
# #         }

# #         .stSlider > div > div > div > div {
# #             background: white !important;
# #             border: 3px solid var(--primary) !important;
# #         }

# #         /* Alerts */
# #         .stSuccess {
# #             background: rgba(0, 200, 150, 0.1) !important;
# #             border-left: 5px solid var(--secondary) !important;
# #             color: #047857 !important;
# #             font-size: 1rem !important;
# #             padding: 1rem 1.25rem !important;
# #         }

# #         .stError {
# #             background: rgba(255, 71, 87, 0.1) !important;
# #             border-left: 5px solid var(--danger) !important;
# #             color: #C81E1E !important;
# #             font-size: 1rem !important;
# #             padding: 1rem 1.25rem !important;
# #         }

# #         .stWarning {
# #             background: rgba(255, 165, 2, 0.1) !important;
# #             border-left: 5px solid var(--warning) !important;
# #             color: #B45309 !important;
# #             font-size: 1rem !important;
# #             padding: 1rem 1.25rem !important;
# #         }

# #         .stInfo {
# #             background: rgba(0, 102, 255, 0.1) !important;
# #             border-left: 5px solid var(--primary) !important;
# #             color: #1E40AF !important;
# #             font-size: 1rem !important;
# #             padding: 1rem 1.25rem !important;
# #         }

# #         /* Metrics */
# #         [data-testid="stMetric"] {
# #             background: white;
# #             padding: 1.5rem;
# #             border-radius: 12px;
# #             border: 1px solid var(--border);
# #             box-shadow: var(--shadow);
# #             transition: all 0.3s;
# #         }

# #         [data-testid="stMetric"]:hover {
# #             box-shadow: 0 4px 16px rgba(0,0,0,0.12);
# #             transform: translateY(-2px);
# #         }

# #         [data-testid="stMetricValue"] {
# #             font-size: 2.25rem !important;
# #             font-weight: 800 !important;
# #             color: var(--primary) !important;
# #         }

# #         [data-testid="stMetricLabel"] {
# #             font-size: 0.9rem !important;
# #             font-weight: 700 !important;
# #             color: #2C3E50 !important;
# #             text-transform: uppercase;
# #             letter-spacing: 0.5px;
# #         }

# #         /* Tabs */
# #         .stTabs [data-baseweb="tab-list"] {
# #             gap: 0.5rem;
# #         }

# #         .stTabs [data-baseweb="tab"] {
# #             font-size: 1.05rem !important;
# #             font-weight: 600 !important;
# #             color: #2C3E50 !important;
# #             padding: 0.75rem 1.5rem;
# #             border-radius: 8px 8px 0 0;
# #         }

# #         .stTabs [aria-selected="true"] {
# #             background: white !important;
# #             color: var(--primary) !important;
# #             border-bottom: 3px solid var(--primary) !important;
# #         }

# #         /* Dataframe */
# #         .dataframe {
# #             font-size: 1rem !important;
# #         }

# #         .dataframe th {
# #             background: var(--primary) !important;
# #             color: white !important;
# #             font-weight: 700 !important;
# #             font-size: 0.95rem !important;
# #             padding: 1rem !important;
# #         }

# #         .dataframe td {
# #             padding: 0.85rem !important;
# #         }

# #         /* Expander */
# #         .streamlit-expanderHeader {
# #             font-size: 1.05rem !important;
# #             font-weight: 600 !important;
# #             background: white !important;
# #             border: 1px solid var(--border) !important;
# #             border-radius: 10px;
# #             padding: 1rem !important;
# #         }

# #         hr {
# #             margin: 2.5rem 0;
# #             border: none;
# #             height: 1px;
# #             background: linear-gradient(90deg, transparent, var(--border), transparent);
# #         }
# #         </style>
# #         """,
# #         unsafe_allow_html=True,
# #     )


# # def admin_login_section() -> bool:
# #     """Modern centered login form."""

# #     if st.session_state.get(AUTH_STATUS_KEY) is True:
# #         st.sidebar.success("✅ Authenticated")
# #         if st.sidebar.button("🚪 Logout", use_container_width=True):
# #             st.session_state[AUTH_STATUS_KEY] = False
# #             st.rerun()
# #         return True

# #     st.markdown("<br><br>", unsafe_allow_html=True)

# #     col1, col2, col3 = st.columns([1, 1.2, 1])

# #     with col2:
# #         st.markdown(
# #             """
# #             <div style='background: white; padding: 3rem 2.5rem; border-radius: 16px;
# #                         box-shadow: 0 10px 40px rgba(0,0,0,0.1); border: 1px solid #E2E8F0;'>
# #                 <div style='text-align: center; margin-bottom: 2rem;'>
# #                     <div style='font-size: 4rem; margin-bottom: 1rem;'>🏥</div>
# #                     <h2 style='color: #2C3E50; margin: 0; font-size: 2rem; font-weight: 800;'>
# #                         Health Authority Portal
# #                     </h2>
# #                     <p style='color: #718096; margin-top: 0.75rem; font-size: 1.05rem;'>
# #                         Secure access for authorized personnel
# #                     </p>
# #                 </div>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )

# #         with st.form("admin_login_form"):
# #             pw = st.text_input(
# #                 "🔐 Password",
# #                 type="password",
# #                 placeholder="Enter administrator password",
# #             )
# #             st.markdown("<br>", unsafe_allow_html=True)
# #             submitted = st.form_submit_button(
# #                 "Access Dashboard", use_container_width=True
# #             )

# #             if submitted:
# #                 if pw == ADMIN_PASSWORD:
# #                     st.session_state[AUTH_STATUS_KEY] = True
# #                     st.success("✅ Authentication successful!")
# #                     time.sleep(0.8)
# #                     st.rerun()
# #                 else:
# #                     st.error("❌ Invalid credentials")
# #                     st.session_state[AUTH_STATUS_KEY] = False

# #         st.info("💡 Demo password: admin123")

# #     return False


# # def main() -> None:
# #     st.set_page_config(
# #         page_title="Health Risk Monitoring Portal",
# #         page_icon="🏥",
# #         layout="wide",
# #         initial_sidebar_state="expanded",
# #     )
# #     _inject_base_css()

# #     # Modern Header
# #     st.markdown(
# #         """
# #         <div style='text-align: center; padding: 1.5rem 0;'>
# #             <div style='font-size: 4rem; margin-bottom: 0.5rem;'>🏥</div>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# #     st.title("Environmental Health Risk Monitoring Portal")
# #     st.markdown(
# #         """
# #         <p style='font-size: 1.2rem; color: #2C3E50; text-align: center;
# #                   margin-bottom: 2.5rem; font-weight: 500;'>
# #         Advanced monitoring and personalized risk assessment for environmental health
# #         </p>
# #         """,
# #         unsafe_allow_html=True,
# #     )
# #     st.markdown("---")

# #     # Modern Sidebar
# #     st.sidebar.markdown("### Navigation")
# #     role = st.sidebar.radio(
# #         "Select View:",
# #         ["👤 Citizen Dashboard", "🏛️ Health Authority"],
# #         index=0,
# #     )

# #     st.sidebar.markdown("---")
# #     st.sidebar.markdown("### System Status")
# #     st.sidebar.success("🌍 **5** cities monitored")
# #     st.sidebar.info("✅ System operational")
# #     st.sidebar.success("🔄 Real-time sync active")

# #     if role.startswith("👤"):
# #         render_citizen_dashboard()
# #     elif role.startswith("🏛️"):
# #         if admin_login_section():
# #             render_admin_dashboard()


# # if __name__ == "__main__":
# #     main()
# import os
# import time
# import streamlit as st

# from src.dashboard.admin_dashboard import render_admin_dashboard
# from src.dashboard.citizen_dashboard import render_citizen_dashboard

# ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
# AUTH_STATUS_KEY = "auth_status"
# ROLE_SELECTED_KEY = "role_selected"
# SELECTED_ROLE_KEY = "selected_role"


# def _inject_base_css() -> None:
#     """Modern professional CSS with enhanced design."""
#     st.markdown(
#         """
#         <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

#         * {
#             font-family: 'Inter', sans-serif;
#         }

#         :root {
#             --primary: #0066FF;
#             --primary-dark: #0052CC;
#             --secondary: #10B981;
#             --danger: #EF4444;
#             --warning: #F59E0B;
#             --bg-main: #F9FAFB;
#             --bg-card: #FFFFFF;
#             --text-primary: #1E293B;
#             --text-secondary: #475569;
#             --border: #E5E7EB;
#             --shadow: 0 4px 12px rgba(0,0,0,0.08);
#         }

#         .stApp {
#             background: linear-gradient(135deg, #F0F9FF 0%, #F9FAFB 100%);
#         }

#         .block-container {
#             padding: 2rem 3rem;
#             max-width: 1400px;
#         }

#         /* Modern Sidebar */
#         section[data-testid="stSidebar"] {
#             background: linear-gradient(180deg, #1E3A8A 0%, #1E293B 100%);
#             border-right: 1px solid rgba(255,255,255,0.1);
#         }

#         section[data-testid="stSidebar"] * {
#             color: #2C3E50 !important;
#         }

#         section[data-testid="stSidebar"] h3 {
#             font-size: 1.1rem !important;
#             font-weight: 700 !important;
#             text-transform: uppercase;
#             letter-spacing: 1px;
#             border-bottom: 2px solid rgba(255,255,255,0.2);
#             padding-bottom: 0.75rem;
#             margin: 1.5rem 0 1rem 0;
#         }

#         section[data-testid="stSidebar"] .stRadio > div > label {
#             background: rgba(255,255,255,0.08);
#             padding: 0.75rem 1rem;
#             border-radius: 8px;
#             margin-bottom: 0.5rem;
#             transition: all 0.3s;
#             border: 1px solid transparent;
#         }

#         section[data-testid="stSidebar"] .stRadio > div > label:hover {
#             background: rgba(255,255,255,0.12);
#             border-color: rgba(255,255,255,0.2);
#         }

#         section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
#             background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
#             border-color: #0066FF;
#             box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
#         }

#         /* Typography */
#         h1 {
#             font-size: 3rem !important;
#             font-weight: 900 !important;
#             color: #2C3E50 !important;
#             margin-bottom: 0.5rem !important;
#             letter-spacing: -0.02em;
#         }

#         h2 {
#             font-size: 2.25rem !important;
#             font-weight: 800 !important;
#             color: #2C3E50 !important;
#         }

#         h3 {
#             font-size: 1.75rem !important;
#             font-weight: 700 !important;
#             color: #2C3E50 !important;
#             margin: 2rem 0 1rem 0 !important;
#         }

#         p, div, span, label {
#             font-size: 1.05rem !important;
#             color: #2C3E50 !important;
#             line-height: 1.6;
#         }

#         label {
#             font-weight: 600 !important;
#             color: #2C3E50 !important;
#         }

#         /* Buttons */
#         .stButton > button {
#             background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
#             color: white !important;
#             border: none;
#             border-radius: 10px;
#             padding: 0.9rem 2.5rem;
#             font-size: 1.05rem !important;
#             font-weight: 700;
#             transition: all 0.3s;
#             box-shadow: 0 4px 14px rgba(0, 102, 255, 0.3);
#             letter-spacing: 0.3px;
#         }

#         .stButton > button:hover {
#             transform: translateY(-2px);
#             box-shadow: 0 8px 20px rgba(0, 102, 255, 0.4);
#         }

#         /* Inputs */
#         .stTextInput > div > div > input {
#             font-size: 1rem !important;
#             border: 2px solid var(--border) !important;
#             border-radius: 10px !important;
#             padding: 0.75rem 1rem !important;
#             background: white !important;
#             transition: all 0.3s;
#         }

#         .stTextInput > div > div > input:focus {
#             border-color: var(--primary) !important;
#             box-shadow: 0 0 0 4px rgba(0, 102, 255, 0.1) !important;
#         }

#         /* Alerts */
#         .stSuccess {
#             background: rgba(16, 185, 129, 0.1) !important;
#             border-left: 5px solid var(--secondary) !important;
#             color: #047857 !important;
#             font-size: 1rem !important;
#             padding: 1rem 1.25rem !important;
#         }

#         .stError {
#             background: rgba(239, 68, 68, 0.1) !important;
#             border-left: 5px solid var(--danger) !important;
#             color: #DC2626 !important;
#             font-size: 1rem !important;
#             padding: 1rem 1.25rem !important;
#         }

#         .stInfo {
#             background: rgba(0, 102, 255, 0.1) !important;
#             border-left: 5px solid var(--primary) !important;
#             color: #1E40AF !important;
#             font-size: 1rem !important;
#             padding: 1rem 1.25rem !important;
#         }

#         /* Metrics */
#         [data-testid="stMetric"] {
#             background: white;
#             padding: 1.5rem;
#             border-radius: 12px;
#             border: 1px solid var(--border);
#             box-shadow: var(--shadow);
#             transition: all 0.3s;
#         }

#         [data-testid="stMetric"]:hover {
#             box-shadow: 0 6px 20px rgba(0,0,0,0.12);
#             transform: translateY(-3px);
#         }

#         [data-testid="stMetricValue"] {
#             font-size: 2.25rem !important;
#             font-weight: 800 !important;
#             color: var(--primary) !important;
#         }

#         hr {
#             margin: 2.5rem 0;
#             border: none;
#             height: 1px;
#             background: linear-gradient(90deg, transparent, var(--border), transparent);
#         }

#         /* Card hover effects */
#         .role-card {
#             transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
#         }

#         .role-card:hover {
#             transform: translateY(-8px);
#             box-shadow: 0 20px 40px rgba(0, 102, 255, 0.2);
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# def render_welcome_screen() -> None:
#     """Modern welcome screen with role selection."""

#     # Hero Header
#     st.markdown(
#         """
#         <div style='text-align: center; padding: 3rem 2rem 2rem 2rem;'>
#             <div style='display: inline-block; background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
#                         padding: 1.5rem; border-radius: 20px; margin-bottom: 1.5rem;
#                         box-shadow: 0 8px 24px rgba(0, 102, 255, 0.3);'>
#                 <div style='font-size: 4.5rem;'>🌍</div>
#             </div>
#             <h1 style='font-size: 3.5rem; font-weight: 900; color: #2C3E50;
#                        margin: 1rem 0 0.5rem 0; letter-spacing: -0.02em;'>
#                 EnviroSense 360
#             </h1>
#             <p style='font-size: 1.3rem; color: #2C3E50; font-weight: 500; max-width: 800px;
#                       margin: 0 auto 1rem auto; line-height: 1.6;'>
#                 Advanced Environmental Health Risk Monitoring & Assessment Platform
#             </p>
#             <p style='font-size: 1.05rem; color: #9CA3AF; max-width: 700px; margin: 0 auto;'>
#                 Real-time monitoring • AI-powered insights • Personalized health recommendations
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown("<br>", unsafe_allow_html=True)

#     # Welcome message
#     st.markdown(
#         """
#         <div style='background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
#                     padding: 2rem; border-radius: 14px; margin: 2rem auto; max-width: 900px;
#                     border: 2px solid #BAE6FD; box-shadow: 0 4px 12px rgba(0, 102, 255, 0.08);'>
#             <h3 style='color: #075985; font-size: 1.5rem; margin: 0 0 1rem 0; font-weight: 700;'>
#                 👋 Welcome to EnviroSense 360
#             </h3>
#             <p style='color: #0C4A6E; font-size: 1.05rem; margin: 0; line-height: 1.7;'>
#                 Your comprehensive solution for environmental health monitoring. Whether you're tracking your
#                 personal health metrics or managing population-wide health data, our AI-powered platform
#                 provides real-time insights and actionable recommendations.
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown("<br><br>", unsafe_allow_html=True)

#     # Role selection
#     st.markdown(
#         """
#         <div style='text-align: center; margin-bottom: 2rem;'>
#             <h2 style='font-size: 2rem; font-weight: 800; color: #2C3E50; margin-bottom: 0.5rem;'>
#                 Choose Your Dashboard
#             </h2>
#             <p style='font-size: 1.1rem; color: #2C3E50;'>
#                 Select the portal that matches your role
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     col1, col2, col3 = st.columns([1, 4, 1])

#     with col2:
#         card_col1, card_col2 = st.columns(2, gap="large")

#         with card_col1:
#             st.markdown(
#                 """
#                 <div class='role-card' style='background: white; padding: 3rem 2rem;
#                             border-radius: 16px; text-align: center;
#                             border: 2px solid #E5E7EB; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
#                             cursor: pointer;'>
#                     <div style='font-size: 5rem; margin-bottom: 1.5rem;'>👤</div>
#                     <h3 style='font-size: 1.75rem; font-weight: 800; color: #2C3E50; margin-bottom: 1rem;'>
#                         Citizen Portal
#                     </h3>
#                     <p style='font-size: 1.05rem; color: #2C3E50; margin-bottom: 2rem; line-height: 1.6;'>
#                         Track your personal health metrics, receive AI-powered risk assessments,
#                         and get personalized health recommendations.
#                     </p>
#                     <div style='background: #F0F9FF; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
#                         <p style='font-size: 0.95rem; color: #0369A1; margin: 0; font-weight: 600;'>
#                             ✓ Personal health tracking<br>
#                             ✓ Real-time risk assessment<br>
#                             ✓ Downloadable reports
#                         </p>
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             if st.button(
#                 "🚀 Access Citizen Portal", use_container_width=True, type="primary"
#             ):
#                 st.session_state[ROLE_SELECTED_KEY] = True
#                 st.session_state[SELECTED_ROLE_KEY] = "citizen"
#                 st.rerun()

#         with card_col2:
#             st.markdown(
#                 """
#                 <div class='role-card' style='background: white; padding: 3rem 2rem;
#                             border-radius: 16px; text-align: center;
#                             border: 2px solid #E5E7EB; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
#                             cursor: pointer;'>
#                     <div style='font-size: 5rem; margin-bottom: 1.5rem;'>🏛️</div>
#                     <h3 style='font-size: 1.75rem; font-weight: 800; color: #2C3E50; margin-bottom: 1rem;'>
#                         Authority Portal
#                     </h3>
#                     <p style='font-size: 1.05rem; color: #2C3E50; margin-bottom: 2rem; line-height: 1.6;'>
#                         Monitor population health metrics, analyze environmental trends,
#                         and manage health authority operations.
#                     </p>
#                     <div style='background: #FEF3C7; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
#                         <p style='font-size: 0.95rem; color: #92400E; margin: 0; font-weight: 600;'>
#                             ✓ Multi-city monitoring<br>
#                             ✓ Advanced analytics<br>
#                             ✓ Export & reporting tools
#                         </p>
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             if st.button(
#                 "🔐 Access Authority Portal", use_container_width=True, type="primary"
#             ):
#                 st.session_state[ROLE_SELECTED_KEY] = True
#                 st.session_state[SELECTED_ROLE_KEY] = "admin"
#                 st.rerun()

#     # Footer info
#     st.markdown("<br><br>", unsafe_allow_html=True)
#     st.markdown(
#         """
#         <div style='text-align: center; padding: 2rem; background: white;
#                     border-radius: 12px; border: 1px solid #E5E7EB;'>
#             <h4 style='color: #2C3E50; font-size: 1.25rem; margin-bottom: 1rem; font-weight: 700;'>
#                 🌟 Platform Features
#             </h4>
#             <div style='display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap;'>
#                 <div style='text-align: center;'>
#                     <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🤖</div>
#                     <p style='color: #2C3E50; margin: 0; font-weight: 600;'>AI-Powered<br>Analysis</p>
#                 </div>
#                 <div style='text-align: center;'>
#                     <div style='font-size: 2rem; margin-bottom: 0.5rem;'>⚡</div>
#                     <p style='color: #2C3E50; margin: 0; font-weight: 600;'>Real-Time<br>Monitoring</p>
#                 </div>
#                 <div style='text-align: center;'>
#                     <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎯</div>
#                     <p style='color: #2C3E50; margin: 0; font-weight: 600;'>Personalized<br>Insights</p>
#                 </div>
#                 <div style='text-align: center;'>
#                     <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🔒</div>
#                     <p style='color: #2C3E50; margin: 0; font-weight: 600;'>Secure &<br>Private</p>
#                 </div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# def admin_login_section() -> bool:
#     """Modern admin login."""

#     if st.session_state.get(AUTH_STATUS_KEY) is True:
#         return True

#     st.markdown("<br><br>", unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 1.2, 1])

#     with col2:
#         st.markdown(
#             """
#             <div style='background: white; padding: 3rem 2.5rem; border-radius: 16px;
#                         box-shadow: 0 10px 40px rgba(0,0,0,0.1); border: 2px solid #E5E7EB;'>
#                 <div style='text-align: center; margin-bottom: 2rem;'>
#                     <div style='font-size: 4rem; margin-bottom: 1rem;'>🔐</div>
#                     <h2 style='color: #2C3E50; margin: 0; font-size: 2rem; font-weight: 800;'>
#                         Health Authority Access
#                     </h2>
#                     <p style='color: #2C3E50; margin-top: 0.75rem; font-size: 1.05rem;'>
#                         Secure authentication required
#                     </p>
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         with st.form("admin_login_form"):
#             pw = st.text_input(
#                 "Administrator Password",
#                 type="password",
#                 placeholder="Enter your secure password",
#             )
#             st.markdown("<br>", unsafe_allow_html=True)

#             col_submit1, col_submit2 = st.columns([1, 1])

#             with col_submit1:
#                 submitted = st.form_submit_button(
#                     "🔓 Access Dashboard", use_container_width=True
#                 )

#             with col_submit2:
#                 back_btn = st.form_submit_button("← Back", use_container_width=True)

#             if back_btn:
#                 st.session_state[ROLE_SELECTED_KEY] = False
#                 st.session_state[SELECTED_ROLE_KEY] = None
#                 st.rerun()

#             if submitted:
#                 if pw == ADMIN_PASSWORD:
#                     st.session_state[AUTH_STATUS_KEY] = True
#                     st.success("✅ Authentication successful!")
#                     time.sleep(0.8)
#                     st.rerun()
#                 else:
#                     st.error("❌ Invalid credentials")
#                     st.session_state[AUTH_STATUS_KEY] = False

#     return False


# def main() -> None:
#     st.set_page_config(
#         page_title="EnviroSense 360 - Health Risk Monitoring",
#         page_icon="🌍",
#         layout="wide",
#         initial_sidebar_state="collapsed",
#     )
#     _inject_base_css()

#     # Initialize session state
#     if ROLE_SELECTED_KEY not in st.session_state:
#         st.session_state[ROLE_SELECTED_KEY] = False
#     if SELECTED_ROLE_KEY not in st.session_state:
#         st.session_state[SELECTED_ROLE_KEY] = None

#     # Show welcome screen if no role selected
#     if not st.session_state.get(ROLE_SELECTED_KEY):
#         render_welcome_screen()
#         return

#     # Configure sidebar for selected role
#     st.set_page_config(
#         page_title="EnviroSense 360",
#         page_icon="🌍",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

#     # Sidebar navigation
#     with st.sidebar:
#         st.markdown("### 🌍 EnviroSense 360")
#         st.markdown("---")

#         current_role = st.session_state.get(SELECTED_ROLE_KEY)

#         role = st.radio(
#             "Dashboard View:",
#             ["👤 Citizen Portal", "🏛️ Health Authority"],
#             index=0 if current_role == "citizen" else 1,
#         )

#         st.markdown("---")
#         st.markdown("### 📊 System Status")
#         st.success("🌍 **5** cities monitored")
#         st.info("✅ System operational")
#         st.success("🔄 Real-time sync")

#         st.markdown("---")

#         if st.button("← Back to Home", use_container_width=True):
#             st.session_state[ROLE_SELECTED_KEY] = False
#             st.session_state[SELECTED_ROLE_KEY] = None
#             st.session_state[AUTH_STATUS_KEY] = False
#             st.rerun()

#     # Render selected dashboard
#     if role.startswith("👤"):
#         render_citizen_dashboard()
#     elif role.startswith("🏛️"):
#         if admin_login_section():
#             render_admin_dashboard()


# if __name__ == "__main__":
#     main()
# import os
# import time
# import streamlit as st

# from src.dashboard.admin_dashboard import render_admin_dashboard
# from src.dashboard.citizen_dashboard import render_citizen_dashboard

# ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
# AUTH_STATUS_KEY = "auth_status"
# ROLE_SELECTED_KEY = "role_selected"
# SELECTED_ROLE_KEY = "selected_role"


# def _inject_base_css() -> None:
#     """Modern professional CSS with enhanced design."""
#     st.markdown(
#         """
#         <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

#         * {
#             font-family: 'Inter', sans-serif;
#         }

#         :root {
#             --primary: #0066FF;
#             --primary-dark: #0052CC;
#             --secondary: #10B981;
#             --danger: #EF4444;
#             --warning: #F59E0B;
#             --bg-main: #F9FAFB;
#             --bg-card: #FFFFFF;
#             --text-primary: #1E293B;
#             --text-secondary: #475569;
#             --border: #E5E7EB;
#             --shadow: 0 4px 12px rgba(0,0,0,0.08);
#         }

#         .stApp {
#             background: linear-gradient(135deg, #F0F9FF 0%, #F9FAFB 100%);
#         }

#         .block-container {
#             padding: 2rem 3rem;
#             max-width: 1400px;
#         }

#         /* Modern Sidebar */
#         section[data-testid="stSidebar"] {
#             background: linear-gradient(180deg, #1E3A8A 0%, #1E293B 100%);
#             border-right: 1px solid rgba(255,255,255,0.1);
#         }

#         section[data-testid="stSidebar"] * {
#             color: #2C3E50 !important;
#         }

#         section[data-testid="stSidebar"] h3 {
#             font-size: 1.1rem !important;
#             font-weight: 700 !important;
#             text-transform: uppercase;
#             letter-spacing: 1px;
#             border-bottom: 2px solid rgba(255,255,255,0.2);
#             padding-bottom: 0.75rem;
#             margin: 1.5rem 0 1rem 0;
#         }

#         section[data-testid="stSidebar"] .stRadio > div > label {
#             background: rgba(255,255,255,0.08);
#             padding: 0.75rem 1rem;
#             border-radius: 8px;
#             margin-bottom: 0.5rem;
#             transition: all 0.3s;
#             border: 1px solid transparent;
#         }

#         section[data-testid="stSidebar"] .stRadio > div > label:hover {
#             background: rgba(255,255,255,0.12);
#             border-color: rgba(255,255,255,0.2);
#         }

#         section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
#             background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
#             border-color: #0066FF;
#             box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
#         }

#         /* Typography */
#         h1 {
#             font-size: 3rem !important;
#             font-weight: 900 !important;
#             color: #2C3E50 !important;
#             margin-bottom: 0.5rem !important;
#             letter-spacing: -0.02em;
#         }

#         h2 {
#             font-size: 2.25rem !important;
#             font-weight: 800 !important;
#             color: #2C3E50 !important;
#         }

#         h3 {
#             font-size: 1.75rem !important;
#             font-weight: 700 !important;
#             color: #2C3E50 !important;
#             margin: 2rem 0 1rem 0 !important;
#         }

#         p, div, span, label {
#             font-size: 1.05rem !important;
#             color: #2C3E50 !important;
#             line-height: 1.6;
#         }

#         label {
#             font-weight: 600 !important;
#             color: #2C3E50 !important;
#         }

#         /* Buttons */
#         .stButton > button {
#             background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
#             color: white !important; /* Changed to white */
#             border: none;
#             border-radius: 10px;
#             padding: 0.9rem 2.5rem;
#             font-size: 1.05rem !important;
#             font-weight: 700;
#             transition: all 0.3s;
#             box-shadow: 0 4px 14px rgba(0, 102, 255, 0.3);
#             letter-spacing: 0.3px;
#         }

#         .stButton > button:hover {
#             transform: translateY(-2px);
#             box-shadow: 0 8px 20px rgba(0, 102, 255, 0.4);
#         }

#         /* Inputs */
#         .stTextInput > div > div > input {
#             font-size: 1rem !important;
#             border: 2px solid var(--border) !important;
#             border-radius: 10px !important;
#             padding: 0.75rem 1rem !important;
#             background: white !important;
#             transition: all 0.3s;
#         }

#         .stTextInput > div > div > input:focus {
#             border-color: var(--primary) !important;
#             box-shadow: 0 0 0 4px rgba(0, 102, 255, 0.1) !important;
#         }

#         /* Alerts */
#         .stSuccess {
#             background: rgba(16, 185, 129, 0.1) !important;
#             border-left: 5px solid var(--secondary) !important;
#             color: #047857 !important;
#             font-size: 1rem !important;
#             padding: 1rem 1.25rem !important;
#         }

#         .stError {
#             background: rgba(239, 68, 68, 0.1) !important;
#             border-left: 5px solid var(--danger) !important;
#             color: #DC2626 !important;
#             font-size: 1rem !important;
#             padding: 1rem 1.25rem !important;
#         }

#         .stInfo {
#             background: rgba(0, 102, 255, 0.1) !important;
#             border-left: 5px solid var(--primary) !important;
#             color: #1E40AF !important;
#             font-size: 1rem !important;
#             padding: 1rem 1.25rem !important;
#         }

#         /* Metrics */
#         [data-testid="stMetric"] {
#             background: white;
#             padding: 1.5rem;
#             border-radius: 12px;
#             border: 1px solid var(--border);
#             box-shadow: var(--shadow);
#             transition: all 0.3s;
#         }

#         [data-testid="stMetric"]:hover {
#             box-shadow: 0 6px 20px rgba(0,0,0,0.12);
#             transform: translateY(-3px);
#         }

#         [data-testid="stMetricValue"] {
#             font-size: 2.25rem !important;
#             font-weight: 800 !important;
#             color: var(--primary) !important;
#         }

#         hr {
#             margin: 2.5rem 0;
#             border: none;
#             height: 1px;
#             background: linear-gradient(90deg, transparent, var(--border), transparent);
#         }

#         /* Card hover effects */
#         .role-card {
#             transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
#         }

#         .role-card:hover {
#             transform: translateY(-8px);
#             box-shadow: 0 20px 40px rgba(0, 102, 255, 0.2);
#         }

#         /* Centered welcome message container */
#         .centered-welcome {
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             min-height: 150px; /* Adjust as needed */
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# def render_welcome_screen() -> None:
#     """Modern welcome screen with role selection."""

#     # Hero Header
#     st.markdown(
#         """
#         <div style='text-align: center; padding: 3rem 2rem 2rem 2rem;'>
#             <div style='display: inline-block; background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
#                          padding: 1.5rem; border-radius: 20px; margin-bottom: 1.5rem;
#                          box-shadow: 0 8px 24px rgba(0, 102, 255, 0.3);'>
#                 <div style='font-size: 4.5rem;'>🌍</div>
#             </div>
#             <h1 style='font-size: 3.5rem; font-weight: 900; color: #2C3E50;
#                         margin: 1rem 0 0.5rem 0; letter-spacing: -0.02em;'>
#                 EnviroSense 360
#             </h1>
#             <p style='font-size: 1.3rem; color: #2C3E50; font-weight: 500; max-width: 800px;
#                      margin: 0 auto 1rem auto; line-height: 1.6;'>
#                 Advanced Environmental Health Risk Monitoring & Assessment Platform
#             </p>
#             <p style='font-size: 1.05rem; color: #9CA3AF; max-width: 700px; margin: 0 auto;'>
#                 Real-time monitoring • AI-powered insights • Personalized health recommendations
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown("<br>", unsafe_allow_html=True)

#     # Role selection
#     st.markdown(
#         """
#         <div style='text-align: center; margin-bottom: 2rem;'>
#             <h2 style='font-size: 2rem; font-weight: 800; color: #2C3E50; margin-bottom: 0.5rem;'>
#                 Choose Your Dashboard
#             </h2>
#             <p style='font-size: 1.1rem; color: #2C3E50;'>
#                 Select the portal that matches your role
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     col1, col2, col3 = st.columns([1, 4, 1])

#     with col2:
#         card_col1, card_col2 = st.columns(2, gap="large")

#         with card_col1:
#             st.markdown(
#                 """
#                 <div class='role-card' style='background: white; padding: 3rem 2rem;
#                                  border-radius: 16px; text-align: center;
#                                  border: 2px solid #E5E7EB; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
#                                  cursor: pointer;'>
#                     <div style='font-size: 5rem; margin-bottom: 1.5rem;'>👤</div>
#                     <h3 style='font-size: 1.75rem; font-weight: 800; color: #2C3E50; margin-bottom: 1rem;'>
#                         Citizen Portal
#                     </h3>
#                     <p style='font-size: 1.05rem; color: #2C3E50; margin-bottom: 2rem; line-height: 1.6;'>
#                         Track your personal health metrics, receive AI-powered risk assessments,
#                         and get personalized health recommendations.
#                     </p>
#                     <div style='background: #F0F9FF; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
#                         <p style='font-size: 0.95rem; color: #0369A1; margin: 0; font-weight: 600;'>
#                             ✓ Personal health tracking<br>
#                             ✓ Real-time risk assessment<br>
#                             ✓ Downloadable reports
#                         </p>
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             if st.button(
#                 "🚀 Access Citizen Portal", use_container_width=True, type="primary"
#             ):
#                 st.session_state[ROLE_SELECTED_KEY] = True
#                 st.session_state[SELECTED_ROLE_KEY] = "citizen"
#                 st.rerun()

#         with card_col2:
#             st.markdown(
#                 """
#                 <div class='role-card' style='background: white; padding: 3rem 2rem;
#                                  border-radius: 16px; text-align: center;
#                                  border: 2px solid #E5E7EB; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
#                                  cursor: pointer;'>
#                     <div style='font-size: 5rem; margin-bottom: 1.5rem;'>🏛️</div>
#                     <h3 style='font-size: 1.75rem; font-weight: 800; color: #2C3E50; margin-bottom: 1rem;'>
#                         Authority Portal
#                     </h3>
#                     <p style='font-size: 1.05rem; color: #2C3E50; margin-bottom: 2rem; line-height: 1.6;'>
#                         Monitor population health metrics, analyze environmental trends,
#                         and manage health authority operations.
#                     </p>
#                     <div style='background: #FEF3C7; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
#                         <p style='font-size: 0.95rem; color: #92400E; margin: 0; font-weight: 600;'>
#                             ✓ Multi-city monitoring<br>
#                             ✓ Advanced analytics<br>
#                             ✓ Export & reporting tools
#                         </p>
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             if st.button(
#                 "🔐 Access Authority Portal", use_container_width=True, type="primary"
#             ):
#                 st.session_state[ROLE_SELECTED_KEY] = True
#                 st.session_state[SELECTED_ROLE_KEY] = "admin"
#                 st.rerun()

#     # Welcome message (moved after role selection for better visual flow on a single page)
#     st.markdown("<br><br>", unsafe_allow_html=True)
#     st.markdown(
#         """
#         <div class='centered-welcome'>
#             <div style='background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
#                         padding: 2rem; border-radius: 14px; margin: 2rem auto; max-width: 900px;
#                         border: 2px solid #BAE6FD; box-shadow: 0 4px 12px rgba(0, 102, 255, 0.08);'>
#                 <h3 style='color: #075985; font-size: 1.5rem; margin: 0 0 1rem 0; font-weight: 700;'>
#                     👋 Welcome to EnviroSense 360
#                 </h3>
#                 <p style='color: #0C4A6E; font-size: 1.05rem; margin: 0; line-height: 1.7;'>
#                     Your comprehensive solution for environmental health monitoring. Whether you're tracking your
#                     personal health metrics or managing population-wide health data, our AI-powered platform
#                     provides real-time insights and actionable recommendations.
#                 </p>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     # Footer info
#     st.markdown("<br><br>", unsafe_allow_html=True)
#     st.markdown(
#         """
#         <div style='text-align: center; padding: 2rem; background: white;
#                      border-radius: 12px; border: 1px solid #E5E7EB;'>
#             <h4 style='color: #2C3E50; font-size: 1.25rem; margin-bottom: 1rem; font-weight: 700;'>
#                 🌟 Platform Features
#             </h4>
#             <div style='display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap;'>
#                 <div style='text-align: center;'>
#                     <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🤖</div>
#                     <p style='color: #2C3E50; margin: 0; font-weight: 600;'>AI-Powered<br>Analysis</p>
#                 </div>
#                 <div style='text-align: center;'>
#                     <div style='font-size: 2rem; margin-bottom: 0.5rem;'>⚡</div>
#                     <p style='color: #2C3E50; margin: 0; font-weight: 600;'>Real-Time<br>Monitoring</p>
#                 </div>
#                 <div style='text-align: center;'>
#                     <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎯</div>
#                     <p style='color: #2C3E50; margin: 0; font-weight: 600;'>Personalized<br>Insights</p>
#                 </div>
#                 <div style='text-align: center;'>
#                     <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🔒</div>
#                     <p style='color: #2C3E50; margin: 0; font-weight: 600;'>Secure &<br>Private</p>
#                 </div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# def admin_login_section() -> bool:
#     """Modern admin login."""

#     if st.session_state.get(AUTH_STATUS_KEY) is True:
#         return True

#     st.markdown("<br><br>", unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 1.2, 1])

#     with col2:
#         st.markdown(
#             """
#             <div style='background: white; padding: 3rem 2.5rem; border-radius: 16px;
#                          box-shadow: 0 10px 40px rgba(0,0,0,0.1); border: 2px solid #E5E7EB;'>
#                 <div style='text-align: center; margin-bottom: 2rem;'>
#                     <div style='font-size: 4rem; margin-bottom: 1rem;'>🔐</div>
#                     <h2 style='color: #2C3E50; margin: 0; font-size: 2rem; font-weight: 800;'>
#                         Health Authority Access
#                     </h2>
#                     <p style='color: #2C3E50; margin-top: 0.75rem; font-size: 1.05rem;'>
#                         Secure authentication required
#                     </p>
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         with st.form("admin_login_form"):
#             pw = st.text_input(
#                 "Administrator Password",
#                 type="password",
#                 placeholder="Enter your secure password",
#             )
#             st.markdown("<br>", unsafe_allow_html=True)

#             col_submit1, col_submit2 = st.columns([1, 1])

#             with col_submit1:
#                 submitted = st.form_submit_button(
#                     "🔓 Access Dashboard", use_container_width=True
#                 )

#             with col_submit2:
#                 back_btn = st.form_submit_button("← Back", use_container_width=True)

#             if back_btn:
#                 st.session_state[ROLE_SELECTED_KEY] = False
#                 st.session_state[SELECTED_ROLE_KEY] = None
#                 st.rerun()

#             if submitted:
#                 if pw == ADMIN_PASSWORD:
#                     st.session_state[AUTH_STATUS_KEY] = True
#                     st.success("✅ Authentication successful!")
#                     time.sleep(0.8)
#                     st.rerun()
#                 else:
#                     st.error("❌ Invalid credentials")
#                     st.session_state[AUTH_STATUS_KEY] = False

#     return False


# def main() -> None:
#     st.set_page_config(
#         page_title="EnviroSense 360 - Health Risk Monitoring",
#         page_icon="🌍",
#         layout="wide",
#         initial_sidebar_state="collapsed",
#     )
#     _inject_base_css()

#     # Initialize session state
#     if ROLE_SELECTED_KEY not in st.session_state:
#         st.session_state[ROLE_SELECTED_KEY] = False
#     if SELECTED_ROLE_KEY not in st.session_state:
#         st.session_state[SELECTED_ROLE_KEY] = None

#     # Show welcome screen if no role selected
#     if not st.session_state.get(ROLE_SELECTED_KEY):
#         render_welcome_screen()
#         return

#     # Configure sidebar for selected role
#     st.set_page_config(
#         page_title="EnviroSense 360",
#         page_icon="🌍",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

#     # Sidebar navigation
#     with st.sidebar:
#         st.markdown("### 🌍 EnviroSense 360")
#         st.markdown("---")

#         current_role = st.session_state.get(SELECTED_ROLE_KEY)

#         role = st.radio(
#             "Dashboard View:",
#             ["👤 Citizen Portal", "🏛️ Health Authority"],
#             index=0 if current_role == "citizen" else 1,
#         )

#         st.markdown("---")
#         st.markdown("### 📊 System Status")
#         st.success("🌍 **5** cities monitored")
#         st.info("✅ System operational")
#         st.success("🔄 Real-time sync")

#         st.markdown("---")

#         if st.button("← Back to Home", use_container_width=True):
#             st.session_state[ROLE_SELECTED_KEY] = False
#             st.session_state[SELECTED_ROLE_KEY] = None
#             st.session_state[AUTH_STATUS_KEY] = False
#             st.rerun()

#     # Render selected dashboard
#     if role.startswith("👤"):
#         render_citizen_dashboard()
#     elif role.startswith("🏛️"):
#         if admin_login_section():
#             render_admin_dashboard()


# if __name__ == "__main__":
#     main()
import os
import time
import streamlit as st

from src.dashboard.admin_dashboard import render_admin_dashboard
from src.dashboard.citizen_dashboard import render_citizen_dashboard

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
AUTH_STATUS_KEY = "auth_status"
ROLE_SELECTED_KEY = "role_selected"
SELECTED_ROLE_KEY = "selected_role"


def _inject_base_css() -> None:
    """Modern professional CSS with enhanced design."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        :root {
            --primary: #0066FF;
            --primary-dark: #0052CC;
            --secondary: #10B981;
            --danger: #EF4444;
            --warning: #F59E0B;
            --bg-main: #F9FAFB;
            --bg-card: #FFFFFF;
            --text-primary: #1F2937;
            --text-secondary: #6B7280;
            --border: #E5E7EB;
            --shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        .stApp {
            background: linear-gradient(135deg, #F0F9FF 0%, #F9FAFB 100%);
        }
        
        .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
        }
        
        /* Modern Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E3A8A 0%, #1E293B 100%);
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        
        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
        
        section[data-testid="stSidebar"] h3 {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 2px solid rgba(255,255,255,0.2);
            padding-bottom: 0.75rem;
            margin: 1.5rem 0 1rem 0;
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label {
            background: rgba(255,255,255,0.08);
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            transition: all 0.3s;
            border: 1px solid transparent;
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label:hover {
            background: rgba(255,255,255,0.12);
            border-color: rgba(255,255,255,0.2);
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
            background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
            border-color: #0066FF;
            box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
        }
        
        /* Typography */
        h1 {
            font-size: 3rem !important;
            font-weight: 900 !important;
            color: var(--text-primary) !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: -0.02em;
        }
        
        h2 {
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            color: var(--text-primary) !important;
        }
        
        h3 {
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            margin: 2rem 0 1rem 0 !important;
        }
        
        p, div, span, label {
            font-size: 1.05rem !important;
            color: var(--text-secondary) !important;
            line-height: 1.6;
        }
        
        label {
            font-weight: 600 !important;
            color: var(--text-primary) !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: #FFFFFF !important;
            border: none;
            border-radius: 10px;
            padding: 0.9rem 2.5rem;
            font-size: 1.05rem !important;
            font-weight: 700;
            transition: all 0.3s;
            box-shadow: 0 4px 14px rgba(0, 102, 255, 0.3);
            letter-spacing: 0.3px;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 102, 255, 0.4);
        }
        
        .stButton > button span {
            color: #FFFFFF !important;
        }
        
        /* Inputs */
        .stTextInput > div > div > input {
            font-size: 1rem !important;
            border: 2px solid var(--border) !important;
            border-radius: 10px !important;
            padding: 0.75rem 1rem !important;
            background: white !important;
            transition: all 0.3s;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 4px rgba(0, 102, 255, 0.1) !important;
        }
        
        /* Alerts */
        .stSuccess {
            background: rgba(16, 185, 129, 0.1) !important;
            border-left: 5px solid var(--secondary) !important;
            color: #047857 !important;
            font-size: 1rem !important;
            padding: 1rem 1.25rem !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1) !important;
            border-left: 5px solid var(--danger) !important;
            color: #DC2626 !important;
            font-size: 1rem !important;
            padding: 1rem 1.25rem !important;
        }
        
        .stInfo {
            background: rgba(0, 102, 255, 0.1) !important;
            border-left: 5px solid var(--primary) !important;
            color: #1E40AF !important;
            font-size: 1rem !important;
            padding: 1rem 1.25rem !important;
        }
        
        /* Metrics */
        [data-testid="stMetric"] {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            transition: all 0.3s;
        }
        
        [data-testid="stMetric"]:hover {
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
            transform: translateY(-3px);
        }
        
        [data-testid="stMetricValue"] {
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            color: var(--primary) !important;
        }
        
        hr {
            margin: 2.5rem 0;
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border), transparent);
        }
        
        /* Card hover effects */
        .role-card {
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .role-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 102, 255, 0.05) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.4s;
        }
        
        .role-card:hover::before {
            opacity: 1;
        }
        
        .role-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 102, 255, 0.2);
            border-color: #0066FF !important;
        }

        /* Centered welcome message container */
        .centered-welcome {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 150px;
        }
        
        /* Animations */
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-float {
            animation: float 3s ease-in-out infinite;
        }
        
        .animate-slide-in {
            animation: slideInUp 0.6s ease-out;
        }
        
        /* Feature cards animation */
        .feature-item {
            transition: all 0.3s;
        }
        
        .feature-item:hover {
            transform: scale(1.1);
        }
        
        /* Gradient text */
        .gradient-text {
            background: linear-gradient(135deg, #0066FF 0%, #0052CC 50%, #10B981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Glassmorphism effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_welcome_screen() -> None:
    """Modern welcome screen with role selection."""

    # Hero Header
    st.markdown(
        """
        <div class='animate-slide-in' style='text-align: center; padding: 3rem 2rem 2rem 2rem;'>
            <div class='animate-float' style='display: inline-block; background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
                         padding: 1.5rem; border-radius: 20px; margin-bottom: 1.5rem;
                         box-shadow: 0 8px 24px rgba(0, 102, 255, 0.3);'>
                <div style='font-size: 4.5rem;'>🌍</div>
            </div>
            <h1 class='gradient-text' style='font-size: 3.5rem; font-weight: 900; 
                        margin: 1rem 0 0.5rem 0; letter-spacing: -0.02em;'>
                EnviroSense 360
            </h1>
            <p style='font-size: 1.3rem; color: #6B7280; font-weight: 500; max-width: 800px; 
                     margin: 0 auto 1rem auto; line-height: 1.6;'>
                Advanced Environmental Health Risk Monitoring & Assessment Platform
            </p>
            <p style='font-size: 1.05rem; color: #9CA3AF; max-width: 700px; margin: 0 auto;'>
                <span style='display: inline-block; padding: 0.5rem 1rem; background: rgba(0, 102, 255, 0.1); 
                             border-radius: 20px; margin: 0 0.5rem;'>Real-time monitoring</span>
                <span style='display: inline-block; padding: 0.5rem 1rem; background: rgba(16, 185, 129, 0.1); 
                             border-radius: 20px; margin: 0 0.5rem;'>AI-powered insights</span>
                <span style='display: inline-block; padding: 0.5rem 1rem; background: rgba(245, 158, 11, 0.1); 
                             border-radius: 20px; margin: 0 0.5rem;'>Personalized health</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Role selection
    st.markdown(
        """
        <div class='animate-slide-in' style='text-align: center; margin-bottom: 2rem;'>
            <h2 style='font-size: 2rem; font-weight: 800; color: #1F2937; margin-bottom: 0.5rem;'>
                Choose Your Dashboard
            </h2>
            <p style='font-size: 1.1rem; color: #6B7280;'>
                Select the portal that matches your role
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([0.5, 5, 0.5])

    with col2:
        card_col1, card_col2 = st.columns(2, gap="large")

        with card_col1:
            st.markdown(
                """
                <div class='role-card glass-card animate-slide-in' style='background: white; padding: 3rem 2rem; 
                                 border-radius: 16px; text-align: center;
                                 border: 2px solid #E5E7EB; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                                 cursor: pointer; height: 100%;'>
                    <div style='font-size: 5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));'>👤</div>
                    <h3 style='font-size: 1.75rem; font-weight: 800; color: #1F2937; margin-bottom: 1rem;'>
                        Citizen Portal
                    </h3>
                    <p style='font-size: 1.05rem; color: #6B7280; margin-bottom: 2rem; line-height: 1.6;'>
                        Track your personal health metrics, receive AI-powered risk assessments, 
                        and get personalized health recommendations.
                    </p>
                    <div style='background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); 
                                 padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;
                                 border: 1px solid #BAE6FD;'>
                        <p style='font-size: 0.95rem; color: #0369A1; margin: 0; font-weight: 600; line-height: 2;'>
                            ✓ Personal health tracking<br>
                            ✓ Real-time risk assessment<br>
                            ✓ Downloadable reports
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "🚀 Access Citizen Portal",
                use_container_width=True,
                type="primary",
                key="citizen_portal_btn",
            ):
                st.session_state[ROLE_SELECTED_KEY] = True
                st.session_state[SELECTED_ROLE_KEY] = "citizen"
                st.rerun()

        with card_col2:
            st.markdown(
                """
                <div class='role-card glass-card animate-slide-in' style='background: white; padding: 3rem 2rem; 
                                 border-radius: 16px; text-align: center;
                                 border: 2px solid #E5E7EB; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                                 cursor: pointer; height: 100%;'>
                    <div style='font-size: 5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));'>🏛️</div>
                    <h3 style='font-size: 1.75rem; font-weight: 800; color: #1F2937; margin-bottom: 1rem;'>
                        Authority Portal
                    </h3>
                    <p style='font-size: 1.05rem; color: #6B7280; margin-bottom: 2rem; line-height: 1.6;'>
                        Monitor population health metrics, analyze environmental trends, 
                        and manage health authority operations.
                    </p>
                    <div style='background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
                                 padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;
                                 border: 1px solid #FCD34D;'>
                        <p style='font-size: 0.95rem; color: #92400E; margin: 0; font-weight: 600; line-height: 2;'>
                            ✓ Multi-city monitoring<br>
                            ✓ Advanced analytics<br>
                            ✓ Export & reporting tools
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "🔐 Access Authority Portal",
                use_container_width=True,
                type="primary",
                key="authority_portal_btn",
            ):
                st.session_state[ROLE_SELECTED_KEY] = True
                st.session_state[SELECTED_ROLE_KEY] = "admin"
                st.rerun()

    # Welcome message (moved after role selection for better visual flow on a single page)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='centered-welcome animate-slide-in'>
            <div class='glass-card' style='background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); 
                        padding: 2.5rem; border-radius: 16px; margin: 2rem auto; max-width: 900px;
                        border: 2px solid #BAE6FD; box-shadow: 0 8px 24px rgba(0, 102, 255, 0.15);'>
                <h3 style='color: #075985; font-size: 1.5rem; margin: 0 0 1rem 0; font-weight: 700;'>
                    👋 Welcome to EnviroSense 360
                </h3>
                <p style='color: #0C4A6E; font-size: 1.05rem; margin: 0; line-height: 1.7;'>
                    Your comprehensive solution for environmental health monitoring. Whether you're tracking your 
                    personal health metrics or managing population-wide health data, our AI-powered platform 
                    provides real-time insights and actionable recommendations to help you make informed decisions.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Footer info
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='glass-card animate-slide-in' style='text-align: center; padding: 2.5rem; background: white; 
                     border-radius: 16px; border: 2px solid #E5E7EB; box-shadow: 0 8px 24px rgba(0,0,0,0.08);'>
            <h4 style='color: #1F2937; font-size: 1.25rem; margin-bottom: 1.5rem; font-weight: 700;'>
                🌟 Platform Features
            </h4>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                        gap: 2rem; max-width: 900px; margin: 0 auto;'>
                <div class='feature-item' style='text-align: center; padding: 1.5rem; 
                            background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
                            border-radius: 12px; border: 1px solid #BAE6FD;'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.75rem;'>🤖</div>
                    <p style='color: #075985; margin: 0; font-weight: 700; font-size: 1rem;'>AI-Powered</p>
                    <p style='color: #0369A1; margin: 0.25rem 0 0 0; font-size: 0.9rem;'>Analysis</p>
                </div>
                <div class='feature-item' style='text-align: center; padding: 1.5rem;
                            background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
                            border-radius: 12px; border: 1px solid #BBF7D0;'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.75rem;'>⚡</div>
                    <p style='color: #065F46; margin: 0; font-weight: 700; font-size: 1rem;'>Real-Time</p>
                    <p style='color: #059669; margin: 0.25rem 0 0 0; font-size: 0.9rem;'>Monitoring</p>
                </div>
                <div class='feature-item' style='text-align: center; padding: 1.5rem;
                            background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                            border-radius: 12px; border: 1px solid #FCD34D;'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.75rem;'>🎯</div>
                    <p style='color: #78350F; margin: 0; font-weight: 700; font-size: 1rem;'>Personalized</p>
                    <p style='color: #92400E; margin: 0.25rem 0 0 0; font-size: 0.9rem;'>Insights</p>
                </div>
                <div class='feature-item' style='text-align: center; padding: 1.5rem;
                            background: linear-gradient(135deg, #FAE8FF 0%, #F3E8FF 100%);
                            border-radius: 12px; border: 1px solid #E9D5FF;'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.75rem;'>🔒</div>
                    <p style='color: #581C87; margin: 0; font-weight: 700; font-size: 1rem;'>Secure &</p>
                    <p style='color: #6B21A8; margin: 0.25rem 0 0 0; font-size: 0.9rem;'>Private</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def admin_login_section() -> bool:
    """Modern admin login."""

    if st.session_state.get(AUTH_STATUS_KEY) is True:
        return True

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown(
            """
            <div class='glass-card animate-slide-in' style='background: white; padding: 3rem 2.5rem; border-radius: 16px; 
                         box-shadow: 0 10px 40px rgba(0,0,0,0.12); border: 2px solid #E5E7EB;'>
                <div style='text-align: center; margin-bottom: 2rem;'>
                    <div class='animate-float' style='font-size: 4rem; margin-bottom: 1rem; 
                                filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));'>🔐</div>
                    <h2 style='color: #1F2937; margin: 0; font-size: 2rem; font-weight: 800;'>
                        Health Authority Access
                    </h2>
                    <p style='color: #6B7280; margin-top: 0.75rem; font-size: 1.05rem;'>
                        Secure authentication required
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("admin_login_form"):
            pw = st.text_input(
                "Administrator Password",
                type="password",
                placeholder="Enter your secure password",
            )
            st.markdown("<br>", unsafe_allow_html=True)

            col_submit1, col_submit2 = st.columns([1, 1])

            with col_submit1:
                submitted = st.form_submit_button(
                    "🔓 Access Dashboard", use_container_width=True
                )

            with col_submit2:
                back_btn = st.form_submit_button("← Back", use_container_width=True)

            if back_btn:
                st.session_state[ROLE_SELECTED_KEY] = False
                st.session_state[SELECTED_ROLE_KEY] = None
                st.rerun()

            if submitted:
                if pw == ADMIN_PASSWORD:
                    st.session_state[AUTH_STATUS_KEY] = True
                    st.success("✅ Authentication successful!")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
                    st.session_state[AUTH_STATUS_KEY] = False

    return False


def main() -> None:
    st.set_page_config(
        page_title="EnviroSense 360 - Health Risk Monitoring",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    _inject_base_css()

    # Initialize session state
    if ROLE_SELECTED_KEY not in st.session_state:
        st.session_state[ROLE_SELECTED_KEY] = False
    if SELECTED_ROLE_KEY not in st.session_state:
        st.session_state[SELECTED_ROLE_KEY] = None

    # Show welcome screen if no role selected
    if not st.session_state.get(ROLE_SELECTED_KEY):
        render_welcome_screen()
        return

    # Configure sidebar for selected role
    st.set_page_config(
        page_title="EnviroSense 360",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🌍 EnviroSense 360")
        st.markdown("---")

        current_role = st.session_state.get(SELECTED_ROLE_KEY)

        role = st.radio(
            "Dashboard View:",
            ["👤 Citizen Portal", "🏛 Health Authority"],
            index=0 if current_role == "citizen" else 1,
        )

        st.markdown("---")
        st.markdown("### 📊 System Status")
        st.success("🌍 *5* cities monitored")
        st.info("✅ System operational")
        st.success("🔄 Real-time sync")

        st.markdown("---")

        if st.button("← Back to Home", use_container_width=True):
            st.session_state[ROLE_SELECTED_KEY] = False
            st.session_state[SELECTED_ROLE_KEY] = None
            st.session_state[AUTH_STATUS_KEY] = False
            st.rerun()

    # Render selected dashboard
    if role.startswith("👤"):
        render_citizen_dashboard()
    elif role.startswith("🏛"):
        if admin_login_section():
            render_admin_dashboard()


if __name__ == "__main__":
    main()
