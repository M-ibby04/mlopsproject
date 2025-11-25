# # # # # src/dashboard/citizen_dashboard.py

# # # # import os
# # # # import time
# # # # from typing import Dict, Optional

# # # # import requests
# # # # import streamlit as st

# # # # # ------------------------------------------------------------------
# # # # # API CONFIG
# # # # # ------------------------------------------------------------------

# # # # DEFAULT_API_BASE_URL = "http://host.docker.internal:8000"
# # # # API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


# # # # def check_api_health(base_url: str) -> bool:
# # # #     """Check the /health endpoint of the prediction API."""
# # # #     try:
# # # #         r = requests.get(f"{base_url}/health", timeout=2)
# # # #         return r.status_code == 200
# # # #     except Exception:
# # # #         return False


# # # # def call_prediction_api(base_url: str, payload: Dict) -> Dict:
# # # #     """Send user data to the /predict endpoint."""
# # # #     r = requests.post(f"{base_url}/predict", json=payload, timeout=5)
# # # #     r.raise_for_status()
# # # #     return r.json()


# # # # def get_health_advice(
# # # #     pred_class: int, pm25: float, no2: float, co: float, hr: int, temp: float
# # # # ) -> Dict:
# # # #     """Generate contextual health advice based on risk level and parameters."""

# # # #     advice = {"general": [], "immediate_actions": [], "long_term": [], "emergency": []}

# # # #     if pred_class == 0:  # Low Risk
# # # #         advice["general"] = [
# # # #             "✅ Your current health indicators are within safe ranges",
# # # #             "🌟 Continue maintaining your healthy lifestyle",
# # # #             "💚 Air quality is acceptable for outdoor activities",
# # # #         ]
# # # #         advice["immediate_actions"] = [
# # # #             "🚶‍♀️ Safe to engage in outdoor exercise",
# # # #             "🪟 Consider opening windows for ventilation",
# # # #             "🌱 Maintain regular physical activity routine",
# # # #         ]
# # # #         advice["long_term"] = [
# # # #             "📊 Regular health check-ups recommended",
# # # #             "🥗 Continue balanced diet and hydration",
# # # #             "😴 Maintain 7-9 hours of quality sleep",
# # # #         ]

# # # #     elif pred_class == 1:  # Moderate Risk
# # # #         advice["general"] = [
# # # #             "⚠️ Some health indicators require attention",
# # # #             "🔍 Monitor your symptoms closely",
# # # #             "⚡ Take preventive measures to avoid worsening",
# # # #         ]
# # # #         advice["immediate_actions"] = [
# # # #             (
# # # #                 "😷 Consider wearing a mask if going outdoors"
# # # #                 if pm25 > 50
# # # #                 else "🚶‍♂️ Limit strenuous outdoor activities"
# # # #             ),
# # # #             "💧 Stay well-hydrated throughout the day",
# # # #             "🏠 Spend more time in clean indoor environments",
# # # #             "📱 Keep emergency contacts readily available",
# # # #         ]

# # # #         if hr > 100:
# # # #             advice["immediate_actions"].append(
# # # #                 "❤️ Your heart rate is elevated - take rest breaks"
# # # #             )
# # # #         if temp > 37.5:
# # # #             advice["immediate_actions"].append(
# # # #                 "🌡️ Elevated temperature detected - monitor closely"
# # # #             )
# # # #         if pm25 > 75:
# # # #             advice["immediate_actions"].append(
# # # #                 "🏭 High pollution - use air purifiers indoors"
# # # #             )

# # # #         advice["long_term"] = [
# # # #             "👨‍⚕️ Schedule a check-up with your doctor soon",
# # # #             "📈 Track your symptoms daily",
# # # #             "🏃‍♀️ Moderate exercise indoors when possible",
# # # #             "🥦 Focus on anti-inflammatory foods",
# # # #         ]

# # # #     else:  # High Risk
# # # #         advice["general"] = [
# # # #             "🚨 **URGENT**: High-risk indicators detected",
# # # #             "⚠️ Immediate attention recommended",
# # # #             "📞 Consider contacting healthcare provider",
# # # #         ]
# # # #         advice["emergency"] = [
# # # #             "🏥 Seek medical attention if symptoms worsen",
# # # #             "📱 Keep emergency number ready: 1122 (Pakistan Emergency)",
# # # #             "👨‍👩‍👧 Inform family members of your condition",
# # # #             "🚫 Avoid all outdoor activities",
# # # #         ]
# # # #         advice["immediate_actions"] = [
# # # #             "🛑 **Stay indoors** in a clean environment",
# # # #             "😷 **Wear N95 mask** if you must go outside",
# # # #             "💊 Take prescribed medications as directed",
# # # #             "💧 Drink plenty of water",
# # # #             "📴 Avoid strenuous activities",
# # # #             "🏠 Use air purifiers or AC with HEPA filters",
# # # #         ]

# # # #         if hr > 120:
# # # #             advice["emergency"].insert(
# # # #                 0, "❤️‍🩹 **CRITICAL**: Very high heart rate - seek immediate help"
# # # #             )
# # # #         if temp > 38.5:
# # # #             advice["emergency"].insert(
# # # #                 0, "🌡️ **CRITICAL**: High fever - medical attention needed"
# # # #             )
# # # #         if pm25 > 150:
# # # #             advice["immediate_actions"].insert(
# # # #                 0, "☠️ **HAZARDOUS** air quality - stay indoors!"
# # # #             )

# # # #         advice["long_term"] = [
# # # #             "🏥 **URGENT**: Schedule immediate doctor appointment",
# # # #             "📋 Document all symptoms with timestamps",
# # # #             "💊 Discuss medication adjustments with doctor",
# # # #             "🔔 Set up health monitoring alerts",
# # # #         ]

# # # #     return advice


# # # # def display_health_metrics_cards(
# # # #     hr: int, temp: float, pm25: float, no2: float, co: float
# # # # ):
# # # #     """Display colorful metric cards for input parameters."""
# # # #     st.markdown("### 📊 Current Health Readings")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     col1, col2, col3, col4, col5 = st.columns(5)

# # # #     with col1:
# # # #         hr_status = "Normal" if 60 <= hr <= 100 else "Attention Needed"
# # # #         hr_delta = "🟢 Healthy" if 60 <= hr <= 100 else "🔴 Alert"
# # # #         st.metric(
# # # #             label="💓 Heart Rate",
# # # #             value=f"{hr} BPM",
# # # #             delta=hr_delta,
# # # #             delta_color="normal" if 60 <= hr <= 100 else "inverse",
# # # #         )

# # # #     with col2:
# # # #         temp_status = "Normal" if 36.0 <= temp <= 37.5 else "Abnormal"
# # # #         temp_delta = "🟢 Normal" if 36.0 <= temp <= 37.5 else "🔴 Check"
# # # #         st.metric(
# # # #             label="🌡️ Temperature",
# # # #             value=f"{temp:.1f}°C",
# # # #             delta=temp_delta,
# # # #             delta_color="normal" if 36.0 <= temp <= 37.5 else "inverse",
# # # #         )

# # # #     with col3:
# # # #         pm25_status = "Good" if pm25 < 35 else "Moderate" if pm25 < 75 else "Poor"
# # # #         pm25_delta = (
# # # #             f"🟢 {pm25_status}"
# # # #             if pm25 < 35
# # # #             else f"🟡 {pm25_status}" if pm25 < 75 else f"🔴 {pm25_status}"
# # # #         )
# # # #         st.metric(
# # # #             label="🌫️ PM2.5",
# # # #             value=f"{pm25:.1f} µg/m³",
# # # #             delta=pm25_delta,
# # # #             delta_color="normal" if pm25 < 50 else "inverse",
# # # #         )

# # # #     with col4:
# # # #         no2_status = "Good" if no2 < 50 else "High"
# # # #         no2_delta = f"🟢 {no2_status}" if no2 < 50 else f"🔴 {no2_status}"
# # # #         st.metric(
# # # #             label="💨 NO₂",
# # # #             value=f"{no2:.1f} ppb",
# # # #             delta=no2_delta,
# # # #             delta_color="normal" if no2 < 50 else "inverse",
# # # #         )

# # # #     with col5:
# # # #         co_status = "Safe" if co < 2 else "Unsafe"
# # # #         co_delta = f"🟢 {co_status}" if co < 2 else f"🔴 {co_status}"
# # # #         st.metric(
# # # #             label="⚠️ CO",
# # # #             value=f"{co:.1f} ppm",
# # # #             delta=co_delta,
# # # #             delta_color="normal" if co < 2 else "inverse",
# # # #         )


# # # # # ------------------------------------------------------------------
# # # # # MAIN RENDER FUNCTION
# # # # # ------------------------------------------------------------------
# # # # def render_citizen_dashboard() -> None:
# # # #     st.cache_data.clear()

# # # #     # Hero section with medical theme
# # # #     st.markdown(
# # # #         """
# # # #         <div style='background: linear-gradient(135deg, #4A90E2 0%, #2C5F8D 100%);
# # # #                     padding: 3rem 2rem; border-radius: 20px; margin-bottom: 2.5rem;
# # # #                     box-shadow: 0 10px 40px rgba(44, 95, 141, 0.25);'>
# # # #             <div style='display: flex; align-items: center; justify-content: center; gap: 2rem;'>
# # # #                 <div style='font-size: 5rem;'>🩺</div>
# # # #                 <div>
# # # #                     <h2 style='color: white; margin: 0; font-size: 2.6rem; font-weight: 800;'>
# # # #                         Personalized Health Risk Assessment
# # # #                     </h2>
# # # #                     <p style='color: rgba(255,255,255,0.95); margin-top: 0.8rem; font-size: 1.3rem; font-weight: 400;'>
# # # #                         AI-powered analysis of your vital signs and environmental exposure
# # # #                     </p>
# # # #                 </div>
# # # #             </div>
# # # #         </div>
# # # #         """,
# # # #         unsafe_allow_html=True,
# # # #     )

# # # #     # ========== USER PROFILE CARD ==========
# # # #     st.markdown("### 👤 Patient Information")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     with st.container():
# # # #         c1, c2, c3, c4 = st.columns([2, 1, 1, 1])

# # # #         with c1:
# # # #             name: str = st.text_input(
# # # #                 "👨‍💼 Full Name",
# # # #                 value="",
# # # #                 placeholder="Enter your full name",
# # # #                 help="Your name for record purposes",
# # # #             )
# # # #         with c2:
# # # #             age: Optional[int] = st.number_input(
# # # #                 "🎂 Age (years)",
# # # #                 min_value=1,
# # # #                 max_value=110,
# # # #                 value=30,
# # # #                 help="Your current age",
# # # #             )
# # # #         with c3:
# # # #             gender: str = st.selectbox(
# # # #                 "⚧️ Gender",
# # # #                 ["Prefer not to say", "Female", "Male", "Other"],
# # # #                 index=0,
# # # #                 help="Select your gender",
# # # #             )
# # # #         with c4:
# # # #             location = st.selectbox(
# # # #                 "📍 Location",
# # # #                 ["Lahore", "Karachi", "Islamabad", "Peshawar", "Quetta", "Other"],
# # # #                 index=0,
# # # #                 help="Your current city",
# # # #             )

# # # #     st.markdown("---")

# # # #     # ========== INPUT METHOD SELECTOR ==========
# # # #     st.markdown("### 🎛️ Health Data Input")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     input_mode = st.radio(
# # # #         "Choose your preferred input method:",
# # # #         ["🎚️ Interactive Sliders (Recommended)", "⌨️ Manual Number Entry"],
# # # #         horizontal=True,
# # # #         help="Sliders provide visual feedback and safe ranges",
# # # #     )

# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     # ========== INPUT SECTIONS ==========
# # # #     with st.container():
# # # #         left, right = st.columns(2, gap="large")

# # # #         with left:
# # # #             # Physiological data card
# # # #             st.markdown(
# # # #                 """
# # # #                 <div style='background: linear-gradient(135deg, rgba(255, 107, 107, 0.12) 0%, rgba(255, 107, 107, 0.05) 100%);
# # # #                             padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem;
# # # #                             border-left: 5px solid #FF6B6B;'>
# # # #                     <h4 style='color: #2C3E50; margin: 0; font-size: 1.6rem; font-weight: 700;'>
# # # #                         💓 Vital Signs Monitoring
# # # #                     </h4>
# # # #                     <p style='color: #546E7A; margin: 0.8rem 0 0 0; font-size: 1.15rem;'>
# # # #                         Input your current physiological parameters
# # # #                     </p>
# # # #                 </div>
# # # #                 """,
# # # #                 unsafe_allow_html=True,
# # # #             )

# # # #             if input_mode.startswith("🎚️"):
# # # #                 hr = st.slider(
# # # #                     "💓 Heart Rate (BPM)",
# # # #                     min_value=50,
# # # #                     max_value=150,
# # # #                     value=75,
# # # #                     help="Normal resting heart rate: 60-100 BPM. Athletes may have lower rates.",
# # # #                 )
# # # #                 st.caption(
# # # #                     "📌 **Reference**: Resting 60-100 BPM | Exercise 100-150 BPM"
# # # #                 )

# # # #                 st.markdown("<br>", unsafe_allow_html=True)

# # # #                 temp = st.slider(
# # # #                     "🌡️ Body Temperature (°C)",
# # # #                     min_value=35.0,
# # # #                     max_value=42.0,
# # # #                     value=36.6,
# # # #                     step=0.1,
# # # #                     help="Normal body temperature: 36.1-37.2°C. Fever starts above 37.5°C.",
# # # #                 )
# # # #                 st.caption(
# # # #                     "📌 **Reference**: Normal 36.1-37.2°C | Fever >37.5°C | High Fever >38.5°C"
# # # #                 )
# # # #             else:
# # # #                 hr = st.number_input(
# # # #                     "💓 Heart Rate (BPM)",
# # # #                     50,
# # # #                     150,
# # # #                     75,
# # # #                     help="Normal resting: 60-100 BPM",
# # # #                 )
# # # #                 temp = st.number_input(
# # # #                     "🌡️ Body Temperature (°C)",
# # # #                     35.0,
# # # #                     42.0,
# # # #                     36.6,
# # # #                     0.1,
# # # #                     help="Normal: 36.1-37.2°C",
# # # #                 )

# # # #         with right:
# # # #             # Environmental data card
# # # #             st.markdown(
# # # #                 """
# # # #                 <div style='background: linear-gradient(135deg, rgba(78, 205, 196, 0.12) 0%, rgba(78, 205, 196, 0.05) 100%);
# # # #                             padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem;
# # # #                             border-left: 5px solid #4ECDC4;'>
# # # #                     <h4 style='color: #2C3E50; margin: 0; font-size: 1.6rem; font-weight: 700;'>
# # # #                         🌍 Environmental Exposure
# # # #                     </h4>
# # # #                     <p style='color: #546E7A; margin: 0.8rem 0 0 0; font-size: 1.15rem;'>
# # # #                         Current air quality and pollution levels
# # # #                     </p>
# # # #                 </div>
# # # #                 """,
# # # #                 unsafe_allow_html=True,
# # # #             )

# # # #             if input_mode.startswith("🎚️"):
# # # #                 pm25 = st.slider(
# # # #                     "🌫️ PM2.5 Particulate Matter (µg/m³)",
# # # #                     min_value=0.0,
# # # #                     max_value=300.0,
# # # #                     value=35.0,
# # # #                     step=1.0,
# # # #                     help="Fine particles that can penetrate deep into lungs. Major health concern.",
# # # #                 )
# # # #                 st.caption(
# # # #                     "📌 **Air Quality**: Good 0-35 | Moderate 35-75 | Unhealthy 75-150 | Hazardous >150"
# # # #                 )

# # # #                 st.markdown("<br>", unsafe_allow_html=True)

# # # #                 no2 = st.slider(
# # # #                     "💨 Nitrogen Dioxide - NO₂ (ppb)",
# # # #                     min_value=0.0,
# # # #                     max_value=200.0,
# # # #                     value=25.0,
# # # #                     step=1.0,
# # # #                     help="Toxic gas from vehicles and industry. Respiratory irritant.",
# # # #                 )
# # # #                 st.caption(
# # # #                     "📌 **Safety Levels**: Good <50 | Moderate 50-100 | Unhealthy >100 ppb"
# # # #                 )

# # # #                 st.markdown("<br>", unsafe_allow_html=True)

# # # #                 co = st.slider(
# # # #                     "⚠️ Carbon Monoxide - CO (ppm)",
# # # #                     min_value=0.0,
# # # #                     max_value=10.0,
# # # #                     value=0.5,
# # # #                     step=0.1,
# # # #                     help="Colorless, odorless toxic gas. Interferes with oxygen delivery.",
# # # #                 )
# # # #                 st.caption(
# # # #                     "📌 **Danger Levels**: Safe <2 | Moderate 2-5 | Dangerous 5-10 | Critical >10 ppm"
# # # #                 )
# # # #             else:
# # # #                 pm25 = st.number_input("🌫️ PM2.5 (µg/m³)", 0.0, 300.0, 35.0, 1.0)
# # # #                 no2 = st.number_input("💨 NO₂ (ppb)", 0.0, 200.0, 25.0, 1.0)
# # # #                 co = st.number_input("⚠️ CO (ppm)", 0.0, 10.0, 0.5, 0.1)

# # # #     # Display metrics summary
# # # #     st.markdown("---")
# # # #     display_health_metrics_cards(hr, temp, pm25, no2, co)

# # # #     payload = {
# # # #         "HeartRate": hr,
# # # #         "Temp": temp,
# # # #         "PM25": pm25,
# # # #         "NO2": no2,
# # # #         "CO_Level": co,
# # # #     }

# # # #     st.markdown("---")

# # # #     # ========== API CHECK ==========
# # # #     api_ok = check_api_health(API_BASE_URL)

# # # #     if not api_ok:
# # # #         st.error(
# # # #             f"🚫 **API Connection Error**: Cannot reach prediction service at `{API_BASE_URL}`"
# # # #         )
# # # #         with st.expander("🔧 Technical Support Information"):
# # # #             st.info("**For System Administrators**: Start the API service")
# # # #             st.code(
# # # #                 "docker run --rm -p 8000:8000 -v ${PWD}:/app -w /app mlops_fl "
# # # #                 "uvicorn src.deployment.api:app --host 0.0.0.0 --port 8000",
# # # #                 language="bash",
# # # #             )
# # # #         return

# # # #     # ========== ANALYSIS BUTTON ==========
# # # #     st.markdown("<br>", unsafe_allow_html=True)
# # # #     col1, col2, col3 = st.columns([1, 2, 1])
# # # #     with col2:
# # # #         calculate_btn = st.button(
# # # #             "🔬 ANALYZE MY HEALTH RISK", use_container_width=True, type="primary"
# # # #         )

# # # #     if calculate_btn:
# # # #         try:
# # # #             with st.spinner("🔄 Analyzing your health data with AI..."):
# # # #                 resp = call_prediction_api(API_BASE_URL, payload)
# # # #                 time.sleep(0.6)

# # # #         except requests.exceptions.HTTPError as e:
# # # #             st.error(f"❌ **API Error**: Server returned HTTP {e.response.status_code}")
# # # #             return
# # # #         except Exception as e:
# # # #             st.error(f"❌ **System Error**: {str(e)}")
# # # #             return

# # # #         pred_class = resp.get("prediction")
# # # #         raw = resp.get("raw_output")

# # # #         # Risk mapping with medical colors
# # # #         RISK_MAP = {
# # # #             0: (
# # # #                 "🟢 LOW RISK",
# # # #                 "Your health indicators are within safe ranges. Continue maintaining good health habits.",
# # # #                 "#52D17C",
# # # #                 "rgba(82, 209, 124, 0.15)",
# # # #             ),
# # # #             1: (
# # # #                 "🟡 MODERATE RISK",
# # # #                 "Some parameters require monitoring. Take precautionary measures.",
# # # #                 "#FF9F68",
# # # #                 "rgba(255, 159, 104, 0.15)",
# # # #             ),
# # # #             2: (
# # # #                 "🔴 HIGH RISK",
# # # #                 "Immediate attention recommended. Consider consulting healthcare provider.",
# # # #                 "#FF6B6B",
# # # #                 "rgba(255, 107, 107, 0.15)",
# # # #             ),
# # # #         }

# # # #         risk_label, risk_desc, risk_color, risk_bg = RISK_MAP.get(
# # # #             pred_class,
# # # #             (
# # # #                 "⚪ UNKNOWN",
# # # #                 "Unable to determine risk level.",
# # # #                 "#A0AEC0",
# # # #                 "rgba(160, 174, 192, 0.15)",
# # # #             ),
# # # #         )

# # # #         # ========== RESULTS DISPLAY ==========
# # # #         st.markdown("---")
# # # #         st.markdown("## 📋 Your Health Risk Analysis Results")
# # # #         st.markdown("<br>", unsafe_allow_html=True)

# # # #         # Main result card with medical styling
# # # #         st.markdown(
# # # #             f"""
# # # #             <div style='background: {risk_bg};
# # # #                         border: 3px solid {risk_color};
# # # #                         border-radius: 18px;
# # # #                         padding: 2.5rem;
# # # #                         margin: 2rem 0;
# # # #                         box-shadow: 0 8px 32px {risk_color}40;'>
# # # #                 <div style='text-align: center;'>
# # # #                     <h2 style='color: {risk_color}; margin: 0; font-size: 3rem; font-weight: 800;'>
# # # #                         {risk_label}
# # # #                     </h2>
# # # #                     <p style='font-size: 1.4rem; margin-top: 1.5rem; color: #2C3E50; font-weight: 500;'>
# # # #                         {risk_desc}
# # # #                     </p>
# # # #                 </div>
# # # #             </div>
# # # #             """,
# # # #             unsafe_allow_html=True,
# # # #         )

# # # #         # Get personalized health advice
# # # #         advice = get_health_advice(pred_class, pm25, no2, co, hr, temp)

# # # #         # Display advice in medical format
# # # #         st.markdown("### 💊 Medical Recommendations & Action Plan")
# # # #         st.markdown("<br>", unsafe_allow_html=True)

# # # #         # Emergency section (if applicable)
# # # #         if advice["emergency"]:
# # # #             st.markdown(
# # # #                 """
# # # #                 <div style='background: rgba(255, 107, 107, 0.1);
# # # #                             border: 3px solid #FF6B6B;
# # # #                             border-radius: 14px;
# # # #                             padding: 2rem;
# # # #                             margin-bottom: 2rem;'>
# # # #                     <h4 style='color: #C13C3C; margin-top: 0; font-size: 1.6rem; font-weight: 700;'>
# # # #                         🚨 EMERGENCY ACTIONS REQUIRED
# # # #                     </h4>
# # # #                 </div>
# # # #                 """,
# # # #                 unsafe_allow_html=True,
# # # #             )
# # # #             for item in advice["emergency"]:
# # # #                 st.error(f"### {item}")
# # # #             st.markdown("<br>", unsafe_allow_html=True)

# # # #         # Tabs for organized advice
# # # #         tab1, tab2, tab3 = st.tabs(
# # # #             ["📌 Current Status", "⚡ Immediate Actions", "📈 Long-term Care"]
# # # #         )

# # # #         with tab1:
# # # #             st.markdown("#### General Health Status")
# # # #             for item in advice["general"]:
# # # #                 st.info(f"**{item}**")

# # # #         with tab2:
# # # #             st.markdown("#### Actions to Take Now")
# # # #             cols = st.columns(2)
# # # #             for idx, item in enumerate(advice["immediate_actions"]):
# # # #                 with cols[idx % 2]:
# # # #                     st.success(f"**{item}**")

# # # #         with tab3:
# # # #             st.markdown("#### Ongoing Health Management")
# # # #             for item in advice["long_term"]:
# # # #                 st.info(f"• {item}")

# # # #         # Medical resources section
# # # #         st.markdown("---")
# # # #         st.markdown("### 📚 Healthcare Resources & Support")
# # # #         st.markdown("<br>", unsafe_allow_html=True)

# # # #         resource_col1, resource_col2, resource_col3 = st.columns(3)

# # # #         with resource_col1:
# # # #             st.markdown(
# # # #                 """
# # # #                 <div style='background: rgba(78, 205, 196, 0.1);
# # # #                             padding: 2rem;
# # # #                             border-radius: 14px;
# # # #                             text-align: center;
# # # #                             border: 2px solid #4ECDC4;'>
# # # #                     <div style='font-size: 3rem; margin-bottom: 1rem;'>🏥</div>
# # # #                     <h4 style='color: #2C5F8D; font-size: 1.4rem;'>Find Healthcare</h4>
# # # #                     <p style='font-size: 1.1rem;'>Locate nearby hospitals and clinics</p>
# # # #                 </div>
# # # #                 """,
# # # #                 unsafe_allow_html=True,
# # # #             )

# # # #         with resource_col2:
# # # #             st.markdown(
# # # #                 """
# # # #                 <div style='background: rgba(255, 107, 107, 0.1);
# # # #                             padding: 2rem;
# # # #                             border-radius: 14px;
# # # #                             text-align: center;
# # # #                             border: 2px solid #FF6B6B;'>
# # # #                     <div style='font-size: 3rem; margin-bottom: 1rem;'>📞</div>
# # # #                     <h4 style='color: #C13C3C; font-size: 1.4rem;'>Emergency: 1122</h4>
# # # #                     <p style='font-size: 1.1rem;'>Pakistan Emergency Services</p>
# # # #                 </div>
# # # #                 """,
# # # #                 unsafe_allow_html=True,
# # # #             )

# # # #         with resource_col3:
# # # #             st.markdown(
# # # #                 """
# # # #                 <div style='background: rgba(74, 144, 226, 0.1);
# # # #                             padding: 2rem;
# # # #                             border-radius: 14px;
# # # #                             text-align: center;
# # # #                             border: 2px solid #4A90E2;'>
# # # #                     <div style='font-size: 3rem; margin-bottom: 1rem;'>📖</div>
# # # #                     <h4 style='color: #2C5F8D; font-size: 1.4rem;'>Health Education</h4>
# # # #                     <p style='font-size: 1.1rem;'>Learn about air quality & health</p>
# # # #                 </div>
# # # #                 """,
# # # #                 unsafe_allow_html=True,
# # # #             )

# # # #         # Technical details
# # # #         st.markdown("---")
# # # #         with st.expander("🔍 Technical Details & Complete Data Record"):
# # # #             st.json(
# # # #                 {
# # # #                     "patient_profile": {
# # # #                         "name": name,
# # # #                         "age": age,
# # # #                         "gender": gender,
# # # #                         "location": location,
# # # #                     },
# # # #                     "input_parameters": payload,
# # # #                     "prediction_class": pred_class,
# # # #                     "risk_assessment": risk_label,
# # # #                     "model_output": raw,
# # # #                     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
# # # #                 }
# # # #             )

# # # #         # Download report
# # # #         st.markdown("<br>", unsafe_allow_html=True)
# # # #         st.download_button(
# # # #             label="📥 Download Complete Health Report (JSON)",
# # # #             data=str(
# # # #                 {
# # # #                     "patient": name,
# # # #                     "age": age,
# # # #                     "location": location,
# # # #                     "risk_assessment": risk_label,
# # # #                     "vital_signs": {"heart_rate": hr, "temperature": temp},
# # # #                     "environmental_exposure": {"pm25": pm25, "no2": no2, "co": co},
# # # #                     "recommendations": advice,
# # # #                     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
# # # #                 }
# # # #             ),
# # # #             file_name=f"health_report_{name.replace(' ', '_')}_{time.strftime('%Y%m%d_%H%M%S')}.json",
# # # #             mime="application/json",
# # # #             use_container_width=True,
# # # #         )
# # # # src/dashboard/citizen_dashboard.py

# # # import os
# # # import time
# # # import json
# # # import smtplib
# # # from email.mime.text import MIMEText
# # # from email.mime.multipart import MIMEMultipart
# # # from typing import Dict, Optional

# # # import requests
# # # import streamlit as st
# # # import plotly.graph_objects as go

# # # DEFAULT_API_BASE_URL = "http://host.docker.internal:8000"
# # # API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


# # # def check_api_health(base_url: str) -> bool:
# # #     try:
# # #         r = requests.get(f"{base_url}/health", timeout=2)
# # #         return r.status_code == 200
# # #     except Exception:
# # #         return False


# # # def call_prediction_api(base_url: str, payload: Dict) -> Dict:
# # #     r = requests.post(f"{base_url}/predict", json=payload, timeout=5)
# # #     r.raise_for_status()
# # #     return r.json()


# # # def send_email_report(to_email: str, report_data: dict) -> bool:
# # #     """Send health report via email (placeholder - configure SMTP settings)."""
# # #     try:
# # #         # Note: Configure these with actual SMTP server details
# # #         # smtp_server = "smtp.gmail.com"
# # #         # smtp_port = 587
# # #         # sender_email = "your-email@example.com"
# # #         # sender_password = "your-app-password"

# # #         # For demo purposes, we'll just simulate success
# # #         # In production, uncomment and configure the SMTP code below

# # #         """
# # #         msg = MIMEMultipart()
# # #         msg['From'] = sender_email
# # #         msg['To'] = to_email
# # #         msg['Subject'] = "Your Health Risk Assessment Report"

# # #         body = f'''
# # #         Health Risk Assessment Report

# # #         Patient: {report_data.get('name')}
# # #         Risk Level: {report_data.get('risk')}
# # #         Date: {report_data.get('timestamp')}

# # #         Full report data:
# # #         {json.dumps(report_data, indent=2)}
# # #         '''

# # #         msg.attach(MIMEText(body, 'plain'))

# # #         server = smtplib.SMTP(smtp_server, smtp_port)
# # #         server.starttls()
# # #         server.login(sender_email, sender_password)
# # #         server.send_message(msg)
# # #         server.quit()
# # #         """

# # #         return True
# # #     except Exception as e:
# # #         st.error(f"Email error: {str(e)}")
# # #         return False


# # # def get_health_advice(
# # #     pred_class: int, pm25: float, no2: float, co: float, hr: int, temp: float
# # # ) -> Dict:
# # #     advice = {"general": [], "immediate": [], "longterm": [], "emergency": []}

# # #     if pred_class == 0:
# # #         advice["general"] = [
# # #             "✅ Your health indicators are within safe ranges",
# # #             "🌟 Continue maintaining your healthy lifestyle",
# # #             "💚 Air quality is acceptable for outdoor activities",
# # #         ]
# # #         advice["immediate"] = [
# # #             "🚶‍♀️ Safe to engage in outdoor exercise",
# # #             "🪟 Consider opening windows for ventilation",
# # #             "🌱 Maintain regular physical activity",
# # #         ]
# # #         advice["longterm"] = [
# # #             "📊 Regular health check-ups recommended",
# # #             "🥗 Continue balanced diet and hydration",
# # #             "😴 Maintain 7-9 hours of quality sleep",
# # #         ]

# # #     elif pred_class == 1:
# # #         advice["general"] = [
# # #             "⚠️ Some health indicators require attention",
# # #             "🔍 Monitor your symptoms closely",
# # #             "⚡ Take preventive measures",
# # #         ]
# # #         advice["immediate"] = [
# # #             (
# # #                 "😷 Consider wearing a mask outdoors"
# # #                 if pm25 > 50
# # #                 else "🚶‍♂️ Limit strenuous activities"
# # #             ),
# # #             "💧 Stay well-hydrated",
# # #             "🏠 Spend more time indoors",
# # #             "📱 Keep emergency contacts ready",
# # #         ]
# # #         if hr > 100:
# # #             advice["immediate"].append("❤️ Elevated heart rate - take rest breaks")
# # #         if temp > 37.5:
# # #             advice["immediate"].append("🌡️ Monitor temperature closely")
# # #         if pm25 > 75:
# # #             advice["immediate"].append("🏭 High pollution - use air purifiers")

# # #         advice["longterm"] = [
# # #             "👨‍⚕️ Schedule a doctor check-up soon",
# # #             "📈 Track symptoms daily",
# # #             "🏃‍♀️ Exercise indoors when possible",
# # #             "🥦 Focus on anti-inflammatory foods",
# # #         ]

# # #     else:
# # #         advice["general"] = [
# # #             "🚨 URGENT: High-risk indicators detected",
# # #             "⚠️ Immediate attention recommended",
# # #             "📞 Contact healthcare provider",
# # #         ]
# # #         advice["emergency"] = [
# # #             "🏥 Seek medical attention if symptoms worsen",
# # #             "📱 Emergency: 1122 (Pakistan)",
# # #             "👨‍👩‍👧 Inform family members",
# # #             "🚫 Avoid all outdoor activities",
# # #         ]
# # #         advice["immediate"] = [
# # #             "🛑 Stay indoors",
# # #             "😷 Wear N95 mask if going outside",
# # #             "💊 Take prescribed medications",
# # #             "💧 Drink plenty of water",
# # #             "📴 Avoid strenuous activities",
# # #             "🏠 Use air purifiers",
# # #         ]

# # #         if hr > 120:
# # #             advice["emergency"].insert(0, "❤️‍🩹 CRITICAL: Very high heart rate")
# # #         if temp > 38.5:
# # #             advice["emergency"].insert(0, "🌡️ CRITICAL: High fever detected")
# # #         if pm25 > 150:
# # #             advice["immediate"].insert(0, "☠️ HAZARDOUS air quality")

# # #         advice["longterm"] = [
# # #             "🏥 URGENT: Immediate doctor appointment",
# # #             "📋 Document all symptoms",
# # #             "💊 Discuss medication adjustments",
# # #             "🔔 Set up health monitoring alerts",
# # #         ]

# # #     return advice


# # # def create_gauge_chart(
# # #     value: float, max_val: float, title: str, thresholds: list
# # # ) -> go.Figure:
# # #     """Create a gauge chart for metrics."""
# # #     fig = go.Figure(
# # #         go.Indicator(
# # #             mode="gauge+number",
# # #             value=value,
# # #             title={"text": title, "font": {"size": 16, "color": "#1E293B"}},
# # #             gauge={
# # #                 "axis": {"range": [0, max_val], "tickwidth": 1},
# # #                 "bar": {"color": "#2563EB"},
# # #                 "steps": [
# # #                     {"range": [0, thresholds[0]], "color": "#D1FAE5"},
# # #                     {"range": [thresholds[0], thresholds[1]], "color": "#FEF3C7"},
# # #                     {"range": [thresholds[1], max_val], "color": "#FEE2E2"},
# # #                 ],
# # #                 "threshold": {
# # #                     "line": {"color": "red", "width": 4},
# # #                     "thickness": 0.75,
# # #                     "value": thresholds[1],
# # #                 },
# # #             },
# # #         )
# # #     )
# # #     fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
# # #     return fig


# # # def render_citizen_dashboard() -> None:
# # #     st.cache_data.clear()

# # #     # Hero section
# # #     st.markdown(
# # #         """
# # #         <div style='background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
# # #                     padding: 2.5rem 2rem; border-radius: 16px; margin-bottom: 2rem;
# # #                     box-shadow: 0 10px 30px rgba(37, 99, 235, 0.2);'>
# # #             <div style='text-align: center;'>
# # #                 <div style='font-size: 3.5rem; margin-bottom: 0.75rem;'>🩺</div>
# # #                 <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 800;'>
# # #                     Personalized Health Risk Assessment
# # #                 </h2>
# # #                 <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem; font-size: 1.05rem;'>
# # #                     AI-powered analysis of your vital signs and environmental exposure
# # #                 </p>
# # #             </div>
# # #         </div>
# # #         """,
# # #         unsafe_allow_html=True,
# # #     )

# # #     # Patient Information
# # #     st.markdown("### 👤 Patient Information")

# # #     col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])

# # #     with col1:
# # #         name = st.text_input("Full Name", placeholder="Enter your full name")
# # #     with col2:
# # #         age = st.number_input("Age", 1, 110, 30)
# # #     with col3:
# # #         gender = st.selectbox(
# # #             "Gender", ["Prefer not to say", "Female", "Male", "Other"]
# # #         )
# # #     with col4:
# # #         location = st.selectbox(
# # #             "City", ["Lahore", "Karachi", "Islamabad", "Peshawar", "Quetta"]
# # #         )
# # #     with col5:
# # #         email = st.text_input(
# # #             "📧 Email", placeholder="your@email.com", help="We'll send your report here"
# # #         )

# # #     st.markdown("---")

# # #     # Input Method
# # #     st.markdown("### 🎛️ Health Data Input")
# # #     input_mode = st.radio(
# # #         "Input Method:", ["🎚️ Sliders", "⌨️ Manual Entry"], horizontal=True
# # #     )

# # #     st.markdown("<br>", unsafe_allow_html=True)

# # #     # Two-column layout
# # #     left_col, right_col = st.columns(2, gap="large")

# # #     with left_col:
# # #         st.markdown(
# # #             """
# # #             <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(239, 68, 68, 0.02));
# # #                         padding: 1.5rem; border-radius: 12px; border-left: 4px solid #EF4444;
# # #                         margin-bottom: 1.5rem;'>
# # #                 <h4 style='color: #1E293B; margin: 0 0 0.5rem 0; font-size: 1.25rem;'>
# # #                     💓 Vital Signs
# # #                 </h4>
# # #                 <p style='color: #64748B; margin: 0; font-size: 0.95rem;'>
# # #                     Your physiological parameters
# # #                 </p>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # #         if input_mode.startswith("🎚️"):
# # #             hr = st.slider("Heart Rate (BPM)", 50, 150, 75, help="Normal: 60-100 BPM")
# # #             st.caption("📌 Normal: 60-100 | Exercise: 100-150")

# # #             temp = st.slider(
# # #                 "Temperature (°C)", 35.0, 42.0, 36.6, 0.1, help="Normal: 36.1-37.2°C"
# # #             )
# # #             st.caption("📌 Normal: 36.1-37.2 | Fever: >37.5")
# # #         else:
# # #             hr = st.number_input("Heart Rate (BPM)", 50, 150, 75)
# # #             temp = st.number_input("Temperature (°C)", 35.0, 42.0, 36.6, 0.1)

# # #     with right_col:
# # #         st.markdown(
# # #             """
# # #             <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(16, 185, 129, 0.02));
# # #                         padding: 1.5rem; border-radius: 12px; border-left: 4px solid #10B981;
# # #                         margin-bottom: 1.5rem;'>
# # #                 <h4 style='color: #1E293B; margin: 0 0 0.5rem 0; font-size: 1.25rem;'>
# # #                     🌍 Environmental Data
# # #                 </h4>
# # #                 <p style='color: #64748B; margin: 0; font-size: 0.95rem;'>
# # #                     Current pollution levels
# # #                 </p>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # #         if input_mode.startswith("🎚️"):
# # #             pm25 = st.slider(
# # #                 "PM2.5 (µg/m³)", 0.0, 300.0, 35.0, 1.0, help="Fine particles"
# # #             )
# # #             st.caption("📌 Good: 0-35 | Moderate: 35-75 | Unhealthy: >75")

# # #             no2 = st.slider("NO₂ (ppb)", 0.0, 200.0, 25.0, 1.0, help="Nitrogen dioxide")
# # #             st.caption("📌 Good: <50 | Moderate: 50-100 | High: >100")

# # #             co = st.slider("CO (ppm)", 0.0, 10.0, 0.5, 0.1, help="Carbon monoxide")
# # #             st.caption("📌 Safe: <2 | Moderate: 2-5 | Dangerous: >5")
# # #         else:
# # #             pm25 = st.number_input("PM2.5 (µg/m³)", 0.0, 300.0, 35.0, 1.0)
# # #             no2 = st.number_input("NO₂ (ppb)", 0.0, 200.0, 25.0, 1.0)
# # #             co = st.number_input("CO (ppm)", 0.0, 10.0, 0.5, 0.1)

# # #     st.markdown("---")

# # #     # Visual gauges
# # #     st.markdown("### 📊 Current Readings Overview")
# # #     gauge_col1, gauge_col2, gauge_col3 = st.columns(3)

# # #     with gauge_col1:
# # #         fig_hr = create_gauge_chart(hr, 150, "Heart Rate (BPM)", [60, 100])
# # #         st.plotly_chart(fig_hr, use_container_width=True)

# # #     with gauge_col2:
# # #         fig_temp = create_gauge_chart(temp, 42, "Temperature (°C)", [36.1, 37.5])
# # #         st.plotly_chart(fig_temp, use_container_width=True)

# # #     with gauge_col3:
# # #         fig_pm = create_gauge_chart(pm25, 300, "PM2.5 (µg/m³)", [35, 75])
# # #         st.plotly_chart(fig_pm, use_container_width=True)

# # #     payload = {
# # #         "HeartRate": hr,
# # #         "Temp": temp,
# # #         "PM25": pm25,
# # #         "NO2": no2,
# # #         "CO_Level": co,
# # #     }

# # #     st.markdown("---")

# # #     # API Check
# # #     api_ok = check_api_health(API_BASE_URL)

# # #     if not api_ok:
# # #         st.error("🚫 API service unavailable")
# # #         with st.expander("Technical Details"):
# # #             st.code(
# # #                 "docker run --rm -p 8000:8000 -v ${PWD}:/app -w /app mlops_fl "
# # #                 "uvicorn src.deployment.api:app --host 0.0.0.0 --port 8000"
# # #             )
# # #         return

# # #     # Analysis Button
# # #     col1, col2, col3 = st.columns([1, 2, 1])
# # #     with col2:
# # #         analyze_btn = st.button(
# # #             "🔬 Analyze Health Risk", use_container_width=True, type="primary"
# # #         )

# # #     if analyze_btn:
# # #         if not email:
# # #             st.warning("⚠️ Please provide your email to receive the report")
# # #             return

# # #         try:
# # #             with st.spinner("🔄 Analyzing your data..."):
# # #                 resp = call_prediction_api(API_BASE_URL, payload)
# # #                 time.sleep(0.5)
# # #         except Exception as e:
# # #             st.error(f"❌ Error: {str(e)}")
# # #             return

# # #         pred_class = resp.get("prediction")
# # #         raw = resp.get("raw_output")

# # #         RISK_MAP = {
# # #             0: (
# # #                 "🟢 LOW RISK",
# # #                 "Health indicators within safe ranges",
# # #                 "#10B981",
# # #                 "#D1FAE5",
# # #             ),
# # #             1: (
# # #                 "🟡 MODERATE RISK",
# # #                 "Some parameters require monitoring",
# # #                 "#F59E0B",
# # #                 "#FEF3C7",
# # #             ),
# # #             2: (
# # #                 "🔴 HIGH RISK",
# # #                 "Immediate attention recommended",
# # #                 "#EF4444",
# # #                 "#FEE2E2",
# # #             ),
# # #         }

# # #         risk_label, risk_desc, risk_color, risk_bg = RISK_MAP.get(
# # #             pred_class, ("⚪ UNKNOWN", "Unable to assess", "#94A3B8", "#F1F5F9")
# # #         )

# # #         # Results Section
# # #         st.markdown("---")
# # #         st.markdown("## 📋 Assessment Results")

# # #         st.markdown(
# # #             f"""
# # #             <div style='background: {risk_bg}; border: 3px solid {risk_color};
# # #                         border-radius: 12px; padding: 2rem; margin: 1.5rem 0; text-align: center;'>
# # #                 <h2 style='color: {risk_color}; margin: 0; font-size: 2.25rem; font-weight: 800;'>
# # #                     {risk_label}
# # #                 </h2>
# # #                 <p style='font-size: 1.15rem; margin-top: 1rem; color: #1E293B; font-weight: 500;'>
# # #                     {risk_desc}
# # #                 </p>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # #         # Health Advice
# # #         advice = get_health_advice(pred_class, pm25, no2, co, hr, temp)

# # #         st.markdown("### 💊 Medical Recommendations")

# # #         if advice["emergency"]:
# # #             st.markdown("#### 🚨 Emergency Actions")
# # #             for item in advice["emergency"]:
# # #                 st.error(item)

# # #         tab1, tab2, tab3 = st.tabs(["📌 Status", "⚡ Immediate", "📈 Long-term"])

# # #         with tab1:
# # #             for item in advice["general"]:
# # #                 st.info(item)

# # #         with tab2:
# # #             for item in advice["immediate"]:
# # #                 st.success(item)

# # #         with tab3:
# # #             for item in advice["longterm"]:
# # #                 st.info(f"• {item}")

# # #         # Resources
# # #         st.markdown("---")
# # #         st.markdown("### 📚 Healthcare Resources")

# # #         res1, res2, res3 = st.columns(3)

# # #         with res1:
# # #             st.markdown(
# # #                 """
# # #                 <div style='background: rgba(16, 185, 129, 0.1); padding: 1.5rem;
# # #                             border-radius: 10px; text-align: center; border: 2px solid #10B981;'>
# # #                     <div style='font-size: 2.5rem;'>🏥</div>
# # #                     <h4 style='color: #1E293B; font-size: 1.1rem;'>Find Healthcare</h4>
# # #                     <p style='font-size: 0.95rem; color: #64748B;'>Nearby hospitals</p>
# # #                 </div>
# # #                 """,
# # #                 unsafe_allow_html=True,
# # #             )

# # #         with res2:
# # #             st.markdown(
# # #                 """
# # #                 <div style='background: rgba(239, 68, 68, 0.1); padding: 1.5rem;
# # #                             border-radius: 10px; text-align: center; border: 2px solid #EF4444;'>
# # #                     <div style='font-size: 2.5rem;'>📞</div>
# # #                     <h4 style='color: #1E293B; font-size: 1.1rem;'>Emergency: 1122</h4>
# # #                     <p style='font-size: 0.95rem; color: #64748B;'>Pakistan Emergency</p>
# # #                 </div>
# # #                 """,
# # #                 unsafe_allow_html=True,
# # #             )

# # #         with res3:
# # #             st.markdown(
# # #                 """
# # #                 <div style='background: rgba(37, 99, 235, 0.1); padding: 1.5rem;
# # #                             border-radius: 10px; text-align: center; border: 2px solid #2563EB;'>
# # #                     <div style='font-size: 2.5rem;'>📖</div>
# # #                     <h4 style='color: #1E293B; font-size: 1.1rem;'>Health Info</h4>
# # #                     <p style='font-size: 0.95rem; color: #64748B;'>Learn more</p>
# # #                 </div>
# # #                 """,
# # #                 unsafe_allow_html=True,
# # #             )

# # #         # Prepare report data
# # #         report_data = {
# # #             "name": name,
# # #             "age": age,
# # #             "location": location,
# # #             "risk": risk_label,
# # #             "vital_signs": {"heart_rate": hr, "temperature": temp},
# # #             "environmental": {"pm25": pm25, "no2": no2, "co": co},
# # #             "recommendations": advice,
# # #             "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
# # #         }

# # #         # Email and Download
# # #         st.markdown("---")

# # #         col_email, col_download = st.columns(2)

# # #         with col_email:
# # #             if st.button("📧 Email Report", use_container_width=True):
# # #                 if send_email_report(email, report_data):
# # #                     st.success(f"✅ Report sent to {email}")
# # #                 else:
# # #                     st.info("📧 Email feature requires SMTP configuration")

# # #         with col_download:
# # #             st.download_button(
# # #                 label="📥 Download Report (JSON)",
# # #                 data=json.dumps(report_data, indent=2),
# # #                 file_name=f"health_report_{time.strftime('%Y%m%d_%H%M%S')}.json",
# # #                 mime="application/json",
# # #                 use_container_width=True,
# # #             )

# # #         # Technical details
# # #         with st.expander("🔍 Technical Details"):
# # #             st.json(
# # #                 {
# # #                     "patient": {
# # #                         "name": name,
# # #                         "age": age,
# # #                         "gender": gender,
# # #                         "location": location,
# # #                     },
# # #                     "inputs": payload,
# # #                     "prediction": pred_class,
# # #                     "risk": risk_label,
# # #                     "model_output": raw,
# # #                     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
# # #                 }
# # #             )
# # import os
# # import time
# # import json
# # from typing import Dict, Optional

# # import requests
# # import streamlit as st
# # import plotly.graph_objects as go
# # from plotly.subplots import make_subplots

# # DEFAULT_API_BASE_URL = "http://host.docker.internal:8000"
# # API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


# # def check_api_health(base_url: str) -> bool:
# #     try:
# #         r = requests.get(f"{base_url}/health", timeout=2)
# #         return r.status_code == 200
# #     except Exception:
# #         return False


# # def call_prediction_api(base_url: str, payload: Dict) -> Dict:
# #     r = requests.post(f"{base_url}/predict", json=payload, timeout=5)
# #     r.raise_for_status()
# #     return r.json()


# # def create_trend_chart(
# #     value: float, max_val: float, title: str, thresholds: list, color: str
# # ) -> go.Figure:
# #     """Create a modern line chart showing trend."""
# #     # Simulate historical data
# #     import numpy as np

# #     historical = [value + np.random.uniform(-5, 5) for _ in range(10)]
# #     historical.append(value)

# #     fig = go.Figure()

# #     # Add threshold zones
# #     fig.add_hrect(
# #         y0=0,
# #         y1=thresholds[0],
# #         fillcolor="#00C896",
# #         opacity=0.1,
# #         layer="below",
# #         line_width=0,
# #     )
# #     fig.add_hrect(
# #         y0=thresholds[0],
# #         y1=thresholds[1],
# #         fillcolor="#FFA502",
# #         opacity=0.1,
# #         layer="below",
# #         line_width=0,
# #     )
# #     fig.add_hrect(
# #         y0=thresholds[1],
# #         y1=max_val,
# #         fillcolor="#FF4757",
# #         opacity=0.1,
# #         layer="below",
# #         line_width=0,
# #     )

# #     # Main line
# #     fig.add_trace(
# #         go.Scatter(
# #             y=historical,
# #             mode="lines+markers",
# #             line=dict(color=color, width=3),
# #             marker=dict(size=8, color=color),
# #             fill="tozeroy",
# #             fillcolor=f'rgba{tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.1,)}',
# #             name=title,
# #         )
# #     )

# #     # Current value marker
# #     fig.add_trace(
# #         go.Scatter(
# #             x=[len(historical) - 1],
# #             y=[value],
# #             mode="markers",
# #             marker=dict(
# #                 size=14,
# #                 color="#FF4757",
# #                 symbol="circle",
# #                 line=dict(width=3, color="white"),
# #             ),
# #             name="Current",
# #             showlegend=False,
# #         )
# #     )

# #     fig.update_layout(
# #         title=dict(text=title, font=dict(size=16, weight="bold", color="#1A202C")),
# #         height=280,
# #         margin=dict(l=10, r=10, t=40, b=10),
# #         plot_bgcolor="white",
# #         paper_bgcolor="white",
# #         xaxis=dict(showgrid=False, showticklabels=False, title=""),
# #         yaxis=dict(
# #             showgrid=True,
# #             gridcolor="#E2E8F0",
# #             range=[0, max_val],
# #             title=dict(text="", font=dict(size=12)),
# #         ),
# #         hovermode="x unified",
# #         showlegend=False,
# #     )

# #     return fig


# # def get_health_advice(
# #     pred_class: int, pm25: float, no2: float, co: float, hr: int, temp: float
# # ) -> Dict:
# #     advice = {"general": [], "immediate": [], "longterm": [], "emergency": []}

# #     if pred_class == 0:
# #         advice["general"] = [
# #             "✅ Your health indicators are within safe ranges",
# #             "🌟 Continue maintaining your healthy lifestyle",
# #             "💚 Air quality is acceptable for outdoor activities",
# #         ]
# #         advice["immediate"] = [
# #             "🚶‍♀️ Safe to engage in outdoor exercise",
# #             "🪟 Consider opening windows for ventilation",
# #             "🌱 Maintain regular physical activity",
# #         ]
# #         advice["longterm"] = [
# #             "📊 Regular health check-ups recommended",
# #             "🥗 Continue balanced diet and hydration",
# #             "😴 Maintain 7-9 hours of quality sleep",
# #         ]
# #     elif pred_class == 1:
# #         advice["general"] = [
# #             "⚠️ Some health indicators require attention",
# #             "🔍 Monitor your symptoms closely",
# #             "⚡ Take preventive measures",
# #         ]
# #         advice["immediate"] = [
# #             (
# #                 "😷 Consider wearing a mask outdoors"
# #                 if pm25 > 50
# #                 else "🚶‍♂️ Limit strenuous activities"
# #             ),
# #             "💧 Stay well-hydrated",
# #             "🏠 Spend more time indoors",
# #             "📱 Keep emergency contacts ready",
# #         ]
# #         if hr > 100:
# #             advice["immediate"].append("❤️ Elevated heart rate - take rest breaks")
# #         if temp > 37.5:
# #             advice["immediate"].append("🌡️ Monitor temperature closely")
# #         if pm25 > 75:
# #             advice["immediate"].append("🏭 High pollution - use air purifiers")

# #         advice["longterm"] = [
# #             "👨‍⚕️ Schedule a doctor check-up soon",
# #             "📈 Track symptoms daily",
# #             "🏃‍♀️ Exercise indoors when possible",
# #             "🥦 Focus on anti-inflammatory foods",
# #         ]
# #     else:
# #         advice["general"] = [
# #             "🚨 URGENT: High-risk indicators detected",
# #             "⚠️ Immediate attention recommended",
# #             "📞 Contact healthcare provider",
# #         ]
# #         advice["emergency"] = [
# #             "🏥 Seek medical attention if symptoms worsen",
# #             "📱 Emergency: 1122 (Pakistan)",
# #             "👨‍👩‍👧 Inform family members",
# #             "🚫 Avoid all outdoor activities",
# #         ]
# #         advice["immediate"] = [
# #             "🛑 Stay indoors",
# #             "😷 Wear N95 mask if going outside",
# #             "💊 Take prescribed medications",
# #             "💧 Drink plenty of water",
# #         ]

# #         if hr > 120:
# #             advice["emergency"].insert(0, "❤️‍🩹 CRITICAL: Very high heart rate")
# #         if temp > 38.5:
# #             advice["emergency"].insert(0, "🌡️ CRITICAL: High fever detected")
# #         if pm25 > 150:
# #             advice["immediate"].insert(0, "☠️ HAZARDOUS air quality")

# #         advice["longterm"] = [
# #             "🏥 URGENT: Immediate doctor appointment",
# #             "📋 Document all symptoms",
# #             "💊 Discuss medication adjustments",
# #         ]

# #     return advice


# # def render_citizen_dashboard() -> None:
# #     st.cache_data.clear()

# #     # Modern Hero Section
# #     st.markdown(
# #         """
# #         <div style='background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
# #                     padding: 3rem 2rem; border-radius: 16px; margin-bottom: 2rem;
# #                     box-shadow: 0 10px 30px rgba(0, 102, 255, 0.25);'>
# #             <div style='text-align: center;'>
# #                 <div style='font-size: 4rem; margin-bottom: 1rem;'>🩺</div>
# #                 <h2 style='color: white; margin: 0; font-size: 2.25rem; font-weight: 800;'>
# #                     Personalized Health Risk Assessment
# #                 </h2>
# #                 <p style='color: white; margin-top: 0.75rem; font-size: 1.15rem;'>
# #                     AI-powered analysis of your vital signs and environmental exposure
# #                 </p>
# #             </div>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# #     # Patient Information
# #     st.markdown("### 👤 Patient Information")

# #     col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])

# #     with col1:
# #         name = st.text_input("Full Name", placeholder="Enter your full name")
# #     with col2:
# #         age = st.number_input("Age", 1, 110, 30)
# #     with col3:
# #         gender = st.selectbox(
# #             "Gender", ["Prefer not to say", "Female", "Male", "Other"]
# #         )
# #     with col4:
# #         location = st.selectbox(
# #             "City", ["Lahore", "Karachi", "Islamabad", "Peshawar", "Quetta"]
# #         )
# #     with col5:
# #         email = st.text_input(
# #             "📧 Email", placeholder="your@email.com", help="Receive your report"
# #         )

# #     st.markdown("---")

# #     # Input Method
# #     st.markdown("### 🎛️ Health Data Input")
# #     input_mode = st.radio(
# #         "Input Method:", ["🎚️ Sliders", "⌨️ Manual Entry"], horizontal=True
# #     )

# #     st.markdown("<br>", unsafe_allow_html=True)

# #     # Two-column layout
# #     left_col, right_col = st.columns(2, gap="large")

# #     with left_col:
# #         st.markdown(
# #             """
# #             <div style='background: linear-gradient(135deg, rgba(255, 71, 87, 0.12), rgba(255, 71, 87, 0.03));
# #                         padding: 1.75rem; border-radius: 14px; border-left: 5px solid #FF4757;
# #                         margin-bottom: 1.5rem;'>
# #                 <h4 style='color: #1A202C; margin: 0 0 0.5rem 0; font-size: 1.35rem; font-weight: 700;'>
# #                     💓 Vital Signs
# #                 </h4>
# #                 <p style='color: #4A5568; margin: 0; font-size: 1rem;'>
# #                     Your physiological parameters
# #                 </p>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )

# #         if input_mode.startswith("🎚️"):
# #             hr = st.slider("Heart Rate (BPM)", 50, 150, 75, help="Normal: 60-100 BPM")
# #             st.caption("📌 **Normal**: 60-100 BPM | **Exercise**: 100-150 BPM")

# #             temp = st.slider(
# #                 "Temperature (°C)", 35.0, 42.0, 36.6, 0.1, help="Normal: 36.1-37.2°C"
# #             )
# #             st.caption("📌 **Normal**: 36.1-37.2°C | **Fever**: >37.5°C")
# #         else:
# #             hr = st.number_input("Heart Rate (BPM)", 50, 150, 75)
# #             temp = st.number_input("Temperature (°C)", 35.0, 42.0, 36.6, 0.1)

# #     with right_col:
# #         st.markdown(
# #             """
# #             <div style='background: linear-gradient(135deg, rgba(0, 200, 150, 0.12), rgba(0, 200, 150, 0.03));
# #                         padding: 1.75rem; border-radius: 14px; border-left: 5px solid #00C896;
# #                         margin-bottom: 1.5rem;'>
# #                 <h4 style='color: #1A202C; margin: 0 0 0.5rem 0; font-size: 1.35rem; font-weight: 700;'>
# #                     🌍 Environmental Data
# #                 </h4>
# #                 <p style='color: #4A5568; margin: 0; font-size: 1rem;'>
# #                     Current pollution levels
# #                 </p>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )

# #         if input_mode.startswith("🎚️"):
# #             pm25 = st.slider(
# #                 "PM2.5 (µg/m³)", 0.0, 300.0, 35.0, 1.0, help="Fine particles"
# #             )
# #             st.caption("📌 **Good**: 0-35 | **Moderate**: 35-75 | **Unhealthy**: >75")

# #             no2 = st.slider("NO₂ (ppb)", 0.0, 200.0, 25.0, 1.0, help="Nitrogen dioxide")
# #             st.caption("📌 **Good**: <50 | **Moderate**: 50-100 | **High**: >100")

# #             co = st.slider("CO (ppm)", 0.0, 10.0, 0.5, 0.1, help="Carbon monoxide")
# #             st.caption("📌 **Safe**: <2 | **Moderate**: 2-5 | **Dangerous**: >5")
# #         else:
# #             pm25 = st.number_input("PM2.5 (µg/m³)", 0.0, 300.0, 35.0, 1.0)
# #             no2 = st.number_input("NO₂ (ppb)", 0.0, 200.0, 25.0, 1.0)
# #             co = st.number_input("CO (ppm)", 0.0, 10.0, 0.5, 0.1)

# #     st.markdown("---")

# #     # Visual trend charts
# #     st.markdown("### 📊 Current Readings Overview")

# #     chart_col1, chart_col2, chart_col3 = st.columns(3)

# #     with chart_col1:
# #         fig_hr = create_trend_chart(hr, 150, "Heart Rate (BPM)", [60, 100], "#FF4757")
# #         st.plotly_chart(fig_hr, use_container_width=True)

# #     with chart_col2:
# #         fig_temp = create_trend_chart(
# #             temp, 42, "Temperature (°C)", [36.1, 37.5], "#FFA502"
# #         )
# #         st.plotly_chart(fig_temp, use_container_width=True)

# #     with chart_col3:
# #         fig_pm = create_trend_chart(pm25, 300, "PM2.5 (µg/m³)", [35, 75], "#0066FF")
# #         st.plotly_chart(fig_pm, use_container_width=True)

# #     payload = {
# #         "HeartRate": hr,
# #         "Temp": temp,
# #         "PM25": pm25,
# #         "NO2": no2,
# #         "CO_Level": co,
# #     }

# #     st.markdown("---")

# #     # API Check
# #     api_ok = check_api_health(API_BASE_URL)

# #     if not api_ok:
# #         st.error("🚫 API service unavailable")
# #         with st.expander("Technical Details"):
# #             st.code(
# #                 "docker run --rm -p 8000:8000 -v ${PWD}:/app -w /app mlops_fl "
# #                 "uvicorn src.deployment.api:app --host 0.0.0.0 --port 8000"
# #             )
# #         return

# #     # Analysis Button
# #     col1, col2, col3 = st.columns([1, 2, 1])
# #     with col2:
# #         analyze_btn = st.button(
# #             "🔬 Analyze Health Risk", use_container_width=True, type="primary"
# #         )

# #     if analyze_btn:
# #         if not email:
# #             st.warning("⚠️ Please provide your email to receive the report")
# #             return

# #         try:
# #             with st.spinner("🔄 Analyzing your data..."):
# #                 resp = call_prediction_api(API_BASE_URL, payload)
# #                 time.sleep(0.5)
# #         except Exception as e:
# #             st.error(f"❌ Error: {str(e)}")
# #             return

# #         pred_class = resp.get("prediction")
# #         raw = resp.get("raw_output")

# #         RISK_MAP = {
# #             0: (
# #                 "🟢 LOW RISK",
# #                 "Health indicators within safe ranges",
# #                 "#00C896",
# #                 "rgba(0, 200, 150, 0.15)",
# #             ),
# #             1: (
# #                 "🟡 MODERATE RISK",
# #                 "Some parameters require monitoring",
# #                 "#FFA502",
# #                 "rgba(255, 165, 2, 0.15)",
# #             ),
# #             2: (
# #                 "🔴 HIGH RISK",
# #                 "Immediate attention recommended",
# #                 "#FF4757",
# #                 "rgba(255, 71, 87, 0.15)",
# #             ),
# #         }

# #         risk_label, risk_desc, risk_color, risk_bg = RISK_MAP.get(
# #             pred_class, ("⚪ UNKNOWN", "Unable to assess", "#94A3B8", "#F7F9FC")
# #         )

# #         # Results Section
# #         st.markdown("---")
# #         st.markdown("## 📋 Assessment Results")

# #         st.markdown(
# #             f"""
# #             <div style='background: {risk_bg}; border: 3px solid {risk_color};
# #                         border-radius: 14px; padding: 2.5rem; margin: 1.5rem 0; text-align: center;
# #                         box-shadow: 0 4px 16px {risk_bg};'>
# #                 <h2 style='color: {risk_color}; margin: 0; font-size: 2.5rem; font-weight: 800;'>
# #                     {risk_label}
# #                 </h2>
# #                 <p style='font-size: 1.25rem; margin-top: 1rem; color: #1A202C; font-weight: 600;'>
# #                     {risk_desc}
# #                 </p>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )

# #         # Health Advice
# #         advice = get_health_advice(pred_class, pm25, no2, co, hr, temp)

# #         st.markdown("### 💊 Medical Recommendations")

# #         if advice["emergency"]:
# #             st.markdown("#### 🚨 Emergency Actions")
# #             for item in advice["emergency"]:
# #                 st.error(item)

# #         tab1, tab2, tab3 = st.tabs(["📌 Status", "⚡ Immediate", "📈 Long-term"])

# #         with tab1:
# #             for item in advice["general"]:
# #                 st.info(item)

# #         with tab2:
# #             for item in advice["immediate"]:
# #                 st.success(item)

# #         with tab3:
# #             for item in advice["longterm"]:
# #                 st.info(f"• {item}")

# #         # Resources
# #         st.markdown("---")
# #         st.markdown("### 📚 Healthcare Resources")

# #         res1, res2, res3 = st.columns(3)

# #         with res1:
# #             st.markdown(
# #                 """
# #                 <div style='background: rgba(0, 200, 150, 0.1); padding: 2rem;
# #                             border-radius: 12px; text-align: center; border: 2px solid #00C896;
# #                             transition: all 0.3s;'>
# #                     <div style='font-size: 3rem; margin-bottom: 0.75rem;'>🏥</div>
# #                     <h4 style='color: #1A202C; font-size: 1.2rem; margin: 0.5rem 0;'>Find Healthcare</h4>
# #                     <p style='font-size: 1rem; color: #4A5568; margin: 0;'>Nearby hospitals</p>
# #                 </div>
# #                 """,
# #                 unsafe_allow_html=True,
# #             )

# #         with res2:
# #             st.markdown(
# #                 """
# #                 <div style='background: rgba(255, 71, 87, 0.1); padding: 2rem;
# #                             border-radius: 12px; text-align: center; border: 2px solid #FF4757;
# #                             transition: all 0.3s;'>
# #                     <div style='font-size: 3rem; margin-bottom: 0.75rem;'>📞</div>
# #                     <h4 style='color: #1A202C; font-size: 1.2rem; margin: 0.5rem 0;'>Emergency: 1122</h4>
# #                     <p style='font-size: 1rem; color: #4A5568; margin: 0;'>Pakistan Emergency</p>
# #                 </div>
# #                 """,
# #                 unsafe_allow_html=True,
# #             )

# #         with res3:
# #             st.markdown(
# #                 """
# #                 <div style='background: rgba(0, 102, 255, 0.1); padding: 2rem;
# #                             border-radius: 12px; text-align: center; border: 2px solid #0066FF;
# #                             transition: all 0.3s;'>
# #                     <div style='font-size: 3rem; margin-bottom: 0.75rem;'>📖</div>
# #                     <h4 style='color: #1A202C; font-size: 1.2rem; margin: 0.5rem 0;'>Health Info</h4>
# #                     <p style='font-size: 1rem; color: #4A5568; margin: 0;'>Learn more</p>
# #                 </div>
# #                 """,
# #                 unsafe_allow_html=True,
# #             )

# #         # Prepare report data
# #         report_data = {
# #             "name": name,
# #             "age": age,
# #             "location": location,
# #             "email": email,
# #             "risk": risk_label,
# #             "vital_signs": {"heart_rate": hr, "temperature": temp},
# #             "environmental": {"pm25": pm25, "no2": no2, "co": co},
# #             "recommendations": advice,
# #             "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
# #         }

# #         # Email and Download
# #         st.markdown("---")

# #         col_email, col_download = st.columns(2)

# #         with col_email:
# #             if st.button("📧 Email Report", use_container_width=True):
# #                 st.info(
# #                     f"📧 Report will be sent to {email} (SMTP configuration required)"
# #                 )

# #         with col_download:
# #             st.download_button(
# #                 label="📥 Download Report (JSON)",
# #                 data=json.dumps(report_data, indent=2),
# #                 file_name=f"health_report_{time.strftime('%Y%m%d_%H%M%S')}.json",
# #                 mime="application/json",
# #                 use_container_width=True,
# #             )

# #         # Technical details
# #         with st.expander("🔍 Technical Details"):
# #             st.json(
# #                 {
# #                     "patient": {
# #                         "name": name,
# #                         "age": age,
# #                         "gender": gender,
# #                         "location": location,
# #                     },
# #                     "inputs": payload,
# #                     "prediction": pred_class,
# #                     "risk": risk_label,
# #                     "model_output": raw,
# #                     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
# #                 }
# #             )
# import os
# import time
# import json
# from typing import Dict, Optional

# import requests
# import streamlit as st
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# DEFAULT_API_BASE_URL = "http://host.docker.internal:8000"
# API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


# def check_api_health(base_url: str) -> bool:
#     try:
#         r = requests.get(f"{base_url}/health", timeout=2)
#         return r.status_code == 200
#     except Exception:
#         return False


# def call_prediction_api(base_url: str, payload: Dict) -> Dict:
#     r = requests.post(f"{base_url}/predict", json=payload, timeout=5)
#     r.raise_for_status()
#     return r.json()


# def create_trend_chart(
#     value: float, max_val: float, title: str, thresholds: list, color: str
# ) -> go.Figure:
#     """Create a modern line chart showing trend."""
#     import numpy as np

#     historical = [value + np.random.uniform(-5, 5) for _ in range(10)]
#     historical.append(value)

#     fig = go.Figure()

#     # Add threshold zones
#     fig.add_hrect(
#         y0=0,
#         y1=thresholds[0],
#         fillcolor="#10B981",
#         opacity=0.1,
#         layer="below",
#         line_width=0,
#     )
#     fig.add_hrect(
#         y0=thresholds[0],
#         y1=thresholds[1],
#         fillcolor="#F59E0B",
#         opacity=0.1,
#         layer="below",
#         line_width=0,
#     )
#     fig.add_hrect(
#         y0=thresholds[1],
#         y1=max_val,
#         fillcolor="#EF4444",
#         opacity=0.1,
#         layer="below",
#         line_width=0,
#     )

#     # Main line
#     fig.add_trace(
#         go.Scatter(
#             y=historical,
#             mode="lines+markers",
#             line=dict(color=color, width=3),
#             marker=dict(size=5),
#             fill="tozeroy",
#             fillcolor=f'rgba{tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.1,)}',
#             name=title,
#         )
#     )

#     # Current value marker
#     fig.add_trace(
#         go.Scatter(
#             x=[len(historical) - 1],
#             y=[value],
#             mode="markers",
#             marker=dict(
#                 size=14,
#                 color="#EF4444",
#                 symbol="circle",
#                 line=dict(width=3, color="white"),
#             ),
#             name="Current",
#             showlegend=False,
#         )
#     )

#     fig.update_layout(
#         title=dict(text=title, font=dict(size=14, weight="bold", color="#1F2937")),
#         height=260,
#         margin=dict(l=10, r=10, t=40, b=10),
#         plot_bgcolor="white",
#         paper_bgcolor="white",
#         xaxis=dict(showgrid=False, showticklabels=False, title=""),
#         yaxis=dict(
#             showgrid=True,
#             gridcolor="#E5E7EB",
#             range=[0, max_val],
#             title=dict(text="", font=dict(size=11)),
#         ),
#         hovermode="x unified",
#         showlegend=False,
#     )

#     return fig


# def get_health_advice(
#     pred_class: int, pm25: float, no2: float, co: float, hr: int, temp: float
# ) -> Dict:
#     advice = {"general": [], "immediate": [], "longterm": [], "emergency": []}

#     if pred_class == 0:
#         advice["general"] = [
#             "Your health indicators are within safe ranges",
#             "Continue maintaining your healthy lifestyle",
#             "Air quality is acceptable for outdoor activities",
#         ]
#         advice["immediate"] = [
#             "Safe to engage in outdoor exercise",
#             "Consider opening windows for ventilation",
#             "Maintain regular physical activity",
#         ]
#         advice["longterm"] = [
#             "Regular health check-ups recommended",
#             "Continue balanced diet and hydration",
#             "Maintain 7-9 hours of quality sleep",
#         ]
#     elif pred_class == 1:
#         advice["general"] = [
#             "Some health indicators require attention",
#             "Monitor your symptoms closely",
#             "Take preventive measures",
#         ]
#         advice["immediate"] = [
#             (
#                 "Consider wearing a mask outdoors"
#                 if pm25 > 50
#                 else "Limit strenuous activities"
#             ),
#             "Stay well-hydrated",
#             "Spend more time indoors",
#             "Keep emergency contacts ready",
#         ]
#         if hr > 100:
#             advice["immediate"].append("Elevated heart rate - take rest breaks")
#         if temp > 37.5:
#             advice["immediate"].append("Monitor temperature closely")
#         if pm25 > 75:
#             advice["immediate"].append("High pollution - use air purifiers")

#         advice["longterm"] = [
#             "Schedule a doctor check-up soon",
#             "Track symptoms daily",
#             "Exercise indoors when possible",
#             "Focus on anti-inflammatory foods",
#         ]
#     else:
#         advice["general"] = [
#             "URGENT: High-risk indicators detected",
#             "Immediate attention recommended",
#             "Contact healthcare provider",
#         ]
#         advice["emergency"] = [
#             "Seek medical attention if symptoms worsen",
#             "Emergency: 1122 (Pakistan)",
#             "Inform family members",
#             "Avoid all outdoor activities",
#         ]
#         advice["immediate"] = [
#             "Stay indoors",
#             "Wear N95 mask if going outside",
#             "Take prescribed medications",
#             "Drink plenty of water",
#         ]

#         if hr > 120:
#             advice["emergency"].insert(0, "CRITICAL: Very high heart rate")
#         if temp > 38.5:
#             advice["emergency"].insert(0, "CRITICAL: High fever detected")
#         if pm25 > 150:
#             advice["immediate"].insert(0, "HAZARDOUS air quality")

#         advice["longterm"] = [
#             "URGENT: Immediate doctor appointment",
#             "Document all symptoms",
#             "Discuss medication adjustments",
#         ]

#     return advice


# def render_citizen_dashboard() -> None:
#     st.cache_data.clear()

#     # Modern Hero Section
#     st.markdown(
#         """
#         <div style='background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
#                     padding: 2.5rem 2rem; border-radius: 14px; margin-bottom: 2rem;
#                     box-shadow: 0 8px 24px rgba(0, 102, 255, 0.25);'>
#             <div style='text-align: center;'>
#                 <div style='font-size: 3.5rem; margin-bottom: 0.75rem;'>🩺</div>
#                 <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 800;'>
#                     Personalized Health Risk Assessment
#                 </h2>
#                 <p style='color: white; margin-top: 0.5rem; font-size: 1.05rem;'>
#                     AI-powered analysis of your vital signs and environmental exposure
#                 </p>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     # Patient Information
#     st.markdown("### 👤 Patient Information")

#     col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])

#     with col1:
#         name = st.text_input("Full Name", placeholder="Enter your full name")
#     with col2:
#         age = st.number_input("Age", 1, 110, 30)
#     with col3:
#         gender = st.selectbox(
#             "Gender", ["Prefer not to say", "Female", "Male", "Other"]
#         )
#     with col4:
#         location = st.selectbox(
#             "City", ["Lahore", "Karachi", "Islamabad", "Peshawar", "Quetta"]
#         )
#     with col5:
#         email = st.text_input(
#             "📧 Email", placeholder="your@email.com", help="Receive your report"
#         )

#     st.markdown("---")

#     # Input Method
#     st.markdown("### 🎛️ Health Data Input")
#     input_mode = st.radio(
#         "Input Method:", ["🎚️ Sliders", "⌨️ Manual Entry"], horizontal=True
#     )

#     st.markdown("<br>", unsafe_allow_html=True)

#     # Two-column layout
#     left_col, right_col = st.columns(2, gap="large")

#     with left_col:
#         st.markdown(
#             """
#             <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.02));
#                         padding: 1.5rem; border-radius: 12px; border-left: 4px solid #EF4444;
#                         margin-bottom: 1.5rem;'>
#                 <h4 style='color: #1F2937; margin: 0 0 0.5rem 0; font-size: 1.25rem; font-weight: 700;'>
#                     💓 Vital Signs
#                 </h4>
#                 <p style='color: #6B7280; margin: 0; font-size: 0.95rem;'>
#                     Your physiological parameters
#                 </p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         if input_mode.startswith("🎚️"):
#             hr = st.slider("Heart Rate (BPM)", 50, 150, 75, help="Normal: 60-100 BPM")
#             st.caption("📌 **Normal**: 60-100 BPM | **Exercise**: 100-150 BPM")

#             temp = st.slider(
#                 "Temperature (°C)", 35.0, 42.0, 36.6, 0.1, help="Normal: 36.1-37.2°C"
#             )
#             st.caption("📌 **Normal**: 36.1-37.2°C | **Fever**: >37.5°C")
#         else:
#             hr = st.number_input("Heart Rate (BPM)", 50, 150, 75)
#             temp = st.number_input("Temperature (°C)", 35.0, 42.0, 36.6, 0.1)

#     with right_col:
#         st.markdown(
#             """
#             <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.02));
#                         padding: 1.5rem; border-radius: 12px; border-left: 4px solid #10B981;
#                         margin-bottom: 1.5rem;'>
#                 <h4 style='color: #1F2937; margin: 0 0 0.5rem 0; font-size: 1.25rem; font-weight: 700;'>
#                     🌍 Environmental Data
#                 </h4>
#                 <p style='color: #6B7280; margin: 0; font-size: 0.95rem;'>
#                     Current pollution levels
#                 </p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         if input_mode.startswith("🎚️"):
#             pm25 = st.slider(
#                 "PM2.5 (µg/m³)", 0.0, 300.0, 35.0, 1.0, help="Fine particles"
#             )
#             st.caption("📌 **Good**: 0-35 | **Moderate**: 35-75 | **Unhealthy**: >75")

#             no2 = st.slider("NO₂ (ppb)", 0.0, 200.0, 25.0, 1.0, help="Nitrogen dioxide")
#             st.caption("📌 **Good**: <50 | **Moderate**: 50-100 | **High**: >100")

#             co = st.slider("CO (ppm)", 0.0, 10.0, 0.5, 0.1, help="Carbon monoxide")
#             st.caption("📌 **Safe**: <2 | **Moderate**: 2-5 | **Dangerous**: >5")
#         else:
#             pm25 = st.number_input("PM2.5 (µg/m³)", 0.0, 300.0, 35.0, 1.0)
#             no2 = st.number_input("NO₂ (ppb)", 0.0, 200.0, 25.0, 1.0)
#             co = st.number_input("CO (ppm)", 0.0, 10.0, 0.5, 0.1)

#     st.markdown("---")

#     # Visual trend charts
#     st.markdown("### 📊 Current Readings Overview")

#     chart_col1, chart_col2, chart_col3 = st.columns(3)

#     with chart_col1:
#         fig_hr = create_trend_chart(hr, 150, "Heart Rate (BPM)", [60, 100], "#EF4444")
#         st.plotly_chart(fig_hr, use_container_width=True)

#     with chart_col2:
#         fig_temp = create_trend_chart(
#             temp, 42, "Temperature (°C)", [36.1, 37.5], "#F59E0B"
#         )
#         st.plotly_chart(fig_temp, use_container_width=True)

#     with chart_col3:
#         fig_pm = create_trend_chart(pm25, 300, "PM2.5 (µg/m³)", [35, 75], "#0066FF")
#         st.plotly_chart(fig_pm, use_container_width=True)

#     payload = {
#         "HeartRate": hr,
#         "Temp": temp,
#         "PM25": pm25,
#         "NO2": no2,
#         "CO_Level": co,
#     }

#     st.markdown("---")

#     # API Check
#     api_ok = check_api_health(API_BASE_URL)

#     if not api_ok:
#         st.error("🚫 API service unavailable")
#         with st.expander("Technical Details"):
#             st.code(
#                 "docker run --rm -p 8000:8000 -v ${PWD}:/app -w /app mlops_fl "
#                 "uvicorn src.deployment.api:app --host 0.0.0.0 --port 8000"
#             )
#         return

#     # Analysis Button
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         analyze_btn = st.button(
#             "🔬 Analyze Health Risk", use_container_width=True, type="primary"
#         )

#     if analyze_btn:
#         if not email:
#             st.warning("⚠️ Please provide your email to receive the report")
#             return

#         try:
#             with st.spinner("🔄 Analyzing your data..."):
#                 resp = call_prediction_api(API_BASE_URL, payload)
#                 time.sleep(0.5)
#         except Exception as e:
#             st.error(f"❌ Error: {str(e)}")
#             return

#         pred_class = resp.get("prediction")
#         raw = resp.get("raw_output")

#         # PERFECT HEALTH OVERRIDE
#         perfect_health = (
#             60 <= hr <= 100
#             and 36.1 <= temp <= 37.2
#             and pm25 < 35
#             and no2 < 50
#             and co < 2
#         )

#         if perfect_health:
#             pred_class = 0
#             risk_label = "🟢 PERFECT HEALTH"
#             risk_desc = "All vital signs and environmental conditions are optimal"
#             risk_color = "#10B981"
#             risk_bg = "rgba(16, 185, 129, 0.15)"
#         else:
#             RISK_MAP = {
#                 0: (
#                     "🟢 LOW RISK",
#                     "Health indicators within safe ranges",
#                     "#10B981",
#                     "rgba(16, 185, 129, 0.15)",
#                 ),
#                 1: (
#                     "🟡 MODERATE RISK",
#                     "Some parameters require monitoring",
#                     "#F59E0B",
#                     "rgba(245, 158, 11, 0.15)",
#                 ),
#                 2: (
#                     "🔴 HIGH RISK",
#                     "Immediate attention recommended",
#                     "#EF4444",
#                     "rgba(239, 68, 68, 0.15)",
#                 ),
#             }

#             risk_label, risk_desc, risk_color, risk_bg = RISK_MAP.get(
#                 pred_class, ("⚪ UNKNOWN", "Unable to assess", "#9CA3AF", "#F3F4F6")
#             )

#         # Results Section
#         st.markdown("---")
#         st.markdown("## 📋 Assessment Results")

#         st.markdown(
#             f"""
#             <div style='background: {risk_bg}; border: 3px solid {risk_color};
#                         border-radius: 14px; padding: 2.5rem; margin: 1.5rem 0; text-align: center;
#                         box-shadow: 0 4px 16px {risk_bg};'>
#                 <h2 style='color: {risk_color}; margin: 0; font-size: 2.5rem; font-weight: 800;'>
#                     {risk_label}
#                 </h2>
#                 <p style='font-size: 1.25rem; margin-top: 1rem; color: #1F2937; font-weight: 600;'>
#                     {risk_desc}
#                 </p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         # Health Advice
#         advice = get_health_advice(pred_class, pm25, no2, co, hr, temp)

#         st.markdown("### 💊 Medical Recommendations")

#         if advice["emergency"]:
#             st.markdown("#### 🚨 Emergency Actions")
#             for item in advice["emergency"]:
#                 st.error(item)

#         tab1, tab2, tab3 = st.tabs(["📌 Status", "⚡ Immediate", "📈 Long-term"])

#         with tab1:
#             for item in advice["general"]:
#                 st.info(item)

#         with tab2:
#             for item in advice["immediate"]:
#                 st.success(item)

#         with tab3:
#             for item in advice["longterm"]:
#                 st.info(f"• {item}")

#         # Resources
#         st.markdown("---")
#         st.markdown("### 📚 Healthcare Resources")

#         res1, res2, res3 = st.columns(3)

#         with res1:
#             st.markdown(
#                 """
#                 <div style='background: rgba(16, 185, 129, 0.1); padding: 2rem;
#                             border-radius: 12px; text-align: center; border: 2px solid #10B981;'>
#                     <div style='font-size: 3rem; margin-bottom: 0.75rem;'>🏥</div>
#                     <h4 style='color: #1F2937; font-size: 1.2rem; margin: 0.5rem 0;'>Find Healthcare</h4>
#                     <p style='font-size: 1rem; color: #6B7280; margin: 0;'>Nearby hospitals</p>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#         with res2:
#             st.markdown(
#                 """
#                 <div style='background: rgba(239, 68, 68, 0.1); padding: 2rem;
#                             border-radius: 12px; text-align: center; border: 2px solid #EF4444;'>
#                     <div style='font-size: 3rem; margin-bottom: 0.75rem;'>📞</div>
#                     <h4 style='color: #1F2937; font-size: 1.2rem; margin: 0.5rem 0;'>Emergency: 1122</h4>
#                     <p style='font-size: 1rem; color: #6B7280; margin: 0;'>Pakistan Emergency</p>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#         with res3:
#             st.markdown(
#                 """
#                 <div style='background: rgba(0, 102, 255, 0.1); padding: 2rem;
#                             border-radius: 12px; text-align: center; border: 2px solid #0066FF;'>
#                     <div style='font-size: 3rem; margin-bottom: 0.75rem;'>📖</div>
#                     <h4 style='color: #1F2937; font-size: 1.2rem; margin: 0.5rem 0;'>Health Info</h4>
#                     <p style='font-size: 1rem; color: #6B7280; margin: 0;'>Learn more</p>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#         # Prepare report data
#         report_data = {
#             "name": name,
#             "age": age,
#             "location": location,
#             "email": email,
#             "risk": risk_label,
#             "vital_signs": {"heart_rate": hr, "temperature": temp},
#             "environmental": {"pm25": pm25, "no2": no2, "co": co},
#             "recommendations": advice,
#             "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
#         }

#         # Email and Download
#         st.markdown("---")

#         col_email, col_download = st.columns(2)

#         with col_email:
#             if st.button("📧 Email Report", use_container_width=True):
#                 st.info(f"📧 Report will be sent to {email}")

#         with col_download:
#             st.download_button(
#                 label="📥 Download Report (JSON)",
#                 data=json.dumps(report_data, indent=2),
#                 file_name=f"health_report_{time.strftime('%Y%m%d_%H%M%S')}.json",
#                 mime="application/json",
#                 use_container_width=True,
#             )

#         # Technical details
#         with st.expander("🔍 Technical Details"):
#             st.json(
#                 {
#                     "patient": {
#                         "name": name,
#                         "age": age,
#                         "gender": gender,
#                         "location": location,
#                     },
#                     "inputs": payload,
#                     "prediction": pred_class,
#                     "risk": risk_label,
#                     "model_output": raw,
#                     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
#                 }
#             )
import os
import time
import json
from typing import Dict, Optional

import requests
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

DEFAULT_API_BASE_URL = "http://host.docker.internal:8000"
API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


def check_api_health(base_url: str) -> bool:
    try:
        r = requests.get(f"{base_url}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def call_prediction_api(base_url: str, payload: Dict) -> Dict:
    r = requests.post(f"{base_url}/predict", json=payload, timeout=5)
    r.raise_for_status()
    return r.json()


def create_trend_chart(
    value: float, max_val: float, title: str, thresholds: list, color: str
) -> go.Figure:
    import numpy as np

    historical = [value + np.random.uniform(-5, 5) for _ in range(10)]
    historical.append(value)

    fig = go.Figure()

    fig.add_hrect(
        y0=0,
        y1=thresholds[0],
        fillcolor="#10B981",
        opacity=0.1,
        layer="below",
        line_width=0,
    )
    fig.add_hrect(
        y0=thresholds[0],
        y1=thresholds[1],
        fillcolor="#F59E0B",
        opacity=0.1,
        layer="below",
        line_width=0,
    )
    fig.add_hrect(
        y0=thresholds[1],
        y1=max_val,
        fillcolor="#EF4444",
        opacity=0.1,
        layer="below",
        line_width=0,
    )

    # Main trend line
    fig.add_trace(
        go.Scatter(
            y=historical,
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor=f'rgba{tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0,2,4)) + (0.1,)}',
            name=title,
        )
    )

    # Current value
    fig.add_trace(
        go.Scatter(
            x=[len(historical) - 1],
            y=[value],
            mode="markers",
            marker=dict(
                size=14,
                color="#EF4444",
                symbol="circle",
                line=dict(width=3, color="white"),
            ),
            showlegend=False,
        )
    )

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, weight="bold", color="#1F2937")),
        height=260,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor="#E5E7EB", range=[0, max_val]),
        hovermode="x unified",
    )
    return fig


def get_health_advice(
    pred_class: int, pm25: float, no2: float, co: float, hr: int, temp: float
) -> Dict:
    advice = {"general": [], "immediate": [], "longterm": [], "emergency": []}

    if pred_class == 0:
        advice["general"] = [
            "Your health indicators are within safe ranges",
            "Continue maintaining your healthy lifestyle",
            "Air quality is acceptable for outdoor activities",
        ]
        advice["immediate"] = [
            "Safe to engage in outdoor exercise",
            "Consider opening windows for ventilation",
            "Maintain regular physical activity",
        ]
        advice["longterm"] = [
            "Regular health check-ups recommended",
            "Continue balanced diet and hydration",
            "Maintain 7-9 hours of quality sleep",
        ]

    elif pred_class == 1:
        advice["general"] = [
            "Some health indicators require attention",
            "Monitor your symptoms closely",
            "Take preventive measures",
        ]
        advice["immediate"] = [
            (
                "Consider wearing a mask outdoors"
                if pm25 > 50
                else "Limit strenuous activities"
            ),
            "Stay well-hydrated",
            "Spend more time indoors",
            "Keep emergency contacts ready",
        ]
        if hr > 100:
            advice["immediate"].append("Elevated heart rate - take rest breaks")
        if temp > 37.5:
            advice["immediate"].append("Monitor temperature closely")
        if pm25 > 75:
            advice["immediate"].append("High pollution - use air purifiers")
        advice["longterm"] = [
            "Schedule a doctor check-up soon",
            "Track symptoms daily",
            "Exercise indoors when possible",
            "Focus on anti-inflammatory foods",
        ]

    else:
        advice["general"] = [
            "URGENT: High-risk indicators detected",
            "Immediate attention recommended",
            "Contact healthcare provider",
        ]
        advice["emergency"] = [
            "Seek medical attention if symptoms worsen",
            "Emergency: 1122 (Pakistan)",
            "Inform family members",
            "Avoid all outdoor activities",
        ]
        advice["immediate"] = [
            "Stay indoors",
            "Wear N95 mask if going outside",
            "Take prescribed medications",
            "Drink plenty of water",
        ]
        if hr > 120:
            advice["emergency"].insert(0, "CRITICAL: Very high heart rate")
        if temp > 38.5:
            advice["emergency"].insert(0, "CRITICAL: High fever detected")
        if pm25 > 150:
            advice["immediate"].insert(0, "HAZARDOUS air quality")
        advice["longterm"] = [
            "URGENT: Immediate doctor appointment",
            "Document all symptoms",
            "Discuss medication adjustments",
        ]

    return advice


def render_citizen_dashboard() -> None:
    st.cache_data.clear()

    # Hero section
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
                    padding: 2.5rem 2rem; border-radius: 14px; margin-bottom: 2rem;
                    box-shadow: 0 8px 24px rgba(0,102,255,0.25);'>
            <div style='text-align: center;'>
                <div style='font-size: 3.5rem; margin-bottom: 0.75rem;'>🩺</div>
                <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 800;'>
                    Personalized Health Risk Assessment
                </h2>
                <p style='color: white; margin-top: 0.5rem; font-size: 1.05rem;'>
                    AI-powered analysis of your vital signs and environmental exposure
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Patient Info
    st.markdown("### 👤 Patient Information")

    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

    with col1:
        name = st.text_input("Full Name", placeholder="Enter your full name")
    with col2:
        age = st.number_input("Age", 1, 110, 30)
    with col3:
        gender = st.selectbox(
            "Gender", ["Prefer not to say", "Female", "Male", "Other"]
        )
    with col4:
        location = st.selectbox(
            "City", ["Lahore", "Karachi", "Islamabad", "Peshawar", "Quetta"]
        )

    st.markdown("---")

    # Input method
    st.markdown("### 🎛️ Health Data Input")
    input_mode = st.radio(
        "Input Method:", ["🎚️ Sliders", "⌨️ Manual Entry"], horizontal=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        st.markdown(
            """
            <div style='background: rgba(239,68,68,0.1); padding: 1.5rem;
                        border-radius: 12px; border-left: 4px solid #EF4444; margin-bottom: 1.5rem;'>
                <h4 style='margin:0;font-size:1.25rem;font-weight:700;color:#1F2937;'>💓 Vital Signs</h4>
                <p style='color:#6B7280;font-size:0.95rem;margin:0;'>Your physiological parameters</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if input_mode.startswith("🎚️"):
            hr = st.slider("Heart Rate (BPM)", 50, 150, 75)
            temp = st.slider("Temperature (°C)", 35.0, 42.0, 36.6, 0.1)
        else:
            hr = st.number_input("Heart Rate (BPM)", 50, 150, 75)
            temp = st.number_input("Temperature (°C)", 35.0, 42.0, 36.6, 0.1)

    with right_col:
        st.markdown(
            """
            <div style='background: rgba(16,185,129,0.1); padding: 1.5rem;
                        border-radius: 12px; border-left: 4px solid #10B981; margin-bottom: 1.5rem;'>
                <h4 style='margin:0;font-size:1.25rem;font-weight:700;color:#1F2937;'>🌍 Environmental Data</h4>
                <p style='color:#6B7280;font-size:0.95rem;margin:0;'>Current pollution levels</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if input_mode.startswith("🎚️"):
            pm25 = st.slider("PM2.5 (µg/m³)", 0.0, 300.0, 35.0)
            st.caption("📌 **Good**: 0-35 | **Moderate**: 35-75 | **Unhealthy**: >75")
            no2 = st.slider("NO₂ (ppb)", 0.0, 200.0, 25.0)
            st.caption("📌 **Good**: <50 | **Moderate**: 50-100 | **High**: >100")
            co = st.slider("CO (ppm)", 0.0, 10.0, 0.5, 0.1)
            st.caption("📌 **Safe**: <2 | **Moderate**: 2-5 | **Dangerous**: >5")
        else:
            pm25 = st.number_input("PM2.5 (µg/m³)", 0.0, 300.0, 35.0)
            no2 = st.number_input("NO₂ (ppb)", 0.0, 200.0, 25.0)
            co = st.number_input("CO (ppm)", 0.0, 10.0, 0.5)

    st.markdown("---")

    # Trend charts
    st.markdown("### 📊 Current Readings Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.plotly_chart(
            create_trend_chart(hr, 150, "Heart Rate (BPM)", [60, 100], "#EF4444"),
            use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            create_trend_chart(temp, 42, "Temperature (°C)", [36.1, 37.5], "#F59E0B"),
            use_container_width=True,
        )
    with c3:
        st.plotly_chart(
            create_trend_chart(pm25, 300, "PM2.5 (µg/m³)", [35, 75], "#0066FF"),
            use_container_width=True,
        )

    st.markdown("---")

    # API check
    if not check_api_health(API_BASE_URL):
        st.error("🚫 API service unavailable")
        return

    # Analyze button
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        analyze_btn = st.button("🔬 Analyze Health Risk", use_container_width=True)

    if analyze_btn:

        payload = {
            "HeartRate": hr,
            "Temp": temp,
            "PM25": pm25,
            "NO2": no2,
            "CO_Level": co,
        }

        try:
            with st.spinner("🔄 Analyzing your data..."):
                resp = call_prediction_api(API_BASE_URL, payload)
                time.sleep(0.5)
        except Exception as e:
            st.error(f"❌ Error: {e}")
            return

        pred_class = resp.get("prediction")
        raw = resp.get("raw_output")

        # PERFECT HEALTH OVERRIDE
        perfect_health = (
            60 <= hr <= 100
            and 36.1 <= temp <= 37.2
            and pm25 < 35
            and no2 < 50
            and co < 2
        )

        if perfect_health:
            pred_class = 0
            risk_label = "🟢 PERFECT HEALTH"
            risk_desc = "All vital signs and environmental conditions are optimal"
            risk_color = "#10B981"
            risk_bg = "rgba(16,185,129,0.15)"
        else:
            RISK_MAP = {
                0: (
                    "🟢 LOW RISK",
                    "Health indicators within safe ranges",
                    "#10B981",
                    "rgba(16,185,129,0.15)",
                ),
                1: (
                    "🟡 MODERATE RISK",
                    "Some parameters require monitoring",
                    "#F59E0B",
                    "rgba(245,158,11,0.15)",
                ),
                2: (
                    "🔴 HIGH RISK",
                    "Immediate attention recommended",
                    "#EF4444",
                    "rgba(239,68,68,0.15)",
                ),
            }
            risk_label, risk_desc, risk_color, risk_bg = RISK_MAP.get(
                pred_class, ("⚪ UNKNOWN", "Unable to assess", "#9CA3AF", "#F3F4F6")
            )

        # Result box
        st.markdown("---")
        st.markdown("## 📋 Assessment Results")

        st.markdown(
            f"""
            <div style='background:{risk_bg};border:3px solid {risk_color};padding:2.5rem;
                        border-radius:14px;text-align:center;margin:1.5rem 0;'>
                <h2 style='color:{risk_color};font-size:2.5rem;margin:0;'>{risk_label}</h2>
                <p style='color:#1F2937;font-size:1.25rem;margin-top:1rem;'>{risk_desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Recommendations
        advice = get_health_advice(pred_class, pm25, no2, co, hr, temp)

        st.markdown("### 💊 Medical Recommendations")

        if advice["emergency"]:
            st.markdown("#### 🚨 Emergency Actions")
            for item in advice["emergency"]:
                st.error(item)

        t1, t2, t3 = st.tabs(["📌 Status", "⚡ Immediate", "📈 Long-term"])

        with t1:
            for item in advice["general"]:
                st.info(item)

        with t2:
            for item in advice["immediate"]:
                st.success(item)

        with t3:
            for item in advice["longterm"]:
                st.info(f"• {item}")

        st.markdown("---")
        st.markdown("### 📚 Healthcare Resources")

        r1, r2, r3 = st.columns(3)

        with r1:
            st.markdown(
                """
                <div style='background:rgba(16,185,129,0.1);padding:2rem;border-radius:12px;text-align:center;
                            border:2px solid #10B981;'>
                    <div style='font-size:3rem;'>🏥</div>
                    <h4 style='margin:0.5rem 0;'>Find Healthcare</h4>
                    <p style='margin:0;color:#6B7280;'>Nearby hospitals</p>
                </div>""",
                unsafe_allow_html=True,
            )

        with r2:
            st.markdown(
                """
                <div style='background:rgba(239,68,68,0.1);padding:2rem;border-radius:12px;text-align:center;
                            border:2px solid #EF4444;'>
                    <div style='font-size:3rem;'>📞</div>
                    <h4 style='margin:0.5rem 0;'>Emergency: 1122</h4>
                    <p style='margin:0;color:#6B7280;'>Pakistan Emergency</p>
                </div>""",
                unsafe_allow_html=True,
            )

        with r3:
            st.markdown(
                """
                <div style='background:rgba(0,102,255,0.1);padding:2rem;border-radius:12px;text-align:center;
                            border:2px solid #0066FF;'>
                    <div style='font-size:3rem;'>📖</div>
                    <h4 style='margin:0.5rem 0;'>Health Info</h4>
                    <p style='margin:0;color:#6B7280;'>Learn more</p>
                </div>""",
                unsafe_allow_html=True,
            )

        # JSON download
        report_data = {
            "name": name,
            "age": age,
            "location": location,
            "risk": risk_label,
            "vital_signs": {"heart_rate": hr, "temperature": temp},
            "environmental": {"pm25": pm25, "no2": no2, "co": co},
            "recommendations": advice,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        st.markdown("---")

        st.download_button(
            label="📥 Download Report (JSON)",
            data=json.dumps(report_data, indent=2),
            file_name=f"health_report_{time.strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )

        with st.expander("🔍 Technical Details"):
            st.json(
                {
                    "patient": {
                        "name": name,
                        "age": age,
                        "gender": gender,
                        "location": location,
                    },
                    "inputs": payload,
                    "prediction": pred_class,
                    "model_output": raw,
                    "risk": risk_label,
                }
            )
