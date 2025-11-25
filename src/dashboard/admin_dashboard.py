# # # # # src/dashboard/admin_dashboard.py

# # # # import pathlib
# # # # import pandas as pd
# # # # import plotly.express as px
# # # # import plotly.graph_objects as go
# # # # import streamlit as st
# # # # import numpy as np
# # # # from datetime import datetime, timedelta

# # # # # ------------------------------------------------------------------
# # # # # DATA SOURCES
# # # # # ------------------------------------------------------------------
# # # # DATA_HOSPITAL_DIR = pathlib.Path("data/processed/merged_hospitals")

# # # # # City coordinates
# # # # CITY_COORDS = {
# # # #     "lahore": (31.5204, 74.3587),
# # # #     "karachi": (24.8607, 67.0011),
# # # #     "islamabad": (33.6844, 73.0479),
# # # #     "peshawar": (34.0151, 71.5249),
# # # #     "quetta": (30.1798, 66.9750),
# # # # }

# # # # # Map hospital files to cities
# # # # CITY_FILE_MAP = {
# # # #     "lahore": "client_merged_S2.csv",
# # # #     "karachi": "client_merged_S3.csv",
# # # #     "islamabad": "client_merged_S4.csv",
# # # #     "peshawar": "client_merged_S5.csv",
# # # #     "quetta": "client_merged_S9.csv",
# # # # }

# # # # # City display names
# # # # CITY_DISPLAY = {
# # # #     "lahore": "🏛️ Lahore",
# # # #     "karachi": "🏖️ Karachi",
# # # #     "islamabad": "🏔️ Islamabad",
# # # #     "peshawar": "🕌 Peshawar",
# # # #     "quetta": "⛰️ Quetta",
# # # # }


# # # # # ------------------------------------------------------------------
# # # # # HELPERS
# # # # # ------------------------------------------------------------------
# # # # def _compute_alert_level(pm25: float) -> str:
# # # #     if pd.isna(pm25):
# # # #         return "Unknown"
# # # #     if pm25 < 35:
# # # #         return "Good"
# # # #     if pm25 < 75:
# # # #         return "Moderate"
# # # #     if pm25 < 150:
# # # #         return "Unhealthy"
# # # #     return "Hazardous"


# # # # def _get_alert_color(level: str) -> str:
# # # #     colors = {
# # # #         "Good": "#52D17C",
# # # #         "Moderate": "#FF9F68",
# # # #         "Unhealthy": "#FF6B6B",
# # # #         "Hazardous": "#8B0000",
# # # #         "Unknown": "#A0AEC0",
# # # #     }
# # # #     return colors.get(level, "#A0AEC0")


# # # # @st.cache_data
# # # # def load_hospital_data() -> pd.DataFrame:
# # # #     dfs = []

# # # #     for city, file in CITY_FILE_MAP.items():
# # # #         fpath = DATA_HOSPITAL_DIR / file
# # # #         if not fpath.exists():
# # # #             continue

# # # #         df = pd.read_csv(fpath)

# # # #         expected_cols = {"Timestamp", "PM25", "NO2", "CO_Level"}
# # # #         missing = expected_cols - set(df.columns)
# # # #         if missing:
# # # #             continue

# # # #         df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
# # # #         for col in ["PM25", "NO2", "CO_Level"]:
# # # #             df[col] = pd.to_numeric(df[col], errors="coerce").clip(lower=0)

# # # #         df["city"] = city
# # # #         dfs.append(df)

# # # #     if not dfs:
# # # #         return pd.DataFrame()

# # # #     return pd.concat(dfs, ignore_index=True)


# # # # # ------------------------------------------------------------------
# # # # # MAIN RENDER FUNCTION
# # # # # ------------------------------------------------------------------
# # # # def render_admin_dashboard() -> None:
# # # #     st.cache_data.clear()

# # # #     st.markdown(
# # # #         """
# # # #         <div style="display:flex; align-items:center; justify-content:center; gap:2rem;">
# # # #             <div style="font-size:5rem;">🏛️</div>
# # # #             <div>
# # # #                 <h2 style="color:white; margin:0; font-size:2.6rem; font-weight:800;">
# # # #                     Health Authority Command Center
# # # #                 </h2>
# # # #                 <p style="color:rgba(255,255,255,0.95); margin-top:0.8rem; font-size:1.3rem; font-weight:400;">
# # # #                     Real-time environmental health monitoring and population risk assessment
# # # #                 </p>
# # # #             </div>
# # # #         </div>
# # # #         """,
# # # #         unsafe_allow_html=True,
# # # #     )

# # # #     df_all = load_hospital_data()
# # # #     if df_all.empty:
# # # #         st.error("❌ No monitoring data available.")
# # # #         return

# # # #     # ---------------- SYSTEM OVERVIEW METRICS ----------------
# # # #     st.markdown("### 📊 System Status Dashboard")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     col1, col2, col3, col4, col5 = st.columns(5)

# # # #     total_cities = df_all["city"].nunique()
# # # #     total_records = len(df_all)
# # # #     avg_pm25 = df_all["PM25"].mean()
# # # #     high_risk_count = (df_all.groupby("city")["PM25"].mean() > 75).sum()
# # # #     latest_update = df_all["Timestamp"].max()

# # # #     with col1:
# # # #         st.metric("🌍 Cities Monitored", total_cities)
# # # #     with col2:
# # # #         st.metric("📊 Total Data Points", f"{total_records:,}")
# # # #     with col3:
# # # #         st.metric("🌫️ National Avg PM2.5", f"{avg_pm25:.1f} µg/m³")
# # # #     with col4:
# # # #         st.metric("⚠️ High-Risk Zones", f"{high_risk_count}/{total_cities}")
# # # #     with col5:
# # # #         st.metric("🕐 Last Sync", latest_update.strftime("%H:%M"))

# # # #     st.markdown("---")

# # # #     # ---------------- MULTI-CITY COMPARISON ----------------
# # # #     st.markdown("### 🏙️ Inter-City Comparative Analysis")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     comp1, comp2 = st.columns([3, 1])

# # # #     with comp1:
# # # #         comparison_metric = st.selectbox(
# # # #             "📈 Select Environmental Parameter:",
# # # #             ["PM2.5 Concentration", "NO₂ Levels", "CO Levels"],
# # # #         )
# # # #     with comp2:
# # # #         sort_order = st.selectbox("🔢 Sort Order:", ["Highest First", "Lowest First"])

# # # #     metric_map = {
# # # #         "PM2.5 Concentration": "PM25",
# # # #         "NO₂ Levels": "NO2",
# # # #         "CO Levels": "CO_Level",
# # # #     }
# # # #     selected_metric = metric_map[comparison_metric]

# # # #     city_avg = df_all.groupby("city")[selected_metric].mean().reset_index()
# # # #     city_avg["city_display"] = city_avg["city"].map(CITY_DISPLAY)

# # # #     city_avg = city_avg.sort_values(
# # # #         selected_metric, ascending=(sort_order == "Lowest First")
# # # #     )

# # # #     # Color generation
# # # #     max_val = city_avg[selected_metric].max() or 1
# # # #     colors = []
# # # #     for val in city_avg[selected_metric]:
# # # #         ratio = val / max_val
# # # #         r = int(255 * ratio)
# # # #         g = int(82 + 107 * (1 - ratio))
# # # #         b = int(124 + 17 * (1 - ratio))
# # # #         colors.append(f"rgba({r},{g},{b},0.8)")

# # # #     fig = go.Figure()
# # # #     fig.add_trace(
# # # #         go.Bar(
# # # #             x=city_avg["city_display"],
# # # #             y=city_avg[selected_metric],
# # # #             marker_color=colors,
# # # #             text=[f"{v:.1f}" for v in city_avg[selected_metric]],
# # # #             textposition="outside",
# # # #         )
# # # #     )

# # # #     fig.update_layout(
# # # #         title=f"Comparative {comparison_metric} Across Cities",
# # # #         height=450,
# # # #     )

# # # #     st.plotly_chart(fig, use_container_width=True)
# # # #     st.markdown("---")

# # # #     # ---------------- CITY-LEVEL ANALYSIS ----------------
# # # #     st.markdown("### 🔬 Detailed City-Level Monitoring")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     a1, a2, a3 = st.columns([2, 1, 1])

# # # #     with a1:
# # # #         cities = sorted(df_all["city"].unique())
# # # #         selected_city = st.selectbox(
# # # #             "🏙️ Select City for Analysis:",
# # # #             cities,
# # # #             format_func=lambda x: CITY_DISPLAY.get(x, x),
# # # #         )

# # # #     with a2:
# # # #         time_range = st.selectbox(
# # # #             "⏰ Time Period:",
# # # #             ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Available Data"],
# # # #         )

# # # #     with a3:
# # # #         chart_type = st.selectbox(
# # # #             "📊 Visualization Type:",
# # # #             ["Multi-Line Chart", "Area Chart", "Scatter Plot"],
# # # #         )

# # # #     df_city = df_all[df_all["city"] == selected_city].sort_values("Timestamp")

# # # #     # Time filter
# # # #     if time_range != "All Available Data":
# # # #         latest_time = df_city["Timestamp"].max()
# # # #         delta = {"Last 24 Hours": 1, "Last 7 Days": 7, "Last 30 Days": 30}[time_range]
# # # #         df_city = df_city[df_city["Timestamp"] >= latest_time - timedelta(days=delta)]

# # # #     if df_city.empty:
# # # #         st.warning("⚠️ No data available for this selection.")
# # # #         return

# # # #     st.markdown(f"#### Environmental Trends: {CITY_DISPLAY[selected_city]}")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     # ---------------- FIXED SCATTER PLOT ----------------
# # # #     if chart_type == "Scatter Plot":
# # # #         fig_city = px.scatter(
# # # #             df_city,
# # # #             x="Timestamp",
# # # #             y="PM25",
# # # #             color="PM25",
# # # #             size=np.abs(df_city["PM25"]) + 0.1,
# # # #             color_continuous_scale=[
# # # #                 [0, "#52D17C"],
# # # #                 [0.5, "#FF9F68"],
# # # #                 [1, "#FF6B6B"],
# # # #             ],
# # # #             title="PM2.5 Distribution Analysis",
# # # #         )

# # # #     elif chart_type == "Multi-Line Chart":
# # # #         fig_city = go.Figure()
# # # #         fig_city.add_trace(
# # # #             go.Scatter(
# # # #                 x=df_city["Timestamp"],
# # # #                 y=df_city["PM25"],
# # # #                 name="PM2.5 (µg/m³)",
# # # #                 line=dict(color="#FF6B6B", width=3),
# # # #                 mode="lines+markers",
# # # #             )
# # # #         )
# # # #         fig_city.add_trace(
# # # #             go.Scatter(
# # # #                 x=df_city["Timestamp"],
# # # #                 y=df_city["NO2"],
# # # #                 name="NO₂ (ppb)",
# # # #                 line=dict(color="#4A90E2", width=3),
# # # #                 mode="lines+markers",
# # # #             )
# # # #         )
# # # #         fig_city.add_trace(
# # # #             go.Scatter(
# # # #                 x=df_city["Timestamp"],
# # # #                 y=df_city["CO_Level"] * 10,
# # # #                 name="CO (ppm ×10)",
# # # #                 line=dict(color="#4ECDC4", width=3),
# # # #                 mode="lines+markers",
# # # #             )
# # # #         )

# # # #     else:  # Area chart
# # # #         fig_city = go.Figure()
# # # #         fig_city.add_trace(
# # # #             go.Scatter(
# # # #                 x=df_city["Timestamp"],
# # # #                 y=df_city["PM25"],
# # # #                 fill="tozeroy",
# # # #                 name="PM2.5",
# # # #                 line=dict(color="#FF6B6B"),
# # # #                 fillcolor="rgba(255,107,107,0.3)",
# # # #             )
# # # #         )

# # # #     fig_city.update_layout(
# # # #         height=480,
# # # #         hovermode="x unified",
# # # #         plot_bgcolor="rgba(248,249,252,0.5)",
# # # #         paper_bgcolor="rgba(0,0,0,0)",
# # # #     )

# # # #     st.plotly_chart(fig_city, use_container_width=True)

# # # #     # ---------------- STATISTICAL SUMMARY ----------------
# # # #     st.markdown("#### 📈 Statistical Summary")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     c1, c2, c3, c4, c5 = st.columns(5)

# # # #     with c1:
# # # #         st.metric("📊 Average PM2.5", f"{df_city['PM25'].mean():.1f}")
# # # #     with c2:
# # # #         st.metric("📈 Peak PM2.5", f"{df_city['PM25'].max():.1f}")
# # # #     with c3:
# # # #         st.metric("📉 Minimum PM2.5", f"{df_city['PM25'].min():.1f}")
# # # #     with c4:
# # # #         st.metric("📊 Std Dev", f"{df_city['PM25'].std():.1f}")
# # # #     with c5:
# # # #         st.metric("⚠️ High Risk %", f"{(df_city['PM25'] > 75).mean() * 100:.1f}%")

# # # #     st.markdown("---")

# # # #     # ---------------- MAP SECTION ----------------
# # # #     st.markdown("### 🗺️ Geographic Risk Distribution Map")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     latest = df_all.sort_values("Timestamp").groupby("city").tail(1)

# # # #     latest["Alert_Level"] = latest["PM25"].apply(_compute_alert_level)
# # # #     latest["alert_color"] = latest["Alert_Level"].apply(_get_alert_color)
# # # #     latest["lat"] = latest["city"].map(lambda c: CITY_COORDS[c][0])
# # # #     latest["lon"] = latest["city"].map(lambda c: CITY_COORDS[c][1])
# # # #     latest["PM25_size"] = latest["PM25"].clip(lower=1)
# # # #     latest["city_display"] = latest["city"].map(CITY_DISPLAY)

# # # #     st.markdown("#### 📋 Current Monitoring Status")

# # # #     display_df = latest[
# # # #         ["city_display", "Timestamp", "PM25", "NO2", "CO_Level", "Alert_Level"]
# # # #     ].rename(
# # # #         columns={
# # # #             "city_display": "City",
# # # #             "PM25": "PM2.5 (µg/m³)",
# # # #             "NO2": "NO₂ (ppb)",
# # # #             "CO_Level": "CO (ppm)",
# # # #             "Alert_Level": "Air Quality Status",
# # # #         }
# # # #     )

# # # #     st.dataframe(display_df, use_container_width=True)

# # # #     st.markdown("#### 🌍 Interactive Geographic Visualization")
# # # #     fig_map = px.scatter_mapbox(
# # # #         latest,
# # # #         lat="lat",
# # # #         lon="lon",
# # # #         size="PM25_size",
# # # #         color="PM25",
# # # #         hover_name="city_display",
# # # #         zoom=4.8,
# # # #         height=600,
# # # #         mapbox_style="carto-positron",
# # # #     )

# # # #     st.plotly_chart(fig_map, use_container_width=True)

# # # #     st.markdown("---")

# # # #     # ---------------- CONTROL PANEL ----------------
# # # #     st.markdown("### 🎛️ Command Center Controls")
# # # #     st.markdown("<br>", unsafe_allow_html=True)

# # # #     c1, c2, c3, c4 = st.columns(4)

# # # #     with c1:
# # # #         if st.button("🔄 Refresh All Data", use_container_width=True):
# # # #             st.cache_data.clear()
# # # #             st.success("Data refreshed")
# # # #             st.rerun()

# # # #     with c2:
# # # #         st.download_button(
# # # #             "📥 Export CSV Report",
# # # #             latest.to_csv(index=False),
# # # #             file_name="environmental_report.csv",
# # # #             mime="text/csv",
# # # #             use_container_width=True,
# # # #         )

# # # #     with c3:
# # # #         st.download_button(
# # # #             "📥 Export JSON Data",
# # # #             latest.to_json(orient="records", indent=2),
# # # #             file_name="environmental_report.json",
# # # #             mime="application/json",
# # # #             use_container_width=True,
# # # #         )

# # # #     summary_text = (
# # # #         f"📊 System Summary\n"
# # # #         f"-------------------------\n"
# # # #         f"Cities Monitored: {total_cities}\n"
# # # #         f"Total Records: {total_records:,}\n"
# # # #         f"Average PM2.5: {avg_pm25:.1f} µg/m³\n"
# # # #     )

# # # #     with c4:
# # # #         show_summary = st.button("📄 System Summary", use_container_width=True)

# # # #     # If button clicked → show summary card + download button
# # # #     if show_summary:
# # # #         st.markdown(
# # # #             """
# # # #             <div style="
# # # #                 background: #1E293B;
# # # #                 padding: 1.5rem;
# # # #                 border-radius: 15px;
# # # #                 color: white;
# # # #                 box-shadow: 0 4px 12px rgba(0,0,0,0.15);
# # # #                 margin-top: 1rem;
# # # #             ">
# # # #                 <h4 style="margin:0; padding:0 0 10px 0; color:#F8FAFC;">📊 System Summary</h4>
# # # #                 <p style="margin:0; padding:0;">
# # # #                     <b>Cities Monitored:</b> {cities}<br>
# # # #                     <b>Total Records:</b> {records}<br>
# # # #                     <b>Average PM2.5:</b> {avg} µg/m³
# # # #                 </p>
# # # #             </div>
# # # #             """.format(
# # # #                 cities=total_cities, records=f"{total_records:,}", avg=f"{avg_pm25:.1f}"
# # # #             ),
# # # #             unsafe_allow_html=True,
# # # #         )

# # # #         # Prepare downloadable text
# # # #         summary_text = (
# # # #             "System Monitoring Summary\n"
# # # #             f"Cities Monitored: {total_cities}\n"
# # # #             f"Total Records: {total_records:,}\n"
# # # #             f"Average PM2.5: {avg_pm25:.1f} µg/m³\n"
# # # #         )

# # # #         st.download_button(
# # # #             label="⬇️ Download Summary Report",
# # # #             data=summary_text,
# # # #             file_name="system_summary.txt",
# # # #             mime="text/plain",
# # # #             use_container_width=True,
# # # #         )

# # # #     # System information
# # # #     st.markdown("---")
# # # #     st.info(
# # # #         "💡 **System Note**: Data updates automatically in real-time. Click map markers for detailed city information. Use filters to analyze specific time periods and parameters."
# # # #     )
# # # # src/dashboard/admin_dashboard.py

# # # import pathlib
# # # import pandas as pd
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # import streamlit as st
# # # import numpy as np
# # # from datetime import datetime, timedelta

# # # DATA_HOSPITAL_DIR = pathlib.Path("data/processed/merged_hospitals")

# # # CITY_COORDS = {
# # #     "lahore": (31.5204, 74.3587),
# # #     "karachi": (24.8607, 67.0011),
# # #     "islamabad": (33.6844, 73.0479),
# # #     "peshawar": (34.0151, 71.5249),
# # #     "quetta": (30.1798, 66.9750),
# # # }

# # # CITY_FILE_MAP = {
# # #     "lahore": "client_merged_S2.csv",
# # #     "karachi": "client_merged_S3.csv",
# # #     "islamabad": "client_merged_S4.csv",
# # #     "peshawar": "client_merged_S5.csv",
# # #     "quetta": "client_merged_S9.csv",
# # # }

# # # CITY_DISPLAY = {
# # #     "lahore": "🏛️ Lahore",
# # #     "karachi": "🏖️ Karachi",
# # #     "islamabad": "🏔️ Islamabad",
# # #     "peshawar": "🕌 Peshawar",
# # #     "quetta": "⛰️ Quetta",
# # # }


# # # def _compute_alert_level(pm25: float) -> str:
# # #     if pd.isna(pm25):
# # #         return "Unknown"
# # #     if pm25 < 35:
# # #         return "Good"
# # #     if pm25 < 75:
# # #         return "Moderate"
# # #     if pm25 < 150:
# # #         return "Unhealthy"
# # #     return "Hazardous"


# # # def _get_alert_color(level: str) -> str:
# # #     return {
# # #         "Good": "#10B981",
# # #         "Moderate": "#F59E0B",
# # #         "Unhealthy": "#EF4444",
# # #         "Hazardous": "#991B1B",
# # #         "Unknown": "#94A3B8",
# # #     }.get(level, "#94A3B8")


# # # @st.cache_data
# # # def load_hospital_data() -> pd.DataFrame:
# # #     dfs = []
# # #     for city, file in CITY_FILE_MAP.items():
# # #         fpath = DATA_HOSPITAL_DIR / file
# # #         if not fpath.exists():
# # #             continue
# # #         df = pd.read_csv(fpath)
# # #         expected_cols = {"Timestamp", "PM25", "NO2", "CO_Level"}
# # #         if expected_cols - set(df.columns):
# # #             continue
# # #         df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
# # #         for col in ["PM25", "NO2", "CO_Level"]:
# # #             df[col] = pd.to_numeric(df[col], errors="coerce").clip(lower=0)
# # #         df["city"] = city
# # #         dfs.append(df)
# # #     return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


# # # def render_admin_dashboard() -> None:
# # #     st.cache_data.clear()

# # #     # Hero Section
# # #     st.markdown(
# # #         """
# # #         <div style='background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
# # #                     padding: 2.5rem 2rem; border-radius: 16px; margin-bottom: 2rem;
# # #                     box-shadow: 0 10px 30px rgba(30, 64, 175, 0.2);'>
# # #             <div style='text-align: center;'>
# # #                 <div style='font-size: 3.5rem; margin-bottom: 0.75rem;'>🏛️</div>
# # #                 <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 800;'>
# # #                     Health Authority Command Center
# # #                 </h2>
# # #                 <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem; font-size: 1.05rem;'>
# # #                     Real-time environmental health monitoring and population risk assessment
# # #                 </p>
# # #             </div>
# # #         </div>
# # #         """,
# # #         unsafe_allow_html=True,
# # #     )

# # #     df_all = load_hospital_data()
# # #     if df_all.empty:
# # #         st.error("❌ No monitoring data available")
# # #         return

# # #     # System Overview
# # #     st.markdown("### 📊 System Overview")

# # #     col1, col2, col3, col4, col5 = st.columns(5)

# # #     total_cities = df_all["city"].nunique()
# # #     total_records = len(df_all)
# # #     avg_pm25 = df_all["PM25"].mean()
# # #     high_risk = (df_all.groupby("city")["PM25"].mean() > 75).sum()
# # #     latest = df_all["Timestamp"].max()

# # #     with col1:
# # #         st.metric("🌍 Cities", total_cities, "Active")
# # #     with col2:
# # #         st.metric("📊 Records", f"{total_records:,}", "Total")
# # #     with col3:
# # #         st.metric("🌫️ Avg PM2.5", f"{avg_pm25:.1f}", "µg/m³")
# # #     with col4:
# # #         st.metric("⚠️ High Risk", f"{high_risk}/{total_cities}", "Cities")
# # #     with col5:
# # #         st.metric(
# # #             "🕐 Last Update", latest.strftime("%H:%M") if pd.notna(latest) else "N/A"
# # #         )

# # #     st.markdown("---")

# # #     # Comparison Section
# # #     st.markdown("### 🏙️ Inter-City Analysis")

# # #     comp_col1, comp_col2 = st.columns([3, 1])

# # #     with comp_col1:
# # #         metric = st.selectbox(
# # #             "Environmental Parameter:",
# # #             ["PM2.5 Concentration", "NO₂ Levels", "CO Levels"],
# # #         )
# # #     with comp_col2:
# # #         sort_order = st.selectbox("Sort:", ["Highest First", "Lowest First"])

# # #     metric_map = {
# # #         "PM2.5 Concentration": "PM25",
# # #         "NO₂ Levels": "NO2",
# # #         "CO Levels": "CO_Level",
# # #     }
# # #     selected = metric_map[metric]

# # #     city_avg = df_all.groupby("city")[selected].mean().reset_index()
# # #     city_avg["city_display"] = city_avg["city"].map(CITY_DISPLAY)
# # #     city_avg = city_avg.sort_values(selected, ascending=(sort_order == "Lowest First"))

# # #     # Better bar chart
# # #     fig = go.Figure()

# # #     colors = ["#2563EB" if i % 2 == 0 else "#3B82F6" for i in range(len(city_avg))]

# # #     fig.add_trace(
# # #         go.Bar(
# # #             x=city_avg["city_display"],
# # #             y=city_avg[selected],
# # #             marker_color=colors,
# # #             marker_line_color="#1E40AF",
# # #             marker_line_width=2,
# # #             text=[f"{v:.1f}" for v in city_avg[selected]],
# # #             textposition="outside",
# # #             textfont=dict(size=13, color="#1E293B", weight="bold"),
# # #             hovertemplate="<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>",
# # #         )
# # #     )

# # #     fig.update_layout(
# # #         title=dict(
# # #             text=f"{metric} Comparison",
# # #             font=dict(size=18, color="#1E293B", weight="bold"),
# # #         ),
# # #         xaxis_title=dict(text="City", font=dict(size=13)),
# # #         yaxis_title=dict(text=metric, font=dict(size=13)),
# # #         height=400,
# # #         plot_bgcolor="#F8FAFC",
# # #         paper_bgcolor="white",
# # #         margin=dict(l=60, r=30, t=60, b=60),
# # #         showlegend=False,
# # #     )

# # #     st.plotly_chart(fig, use_container_width=True)

# # #     st.markdown("---")

# # #     # City Detail Section
# # #     st.markdown("### 🔬 City-Level Analysis")

# # #     detail_col1, detail_col2, detail_col3 = st.columns([2, 1, 1])

# # #     with detail_col1:
# # #         cities = sorted(df_all["city"].unique())
# # #         selected_city = st.selectbox(
# # #             "Select City:", cities, format_func=lambda x: CITY_DISPLAY.get(x, x)
# # #         )

# # #     with detail_col2:
# # #         time_range = st.selectbox(
# # #             "Time Period:",
# # #             ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Data"],
# # #             index=1,
# # #         )

# # #     with detail_col3:
# # #         chart_type = st.selectbox(
# # #             "Chart Type:", ["Line Chart", "Area Chart", "Scatter"], index=0
# # #         )

# # #     df_city = df_all[df_all["city"] == selected_city].sort_values("Timestamp")

# # #     # Time filtering
# # #     if time_range != "All Data":
# # #         latest_time = df_city["Timestamp"].max()
# # #         delta_map = {"Last 24 Hours": 1, "Last 7 Days": 7, "Last 30 Days": 30}
# # #         df_city = df_city[
# # #             df_city["Timestamp"] >= latest_time - timedelta(days=delta_map[time_range])
# # #         ]

# # #     if df_city.empty:
# # #         st.warning("⚠️ No data for this selection")
# # #         return

# # #     st.markdown(f"#### Environmental Trends: {CITY_DISPLAY[selected_city]}")

# # #     # Create appropriate chart
# # #     if chart_type == "Line Chart":
# # #         fig_city = go.Figure()
# # #         fig_city.add_trace(
# # #             go.Scatter(
# # #                 x=df_city["Timestamp"],
# # #                 y=df_city["PM25"],
# # #                 name="PM2.5",
# # #                 line=dict(color="#EF4444", width=3),
# # #                 mode="lines+markers",
# # #                 marker=dict(size=5),
# # #             )
# # #         )
# # #         fig_city.add_trace(
# # #             go.Scatter(
# # #                 x=df_city["Timestamp"],
# # #                 y=df_city["NO2"],
# # #                 name="NO₂",
# # #                 line=dict(color="#3B82F6", width=3),
# # #                 mode="lines+markers",
# # #                 marker=dict(size=5),
# # #             )
# # #         )
# # #         fig_city.add_trace(
# # #             go.Scatter(
# # #                 x=df_city["Timestamp"],
# # #                 y=df_city["CO_Level"] * 10,
# # #                 name="CO (×10)",
# # #                 line=dict(color="#10B981", width=3),
# # #                 mode="lines+markers",
# # #                 marker=dict(size=5),
# # #             )
# # #         )
# # #     elif chart_type == "Area Chart":
# # #         fig_city = go.Figure()
# # #         fig_city.add_trace(
# # #             go.Scatter(
# # #                 x=df_city["Timestamp"],
# # #                 y=df_city["PM25"],
# # #                 fill="tozeroy",
# # #                 name="PM2.5",
# # #                 line=dict(color="#EF4444", width=2),
# # #                 fillcolor="rgba(239, 68, 68, 0.2)",
# # #             )
# # #         )
# # #     else:
# # #         fig_city = px.scatter(
# # #             df_city,
# # #             x="Timestamp",
# # #             y="PM25",
# # #             color="PM25",
# # #             size=np.abs(df_city["PM25"]) + 0.1,
# # #             color_continuous_scale=[[0, "#10B981"], [0.5, "#F59E0B"], [1, "#EF4444"]],
# # #         )

# # #     fig_city.update_layout(
# # #         height=420,
# # #         hovermode="x unified",
# # #         plot_bgcolor="#F8FAFC",
# # #         paper_bgcolor="white",
# # #         margin=dict(l=60, r=30, t=40, b=60),
# # #         legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
# # #     )

# # #     st.plotly_chart(fig_city, use_container_width=True)

# # #     # Statistics
# # #     st.markdown("#### 📈 Statistics")

# # #     stat1, stat2, stat3, stat4, stat5 = st.columns(5)

# # #     with stat1:
# # #         st.metric("Avg PM2.5", f"{df_city['PM25'].mean():.1f}")
# # #     with stat2:
# # #         st.metric("Max PM2.5", f"{df_city['PM25'].max():.1f}")
# # #     with stat3:
# # #         st.metric("Min PM2.5", f"{df_city['PM25'].min():.1f}")
# # #     with stat4:
# # #         st.metric("Std Dev", f"{df_city['PM25'].std():.1f}")
# # #     with stat5:
# # #         st.metric("High Risk %", f"{(df_city['PM25'] > 75).mean() * 100:.1f}%")

# # #     st.markdown("---")

# # #     # Map Section
# # #     st.markdown("### 🗺️ Geographic Distribution")

# # #     latest_data = df_all.sort_values("Timestamp").groupby("city").tail(1)
# # #     latest_data["Alert_Level"] = latest_data["PM25"].apply(_compute_alert_level)
# # #     latest_data["lat"] = latest_data["city"].map(lambda c: CITY_COORDS[c][0])
# # #     latest_data["lon"] = latest_data["city"].map(lambda c: CITY_COORDS[c][1])
# # #     latest_data["PM25_size"] = latest_data["PM25"].clip(lower=1)
# # #     latest_data["city_display"] = latest_data["city"].map(CITY_DISPLAY)

# # #     st.markdown("#### 📋 Current Status")

# # #     display_df = latest_data[
# # #         ["city_display", "Timestamp", "PM25", "NO2", "CO_Level", "Alert_Level"]
# # #     ].rename(
# # #         columns={
# # #             "city_display": "City",
# # #             "PM25": "PM2.5",
# # #             "NO2": "NO₂",
# # #             "CO_Level": "CO",
# # #             "Alert_Level": "Status",
# # #         }
# # #     )

# # #     st.dataframe(display_df, use_container_width=True, height=200)

# # #     st.markdown("#### 🌍 Map View")

# # #     fig_map = px.scatter_mapbox(
# # #         latest_data,
# # #         lat="lat",
# # #         lon="lon",
# # #         size="PM25_size",
# # #         color="PM25",
# # #         hover_name="city_display",
# # #         hover_data={
# # #             "Timestamp": True,
# # #             "PM25": ":.1f",
# # #             "NO2": ":.1f",
# # #             "CO_Level": ":.2f",
# # #             "Alert_Level": True,
# # #             "PM25_size": False,
# # #             "lat": False,
# # #             "lon": False,
# # #         },
# # #         color_continuous_scale=[[0, "#10B981"], [0.4, "#F59E0B"], [1, "#EF4444"]],
# # #         zoom=4.8,
# # #         height=550,
# # #         mapbox_style="carto-positron",
# # #     )

# # #     fig_map.update_layout(
# # #         margin={"r": 0, "t": 0, "l": 0, "b": 0},
# # #         coloraxis_colorbar=dict(
# # #             title=dict(text="PM2.5", font=dict(size=12)), thickness=15, len=0.7
# # #         ),
# # #     )

# # #     st.plotly_chart(fig_map, use_container_width=True)

# # #     st.markdown("---")

# # #     # Control Panel
# # #     st.markdown("### 🎛️ Controls")

# # #     ctrl1, ctrl2, ctrl3, ctrl4 = st.columns(4)

# # #     with ctrl1:
# # #         if st.button("🔄 Refresh", use_container_width=True):
# # #             st.cache_data.clear()
# # #             st.success("Data refreshed")
# # #             st.rerun()

# # #     with ctrl2:
# # #         st.download_button(
# # #             "📥 CSV",
# # #             latest_data.to_csv(index=False),
# # #             file_name=f"report_{datetime.now().strftime('%Y%m%d')}.csv",
# # #             mime="text/csv",
# # #             use_container_width=True,
# # #         )

# # #     with ctrl3:
# # #         st.download_button(
# # #             "📥 JSON",
# # #             latest_data.to_json(orient="records", indent=2),
# # #             file_name=f"report_{datetime.now().strftime('%Y%m%d')}.json",
# # #             mime="application/json",
# # #             use_container_width=True,
# # #         )

# # #     with ctrl4:
# # #         show_summary = st.button("📄 Summary", use_container_width=True)

# # #     if show_summary:
# # #         st.markdown(
# # #             f"""
# # #             <div style='background: white; padding: 1.5rem; border-radius: 12px;
# # #                         border: 2px solid #2563EB; margin-top: 1rem;'>
# # #                 <h4 style='color: #1E293B; margin: 0 0 1rem 0;'>📊 System Summary</h4>
# # #                 <p style='color: #475569; margin: 0; line-height: 1.8;'>
# # #                     <b>Cities Monitored:</b> {total_cities}<br>
# # #                     <b>Total Records:</b> {total_records:,}<br>
# # #                     <b>Average PM2.5:</b> {avg_pm25:.1f} µg/m³<br>
# # #                     <b>High-Risk Cities:</b> {high_risk}
# # #                 </p>
# # #             </div>
# # #             """,
# # #             unsafe_allow_html=True,
# # #         )

# # #         summary_text = (
# # #             f"System Monitoring Summary\n"
# # #             f"Cities: {total_cities}\n"
# # #             f"Records: {total_records:,}\n"
# # #             f"Avg PM2.5: {avg_pm25:.1f} µg/m³\n"
# # #             f"High-Risk: {high_risk}"
# # #         )

# # #         st.download_button(
# # #             "⬇️ Download Summary",
# # #             summary_text,
# # #             file_name="summary.txt",
# # #             mime="text/plain",
# # #             use_container_width=True,
# # #         )

# # #     st.markdown("---")
# # #     st.info("💡 Real-time data updates. Click map markers for details.")
# # import pathlib
# # import pandas as pd
# # import plotly.express as px
# # import plotly.graph_objects as go
# # import streamlit as st
# # import numpy as np
# # from datetime import datetime, timedelta

# # DATA_HOSPITAL_DIR = pathlib.Path("data/processed/merged_hospitals")

# # CITY_COORDS = {
# #     "lahore": (31.5204, 74.3587),
# #     "karachi": (24.8607, 67.0011),
# #     "islamabad": (33.6844, 73.0479),
# #     "peshawar": (34.0151, 71.5249),
# #     "quetta": (30.1798, 66.9750),
# # }

# # CITY_FILE_MAP = {
# #     "lahore": "client_merged_S2.csv",
# #     "karachi": "client_merged_S3.csv",
# #     "islamabad": "client_merged_S4.csv",
# #     "peshawar": "client_merged_S5.csv",
# #     "quetta": "client_merged_S9.csv",
# # }

# # CITY_DISPLAY = {
# #     "lahore": "🏛️ Lahore",
# #     "karachi": "🏖️ Karachi",
# #     "islamabad": "🏔️ Islamabad",
# #     "peshawar": "🕌 Peshawar",
# #     "quetta": "⛰️ Quetta",
# # }


# # def _compute_alert_level(pm25: float) -> str:
# #     if pd.isna(pm25):
# #         return "Unknown"
# #     if pm25 < 35:
# #         return "Good"
# #     if pm25 < 75:
# #         return "Moderate"
# #     if pm25 < 150:
# #         return "Unhealthy"
# #     return "Hazardous"


# # @st.cache_data
# # def load_hospital_data() -> pd.DataFrame:
# #     dfs = []
# #     for city, file in CITY_FILE_MAP.items():
# #         fpath = DATA_HOSPITAL_DIR / file
# #         if not fpath.exists():
# #             continue
# #         df = pd.read_csv(fpath)
# #         expected_cols = {"Timestamp", "PM25", "NO2", "CO_Level"}
# #         if expected_cols - set(df.columns):
# #             continue
# #         df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
# #         for col in ["PM25", "NO2", "CO_Level"]:
# #             df[col] = pd.to_numeric(df[col], errors="coerce").clip(lower=0)
# #         df["city"] = city
# #         dfs.append(df)
# #     return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


# # def render_admin_dashboard() -> None:
# #     st.cache_data.clear()

# #     # Modern Hero Section
# #     st.markdown(
# #         """
# #         <div style='background: linear-gradient(135deg, #1A365D 0%, #0F172A 100%);
# #                     padding: 3rem 2rem; border-radius: 16px; margin-bottom: 2rem;
# #                     box-shadow: 0 10px 30px rgba(26, 54, 93, 0.3);'>
# #             <div style='text-align: center;'>
# #                 <div style='font-size: 4rem; margin-bottom: 1rem;'>🏛️</div>
# #                 <h2 style='color: white; margin: 0; font-size: 2.25rem; font-weight: 800;'>
# #                     Health Authority Command Center
# #                 </h2>
# #                 <p style='color: rgba(255,255,255,0.95); margin-top: 0.75rem; font-size: 1.15rem;'>
# #                     Real-time environmental health monitoring and population risk assessment
# #                 </p>
# #             </div>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# #     df_all = load_hospital_data()
# #     if df_all.empty:
# #         st.error("❌ No monitoring data available")
# #         return

# #     # System Overview
# #     st.markdown("### 📊 System Overview")

# #     col1, col2, col3, col4, col5 = st.columns(5)

# #     total_cities = df_all["city"].nunique()
# #     total_records = len(df_all)
# #     avg_pm25 = df_all["PM25"].mean()
# #     high_risk = (df_all.groupby("city")["PM25"].mean() > 75).sum()
# #     latest = df_all["Timestamp"].max()

# #     with col1:
# #         st.metric("🌍 CITIES", total_cities, "Active")
# #     with col2:
# #         st.metric("📊 RECORDS", f"{total_records:,}", "Total")
# #     with col3:
# #         st.metric("🌫️ AVG PM2.5", f"{avg_pm25:.1f}", "µg/m³")
# #     with col4:
# #         st.metric("⚠️ HIGH RISK", f"{high_risk}/{total_cities}", "Cities")
# #     with col5:
# #         st.metric(
# #             "🕐 LAST UPDATE", latest.strftime("%H:%M") if pd.notna(latest) else "N/A"
# #         )

# #     st.markdown("---")

# #     # Comparison Section
# #     st.markdown("### 🏙️ Inter-City Analysis")

# #     comp_col1, comp_col2 = st.columns([3, 1])

# #     with comp_col1:
# #         metric = st.selectbox(
# #             "Environmental Parameter:",
# #             ["PM2.5 Concentration", "NO₂ Levels", "CO Levels"],
# #         )
# #     with comp_col2:
# #         sort_order = st.selectbox("Sort:", ["Highest First", "Lowest First"])

# #     metric_map = {
# #         "PM2.5 Concentration": "PM25",
# #         "NO₂ Levels": "NO2",
# #         "CO Levels": "CO_Level",
# #     }
# #     selected = metric_map[metric]

# #     city_avg = df_all.groupby("city")[selected].mean().reset_index()
# #     city_avg["city_display"] = city_avg["city"].map(CITY_DISPLAY)
# #     city_avg = city_avg.sort_values(selected, ascending=(sort_order == "Lowest First"))

# #     # Modern bar chart
# #     fig = go.Figure()

# #     colors = ["#0066FF", "#0052CC", "#00C896", "#FFA502", "#FF4757"][: len(city_avg)]

# #     fig.add_trace(
# #         go.Bar(
# #             x=city_avg["city_display"],
# #             y=city_avg[selected],
# #             marker=dict(color=colors, line=dict(color="white", width=2)),
# #             text=[f"{v:.1f}" for v in city_avg[selected]],
# #             textposition="outside",
# #             textfont=dict(size=13, color="#1A202C", weight="bold"),
# #             hovertemplate="<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>",
# #         )
# #     )

# #     fig.update_layout(
# #         title=dict(
# #             text=f"{metric} Comparison Across Cities",
# #             font=dict(size=18, weight="bold", color="#1A202C"),
# #         ),
# #         xaxis_title="",
# #         yaxis_title=metric,
# #         height=420,
# #         plot_bgcolor="white",
# #         paper_bgcolor="white",
# #         margin=dict(l=60, r=30, t=60, b=60),
# #         showlegend=False,
# #         xaxis=dict(showgrid=False),
# #         yaxis=dict(showgrid=True, gridcolor="#E2E8F0"),
# #     )

# #     st.plotly_chart(fig, use_container_width=True)

# #     st.markdown("---")

# #     # City Detail Section
# #     st.markdown("### 🔬 City-Level Analysis")

# #     detail_col1, detail_col2, detail_col3 = st.columns([2, 1, 1])

# #     with detail_col1:
# #         cities = sorted(df_all["city"].unique())
# #         selected_city = st.selectbox(
# #             "Select City:", cities, format_func=lambda x: CITY_DISPLAY.get(x, x)
# #         )

# #     with detail_col2:
# #         time_range = st.selectbox(
# #             "Time Period:",
# #             ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Data"],
# #             index=1,
# #         )

# #     with detail_col3:
# #         chart_style = st.selectbox(
# #             "Chart Style:", ["Multi-Line", "Area", "Scatter"], index=0
# #         )

# #     df_city = df_all[df_all["city"] == selected_city].sort_values("Timestamp")

# #     # Time filtering
# #     if time_range != "All Data":
# #         latest_time = df_city["Timestamp"].max()
# #         delta_map = {"Last 24 Hours": 1, "Last 7 Days": 7, "Last 30 Days": 30}
# #         df_city = df_city[
# #             df_city["Timestamp"] >= latest_time - timedelta(days=delta_map[time_range])
# #         ]

# #     if df_city.empty:
# #         st.warning("⚠️ No data for this selection")
# #         return

# #     st.markdown(f"#### Environmental Trends: {CITY_DISPLAY[selected_city]}")

# #     # Create modern chart
# #     if chart_style == "Multi-Line":
# #         fig_city = go.Figure()

# #         fig_city.add_trace(
# #             go.Scatter(
# #                 x=df_city["Timestamp"],
# #                 y=df_city["PM25"],
# #                 name="PM2.5",
# #                 line=dict(color="#FF4757", width=3),
# #                 mode="lines",
# #                 fill="tozeroy",
# #                 fillcolor="rgba(255, 71, 87, 0.1)",
# #             )
# #         )

# #         fig_city.add_trace(
# #             go.Scatter(
# #                 x=df_city["Timestamp"],
# #                 y=df_city["NO2"],
# #                 name="NO₂",
# #                 line=dict(color="#0066FF", width=3),
# #                 mode="lines",
# #                 fill="tozeroy",
# #                 fillcolor="rgba(0, 102, 255, 0.1)",
# #             )
# #         )

# #         fig_city.add_trace(
# #             go.Scatter(
# #                 x=df_city["Timestamp"],
# #                 y=df_city["CO_Level"] * 10,
# #                 name="CO (×10)",
# #                 line=dict(color="#00C896", width=3),
# #                 mode="lines",
# #                 fill="tozeroy",
# #                 fillcolor="rgba(0, 200, 150, 0.1)",
# #             )
# #         )

# #     elif chart_style == "Area":
# #         fig_city = go.Figure()
# #         fig_city.add_trace(
# #             go.Scatter(
# #                 x=df_city["Timestamp"],
# #                 y=df_city["PM25"],
# #                 fill="tozeroy",
# #                 name="PM2.5",
# #                 line=dict(color="#0066FF", width=2),
# #                 fillcolor="rgba(0, 102, 255, 0.2)",
# #             )
# #         )
# #     else:
# #         fig_city = px.scatter(
# #             df_city,
# #             x="Timestamp",
# #             y="PM25",
# #             color="PM25",
# #             size=np.abs(df_city["PM25"]) + 0.1,
# #             color_continuous_scale=[[0, "#00C896"], [0.5, "#FFA502"], [1, "#FF4757"]],
# #         )

# #     fig_city.update_layout(
# #         height=450,
# #         hovermode="x unified",
# #         plot_bgcolor="white",
# #         paper_bgcolor="white",
# #         margin=dict(l=60, r=30, t=40, b=60),
# #         legend=dict(
# #             orientation="h",
# #             yanchor="bottom",
# #             y=1.02,
# #             xanchor="center",
# #             x=0.5,
# #             bgcolor="rgba(255,255,255,0.8)",
# #             bordercolor="#E2E8F0",
# #             borderwidth=1,
# #         ),
# #         xaxis=dict(showgrid=False),
# #         yaxis=dict(showgrid=True, gridcolor="#E2E8F0"),
# #     )

# #     st.plotly_chart(fig_city, use_container_width=True)

# #     # Statistics
# #     st.markdown("#### 📈 Statistical Summary")

# #     stat1, stat2, stat3, stat4, stat5 = st.columns(5)

# #     with stat1:
# #         st.metric("AVG PM2.5", f"{df_city['PM25'].mean():.1f}")
# #     with stat2:
# #         st.metric("MAX PM2.5", f"{df_city['PM25'].max():.1f}")
# #     with stat3:
# #         st.metric("MIN PM2.5", f"{df_city['PM25'].min():.1f}")
# #     with stat4:
# #         st.metric("STD DEV", f"{df_city['PM25'].std():.1f}")
# #     with stat5:
# #         st.metric("HIGH RISK %", f"{(df_city['PM25'] > 75).mean() * 100:.1f}%")

# #     st.markdown("---")

# #     # Map Section
# #     st.markdown("### 🗺️ Geographic Distribution")

# #     latest_data = df_all.sort_values("Timestamp").groupby("city").tail(1)
# #     latest_data["Alert_Level"] = latest_data["PM25"].apply(_compute_alert_level)
# #     latest_data["lat"] = latest_data["city"].map(lambda c: CITY_COORDS[c][0])
# #     latest_data["lon"] = latest_data["city"].map(lambda c: CITY_COORDS[c][1])
# #     latest_data["PM25_size"] = latest_data["PM25"].clip(lower=1)
# #     latest_data["city_display"] = latest_data["city"].map(CITY_DISPLAY)

# #     st.markdown("#### 📋 Current Status Table")

# #     display_df = latest_data[
# #         ["city_display", "Timestamp", "PM25", "NO2", "CO_Level", "Alert_Level"]
# #     ].rename(
# #         columns={
# #             "city_display": "City",
# #             "PM25": "PM2.5 (µg/m³)",
# #             "NO2": "NO₂ (ppb)",
# #             "CO_Level": "CO (ppm)",
# #             "Alert_Level": "Status",
# #         }
# #     )

# #     st.dataframe(display_df, use_container_width=True, height=220)

# #     st.markdown("#### 🌍 Interactive Map")

# #     fig_map = px.scatter_mapbox(
# #         latest_data,
# #         lat="lat",
# #         lon="lon",
# #         size="PM25_size",
# #         color="PM25",
# #         hover_name="city_display",
# #         hover_data={
# #             "Timestamp": True,
# #             "PM25": ":.1f",
# #             "NO2": ":.1f",
# #             "CO_Level": ":.2f",
# #             "Alert_Level": True,
# #             "PM25_size": False,
# #             "lat": False,
# #             "lon": False,
# #         },
# #         color_continuous_scale=[[0, "#00C896"], [0.4, "#FFA502"], [1, "#FF4757"]],
# #         zoom=4.8,
# #         height=580,
# #         mapbox_style="carto-positron",
# #     )

# #     fig_map.update_layout(
# #         margin={"r": 0, "t": 0, "l": 0, "b": 0},
# #         coloraxis_colorbar=dict(
# #             title=dict(text="PM2.5 (µg/m³)", font=dict(size=12)), thickness=18, len=0.75
# #         ),
# #     )

# #     st.plotly_chart(fig_map, use_container_width=True)

# #     st.markdown("---")

# #     # Control Panel
# #     st.markdown("### 🎛️ Command Center Controls")

# #     ctrl1, ctrl2, ctrl3, ctrl4 = st.columns(4)

# #     with ctrl1:
# #         if st.button("🔄 Refresh Data", use_container_width=True):
# #             st.cache_data.clear()
# #             st.success("✅ Data refreshed")
# #             st.rerun()

# #     with ctrl2:
# #         st.download_button(
# #             "📥 Export CSV",
# #             latest_data.to_csv(index=False),
# #             file_name=f"report_{datetime.now().strftime('%Y%m%d')}.csv",
# #             mime="text/csv",
# #             use_container_width=True,
# #         )

# #     with ctrl3:
# #         st.download_button(
# #             "📥 Export JSON",
# #             latest_data.to_json(orient="records", indent=2),
# #             file_name=f"report_{datetime.now().strftime('%Y%m%d')}.json",
# #             mime="application/json",
# #             use_container_width=True,
# #         )

# #     with ctrl4:
# #         show_summary = st.button("📄 System Summary", use_container_width=True)

# #     if show_summary:
# #         st.markdown(
# #             f"""
# #             <div style='background: white; padding: 2rem; border-radius: 14px;
# #                         border: 2px solid #0066FF; margin-top: 1.5rem;
# #                         box-shadow: 0 4px 16px rgba(0, 102, 255, 0.1);'>
# #                 <h4 style='color: #1A202C; margin: 0 0 1.25rem 0; font-size: 1.5rem; font-weight: 700;'>
# #                     📊 System Monitoring Summary
# #                 </h4>
# #                 <p style='color: #4A5568; margin: 0; line-height: 2; font-size: 1.05rem;'>
# #                     <b>Cities Monitored:</b> {total_cities}<br>
# #                     <b>Total Records:</b> {total_records:,}<br>
# #                     <b>Average PM2.5:</b> {avg_pm25:.1f} µg/m³<br>
# #                     <b>High-Risk Cities:</b> {high_risk}/{total_cities}
# #                 </p>
# #             </div>
# #             """,
# #             unsafe_allow_html=True,
# #         )

# #         summary_text = (
# #             f"System Monitoring Summary\n"
# #             f"========================\n"
# #             f"Cities Monitored: {total_cities}\n"
# #             f"Total Records: {total_records:,}\n"
# #             f"Average PM2.5: {avg_pm25:.1f} µg/m³\n"
# #             f"High-Risk Cities: {high_risk}/{total_cities}\n"
# #             f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
# #         )

# #         st.download_button(
# #             "⬇️ Download Summary Report",
# #             summary_text,
# #             file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
# #             mime="text/plain",
# #             use_container_width=True,
# #         )

# #     st.markdown("---")
# #     st.info(
# #         "💡 **System Note**: Data updates in real-time. Click map markers for city details. Use filters for historical analysis."
# #     )
# import pathlib
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import streamlit as st
# import numpy as np
# from datetime import datetime, timedelta

# # Using FontAwesome for professional icons
# FA_ICON_COMMAND = '<i class="fas fa-chart-line"></i>'
# FA_ICON_CITY = '<i class="fas fa-city"></i>'
# FA_ICON_METRIC = '<i class="fas fa-database"></i>'
# FA_ICON_SMOG = '<i class="fas fa-smog"></i>'
# FA_ICON_RISK_WARN = '<i class="fas fa-exclamation-circle"></i>'
# FA_ICON_TIME = '<i class="fas fa-clock"></i>'
# FA_ICON_REFRESH = '<i class="fas fa-sync-alt"></i>'

# DATA_HOSPITAL_DIR = pathlib.Path("data/processed/merged_hospitals")

# CITY_COORDS = {
#     "lahore": (31.5204, 74.3587),
#     "karachi": (24.8607, 67.0011),
#     "islamabad": (33.6844, 73.0479),
#     "peshawar": (34.0151, 71.5249),
#     "quetta": (30.1798, 66.9750),
# }

# CITY_FILE_MAP = {
#     "lahore": "client_merged_S2.csv",
#     "karachi": "client_merged_S3.csv",
#     "islamabad": "client_merged_S4.csv",
#     "peshawar": "client_merged_S5.csv",
#     "quetta": "client_merged_S9.csv",
# }

# # Cleaner, professional display names
# CITY_DISPLAY = {
#     "lahore": "Lahore",
#     "karachi": "Karachi",
#     "islamabad": "Islamabad",
#     "peshawar": "Peshawar",
#     "quetta": "Quetta",
# }


# def _compute_alert_level(pm25: float) -> str:
#     if pd.isna(pm25):
#         return "Unknown"
#     if pm25 < 35:
#         return "Good"
#     if pm25 < 75:
#         return "Moderate"
#     if pm25 < 150:
#         return "Unhealthy"
#     return "Hazardous"


# @st.cache_data
# def load_hospital_data() -> pd.DataFrame:
#     dfs = []
#     for city, file in CITY_FILE_MAP.items():
#         fpath = DATA_HOSPITAL_DIR / file
#         if not fpath.exists():
#             continue
#         df = pd.read_csv(fpath)
#         expected_cols = {"Timestamp", "PM25", "NO2", "CO_Level"}
#         if expected_cols - set(df.columns):
#             continue
#         df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
#         for col in ["PM25", "NO2", "CO_Level"]:
#             df[col] = pd.to_numeric(df[col], errors="coerce").clip(lower=0)
#         df["city"] = city
#         dfs.append(df)
#     return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


# def render_admin_dashboard() -> None:
#     st.cache_data.clear()

#     # Modern Hero Section
#     st.markdown(
#         f"""
#         <div style='background: linear-gradient(135deg, #1A365D 0%, #0F172A 100%);
#                     padding: 3rem 2rem; border-radius: 16px; margin-bottom: 2rem;
#                     box-shadow: 0 10px 30px rgba(26, 54, 93, 0.3);'>
#             <div style='text-align: center;'>
#                 <div style='font-size: 4rem; margin-bottom: 1rem; color: white;'>
#                     <i class="fas fa-university"></i>
#                 </div>
#                 <h2 style='color: white; margin: 0; font-size: 2.25rem; font-weight: 800;'>
#                     Health Authority Command Center
#                 </h2>
#                 <p style='color: rgba(255,255,255,0.95); margin-top: 0.75rem; font-size: 1.15rem;'>
#                     Real-time environmental health monitoring and population risk assessment
#                 </p>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     df_all = load_hospital_data()
#     if df_all.empty:
#         st.error("❌ No monitoring data available. Check data directory.")
#         return

#     # System Overview
#     st.markdown(f"### {FA_ICON_COMMAND} System Overview")

#     col1, col2, col3, col4, col5 = st.columns(5)

#     total_cities = df_all["city"].nunique()
#     total_records = len(df_all)
#     avg_pm25 = df_all["PM25"].mean()
#     high_risk = (df_all.groupby("city")["PM25"].mean() > 75).sum()
#     latest = df_all["Timestamp"].max()

#     with col1:
#         st.metric(f"{FA_ICON_CITY} CITIES", total_cities, "Active")
#     with col2:
#         st.metric(f"{FA_ICON_METRIC} RECORDS", f"{total_records:,}", "Total")
#     with col3:
#         st.metric(f"{FA_ICON_SMOG} AVG PM2.5", f"{avg_pm25:.1f}", "µg/m³")
#     with col4:
#         st.metric(
#             f"{FA_ICON_RISK_WARN} HIGH RISK", f"{high_risk}/{total_cities}", "Cities"
#         )
#     with col5:
#         st.metric(
#             f"{FA_ICON_TIME} LAST UPDATE",
#             latest.strftime("%H:%M") if pd.notna(latest) else "N/A",
#         )

#     st.markdown("---")

#     # Comparison Section
#     st.markdown("### 🏙️ Inter-City Analysis")

#     comp_col1, comp_col2 = st.columns([3, 1])

#     with comp_col1:
#         metric = st.selectbox(
#             "Environmental Parameter:",
#             ["PM2.5 Concentration", "NO₂ Levels", "CO Levels"],
#         )
#     with comp_col2:
#         sort_order = st.selectbox("Sort:", ["Highest First", "Lowest First"])

#     metric_map = {
#         "PM2.5 Concentration": "PM25",
#         "NO₂ Levels": "NO2",
#         "CO Levels": "CO_Level",
#     }
#     selected = metric_map[metric]

#     city_avg = df_all.groupby("city")[selected].mean().reset_index()
#     city_avg["city_display"] = city_avg["city"].map(CITY_DISPLAY)
#     city_avg = city_avg.sort_values(selected, ascending=(sort_order == "Lowest First"))

#     # Modern bar chart with defined colors
#     fig = go.Figure()

#     colors = ["#0066FF", "#1A365D", "#00C896", "#FFA502", "#FF4757"][: len(city_avg)]

#     fig.add_trace(
#         go.Bar(
#             x=city_avg["city_display"],
#             y=city_avg[selected],
#             marker=dict(color=colors, line=dict(color="white", width=2)),
#             text=[f"{v:.1f}" for v in city_avg[selected]],
#             textposition="outside",
#             textfont=dict(size=13, color="#1A202C", weight="bold"),
#             hovertemplate="<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>",
#         )
#     )

#     fig.update_layout(
#         title=dict(
#             text=f"{metric} Comparison Across Cities",
#             font=dict(size=18, weight="bold", color="#1A202C"),
#         ),
#         xaxis_title="",
#         yaxis_title=metric,
#         height=420,
#         plot_bgcolor="white",
#         paper_bgcolor="white",
#         margin=dict(l=60, r=30, t=60, b=60),
#         showlegend=False,
#         xaxis=dict(showgrid=False),
#         yaxis=dict(showgrid=True, gridcolor="#E2E8F0"),
#     )

#     st.plotly_chart(fig, use_container_width=True)

#     st.markdown("---")

#     # City Detail Section
#     st.markdown("### 🔬 City-Level Analysis")

#     detail_col1, detail_col2, detail_col3 = st.columns([2, 1, 1])

#     with detail_col1:
#         cities = sorted(df_all["city"].unique())
#         selected_city = st.selectbox(
#             "Select City:", cities, format_func=lambda x: CITY_DISPLAY.get(x, x)
#         )

#     with detail_col2:
#         time_range = st.selectbox(
#             "Time Period:",
#             ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Data"],
#             index=1,
#         )

#     with detail_col3:
#         chart_style = st.selectbox(
#             "Chart Style:", ["Multi-Line", "Area", "Scatter"], index=0
#         )

#     df_city = df_all[df_all["city"] == selected_city].sort_values("Timestamp")

#     # Time filtering
#     if time_range != "All Data":
#         latest_time = df_city["Timestamp"].max()
#         delta_map = {"Last 24 Hours": 1, "Last 7 Days": 7, "Last 30 Days": 30}
#         df_city = df_city[
#             df_city["Timestamp"] >= latest_time - timedelta(days=delta_map[time_range])
#         ]

#     if df_city.empty:
#         st.warning(
#             f"⚠️ No data available for {CITY_DISPLAY[selected_city]} in the selected time range."
#         )
#         return

#     st.markdown(f"#### Environmental Trends: {CITY_DISPLAY[selected_city]}")

#     # Create modern chart
#     if chart_style == "Multi-Line":
#         fig_city = go.Figure()

#         # Use primary, danger, and secondary colors
#         fig_city.add_trace(
#             go.Scatter(
#                 x=df_city["Timestamp"],
#                 y=df_city["PM25"],
#                 name="PM2.5",
#                 line=dict(color="#FF4757", width=3),  # Danger
#                 mode="lines",
#                 fill="tozeroy",
#                 fillcolor="rgba(255, 71, 87, 0.1)",
#             )
#         )

#         fig_city.add_trace(
#             go.Scatter(
#                 x=df_city["Timestamp"],
#                 y=df_city["NO2"],
#                 name="NO₂",
#                 line=dict(color="#0066FF", width=3),  # Primary
#                 mode="lines",
#                 fill="tozeroy",
#                 fillcolor="rgba(0, 102, 255, 0.1)",
#             )
#         )

#         fig_city.add_trace(
#             go.Scatter(
#                 x=df_city["Timestamp"],
#                 y=df_city["CO_Level"] * 10,
#                 name="CO (×10)",
#                 line=dict(color="#00C896", width=3),  # Secondary
#                 mode="lines",
#                 fill="tozeroy",
#                 fillcolor="rgba(0, 200, 150, 0.1)",
#             )
#         )

#     elif chart_style == "Area":
#         # Simplified area chart focusing on PM2.5
#         fig_city = go.Figure()
#         fig_city.add_trace(
#             go.Scatter(
#                 x=df_city["Timestamp"],
#                 y=df_city["PM25"],
#                 fill="tozeroy",
#                 name="PM2.5",
#                 line=dict(color="#0066FF", width=2),
#                 fillcolor="rgba(0, 102, 255, 0.2)",
#             )
#         )
#     else:
#         # Scatter chart with professional colors
#         fig_city = px.scatter(
#             df_city,
#             x="Timestamp",
#             y="PM25",
#             color="PM25",
#             size=np.abs(df_city["PM25"]) + 0.1,
#             color_continuous_scale=[[0, "#00C896"], [0.5, "#FFA502"], [1, "#FF4757"]],
#         )

#     fig_city.update_layout(
#         height=450,
#         hovermode="x unified",
#         plot_bgcolor="white",
#         paper_bgcolor="white",
#         margin=dict(l=60, r=30, t=40, b=60),
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1.02,
#             xanchor="center",
#             x=0.5,
#             bgcolor="rgba(255,255,255,0.8)",
#             bordercolor="#E2E8F0",
#             borderwidth=1,
#         ),
#         xaxis=dict(showgrid=False),
#         yaxis=dict(showgrid=True, gridcolor="#E2E8F0"),
#     )

#     st.plotly_chart(fig_city, use_container_width=True)

#     # Statistics
#     st.markdown("#### 📈 Statistical Summary (PM2.5)")

#     stat1, stat2, stat3, stat4, stat5 = st.columns(5)

#     with stat1:
#         st.metric("AVG PM2.5", f"{df_city['PM25'].mean():.1f}")
#     with stat2:
#         st.metric("MAX PM2.5", f"{df_city['PM25'].max():.1f}")
#     with stat3:
#         st.metric("MIN PM2.5", f"{df_city['PM25'].min():.1f}")
#     with stat4:
#         st.metric("STD DEV", f"{df_city['PM25'].std():.1f}")
#     with stat5:
#         st.metric("UNHEALTHY %", f"{(df_city['PM25'] > 75).mean() * 100:.1f}%")

#     st.markdown("---")

#     # Map Section
#     st.markdown("### 🗺️ Geographic Distribution")

#     latest_data = df_all.sort_values("Timestamp").groupby("city").tail(1)
#     latest_data["Alert_Level"] = latest_data["PM25"].apply(_compute_alert_level)
#     latest_data["lat"] = latest_data["city"].map(lambda c: CITY_COORDS[c][0])
#     latest_data["lon"] = latest_data["city"].map(lambda c: CITY_COORDS[c][1])
#     latest_data["PM25_size"] = latest_data["PM25"].clip(lower=1)
#     latest_data["city_display"] = latest_data["city"].map(CITY_DISPLAY)

#     st.markdown("#### 📋 Current Status Table")

#     display_df = latest_data[
#         ["city_display", "Timestamp", "PM25", "NO2", "CO_Level", "Alert_Level"]
#     ].rename(
#         columns={
#             "city_display": "City",
#             "PM25": "PM2.5 (µg/m³)",
#             "NO2": "NO₂ (ppb)",
#             "CO_Level": "CO (ppm)",
#             "Alert_Level": "Status",
#         }
#     )

#     st.dataframe(display_df, use_container_width=True, height=220)

#     st.markdown("#### 🌍 Interactive Map")

#     fig_map = px.scatter_mapbox(
#         latest_data,
#         lat="lat",
#         lon="lon",
#         size="PM25_size",
#         color="PM25",
#         hover_name="city_display",
#         hover_data={
#             "Timestamp": True,
#             "PM25": ":.1f",
#             "NO2": ":.1f",
#             "CO_Level": ":.2f",
#             "Alert_Level": True,
#             "PM25_size": False,
#             "lat": False,
#             "lon": False,
#         },
#         color_continuous_scale=[[0, "#00C896"], [0.4, "#FFA502"], [1, "#FF4757"]],
#         zoom=4.8,
#         height=580,
#         mapbox_style="carto-positron",
#     )

#     fig_map.update_layout(
#         margin={"r": 0, "t": 0, "l": 0, "b": 0},
#         coloraxis_colorbar=dict(
#             title=dict(text="PM2.5 (µg/m³)", font=dict(size=12)), thickness=18, len=0.75
#         ),
#     )

#     st.plotly_chart(fig_map, use_container_width=True)

#     st.markdown("---")

#     # Control Panel
#     st.markdown("### 🎛️ Command Center Controls")

#     ctrl1, ctrl2, ctrl3, ctrl4 = st.columns(4)

#     with ctrl1:
#         if st.button(f"{FA_ICON_REFRESH} Refresh Data", use_container_width=True):
#             st.cache_data.clear()
#             st.success("✅ Data refreshed")
#             st.rerun()

#     with ctrl2:
#         st.download_button(
#             "📥 Export CSV",
#             latest_data.to_csv(index=False),
#             file_name=f"report_{datetime.now().strftime('%Y%m%d')}.csv",
#             mime="text/csv",
#             use_container_width=True,
#         )

#     with ctrl3:
#         st.download_button(
#             "📥 Export JSON",
#             latest_data.to_json(orient="records", indent=2),
#             file_name=f"report_{datetime.now().strftime('%Y%m%d')}.json",
#             mime="application/json",
#             use_container_width=True,
#         )

#     with ctrl4:
#         show_summary = st.button("📄 System Summary", use_container_width=True)

#     if show_summary:
#         st.markdown(
#             f"""
#             <div style='background: white; padding: 2rem; border-radius: 14px;
#                         border: 2px solid #0066FF; margin-top: 1.5rem;
#                         box-shadow: 0 4px 16px rgba(0, 102, 255, 0.1);'>
#                 <h4 style='color: #1A202C; margin: 0 0 1.25rem 0; font-size: 1.5rem; font-weight: 700;'>
#                     📊 System Monitoring Summary
#                 </h4>
#                 <p style='color: #4A5568; margin: 0; line-height: 2; font-size: 1.05rem;'>
#                     <b>Cities Monitored:</b> {total_cities}<br>
#                     <b>Total Records:</b> {total_records:,}<br>
#                     <b>Average PM2.5:</b> {avg_pm25:.1f} µg/m³<br>
#                     <b>Unhealthy Cities:</b> {high_risk}/{total_cities}
#                 </p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         summary_text = (
#             f"System Monitoring Summary\n"
#             f"========================\n"
#             f"Cities Monitored: {total_cities}\n"
#             f"Total Records: {total_records:,}\n"
#             f"Average PM2.5: {avg_pm25:.1f} µg/m³\n"
#             f"Unhealthy Cities: {high_risk}/{total_cities}\n"
#             f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
#         )

#         st.download_button(
#             "⬇️ Download Summary Report",
#             summary_text,
#             file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#             mime="text/plain",
#             use_container_width=True,
#         )

#     st.markdown("---")
#     st.info(
#         "💡 **System Note**: Dashboard uses FontAwesome icons for a professional look. Real-time data visualization is achieved with Plotly."
#     )
import pathlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from datetime import datetime, timedelta

DATA_HOSPITAL_DIR = pathlib.Path("data/processed/merged_hospitals")

CITY_COORDS = {
    "lahore": (31.5204, 74.3587),
    "karachi": (24.8607, 67.0011),
    "islamabad": (33.6844, 73.0479),
    "peshawar": (34.0151, 71.5249),
    "quetta": (30.1798, 66.9750),
}

CITY_FILE_MAP = {
    "lahore": "client_merged_S2.csv",
    "karachi": "client_merged_S3.csv",
    "islamabad": "client_merged_S4.csv",
    "peshawar": "client_merged_S5.csv",
    "quetta": "client_merged_S9.csv",
}

CITY_DISPLAY = {
    "lahore": "Lahore",
    "karachi": "Karachi",
    "islamabad": "Islamabad",
    "peshawar": "Peshawar",
    "quetta": "Quetta",
}


def _compute_alert_level(pm25: float) -> str:
    if pd.isna(pm25):
        return "Unknown"
    if pm25 < 35:
        return "Good"
    if pm25 < 75:
        return "Moderate"
    if pm25 < 150:
        return "Unhealthy"
    return "Hazardous"


@st.cache_data
def load_hospital_data() -> pd.DataFrame:
    dfs = []
    for city, file in CITY_FILE_MAP.items():
        fpath = DATA_HOSPITAL_DIR / file
        if not fpath.exists():
            continue
        df = pd.read_csv(fpath)
        expected_cols = {"Timestamp", "PM25", "NO2", "CO_Level"}
        if expected_cols - set(df.columns):
            continue
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        for col in ["PM25", "NO2", "CO_Level"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").clip(lower=0)
        df["city"] = city
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def render_admin_dashboard() -> None:
    st.cache_data.clear()

    # Modern Hero Section
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #1E3A8A 0%, #1E293B 100%); 
                    padding: 2.5rem 2rem; border-radius: 14px; margin-bottom: 2rem;
                    box-shadow: 0 8px 24px rgba(30, 58, 138, 0.3);'>
            <div style='text-align: center;'>
                <div style='font-size: 3.5rem; margin-bottom: 0.75rem;'>🏛️</div>
                <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 800;'>
                    Health Authority Command Center
                </h2>
                <p style='color: rgba(255,255,255,0.95); margin-top: 0.5rem; font-size: 1.05rem;'>
                    Real-time environmental health monitoring and population risk assessment
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df_all = load_hospital_data()
    if df_all.empty:
        st.error("❌ No monitoring data available. Check data directory.")
        return

    # System Overview
    st.markdown("### 📊 System Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    total_cities = df_all["city"].nunique()
    total_records = len(df_all)
    avg_pm25 = df_all["PM25"].mean()
    high_risk = (df_all.groupby("city")["PM25"].mean() > 75).sum()
    latest = df_all["Timestamp"].max()

    with col1:
        st.metric("🌍 CITIES", total_cities, "Active")
    with col2:
        st.metric("📊 RECORDS", f"{total_records:,}", "Total")
    with col3:
        st.metric("🌫️ AVG PM2.5", f"{avg_pm25:.1f}", "µg/m³")
    with col4:
        st.metric("⚠️ HIGH RISK", f"{high_risk}/{total_cities}", "Cities")
    with col5:
        st.metric(
            "🕐 LAST UPDATE",
            latest.strftime("%H:%M") if pd.notna(latest) else "N/A",
        )

    st.markdown("---")

    # Comparison Section
    st.markdown("### 🏙️ Inter-City Analysis")

    comp_col1, comp_col2 = st.columns([3, 1])

    with comp_col1:
        metric = st.selectbox(
            "Environmental Parameter:",
            ["PM2.5 Concentration", "NO₂ Levels", "CO Levels"],
        )
    with comp_col2:
        sort_order = st.selectbox("Sort:", ["Highest First", "Lowest First"])

    metric_map = {
        "PM2.5 Concentration": "PM25",
        "NO₂ Levels": "NO2",
        "CO Levels": "CO_Level",
    }
    selected = metric_map[metric]

    city_avg = df_all.groupby("city")[selected].mean().reset_index()
    city_avg["city_display"] = city_avg["city"].map(CITY_DISPLAY)
    city_avg = city_avg.sort_values(selected, ascending=(sort_order == "Lowest First"))

    # Modern bar chart
    fig = go.Figure()

    colors = ["#0066FF", "#1E3A8A", "#10B981", "#F59E0B", "#EF4444"][: len(city_avg)]

    fig.add_trace(
        go.Bar(
            x=city_avg["city_display"],
            y=city_avg[selected],
            marker=dict(color=colors, line=dict(color="white", width=2)),
            text=[f"{v:.1f}" for v in city_avg[selected]],
            textposition="outside",
            textfont=dict(size=13, color="#1F2937", weight="bold"),
            hovertemplate="<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text=f"{metric} Comparison Across Cities",
            font=dict(size=18, weight="bold", color="#1F2937"),
        ),
        xaxis_title="",
        yaxis_title=metric,
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=60, r=30, t=60, b=60),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # City Detail Section
    st.markdown("### 🔬 City-Level Analysis")

    detail_col1, detail_col2, detail_col3 = st.columns([2, 1, 1])

    with detail_col1:
        cities = sorted(df_all["city"].unique())
        selected_city = st.selectbox(
            "Select City:", cities, format_func=lambda x: CITY_DISPLAY.get(x, x)
        )

    with detail_col2:
        time_range = st.selectbox(
            "Time Period:",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Data"],
            index=1,
        )

    with detail_col3:
        chart_style = st.selectbox(
            "Chart Style:", ["Multi-Line", "Area", "Scatter"], index=0
        )

    df_city = df_all[df_all["city"] == selected_city].sort_values("Timestamp")

    # Time filtering
    if time_range != "All Data":
        latest_time = df_city["Timestamp"].max()
        delta_map = {"Last 24 Hours": 1, "Last 7 Days": 7, "Last 30 Days": 30}
        df_city = df_city[
            df_city["Timestamp"] >= latest_time - timedelta(days=delta_map[time_range])
        ]

    if df_city.empty:
        st.warning(
            f"⚠️ No data available for {CITY_DISPLAY[selected_city]} in the selected time range."
        )
        return

    st.markdown(f"#### Environmental Trends: {CITY_DISPLAY[selected_city]}")

    # Create chart
    if chart_style == "Multi-Line":
        fig_city = go.Figure()

        fig_city.add_trace(
            go.Scatter(
                x=df_city["Timestamp"],
                y=df_city["PM25"],
                name="PM2.5",
                line=dict(color="#EF4444", width=3),
                mode="lines",
                fill="tozeroy",
                fillcolor="rgba(239, 68, 68, 0.1)",
            )
        )

        fig_city.add_trace(
            go.Scatter(
                x=df_city["Timestamp"],
                y=df_city["NO2"],
                name="NO₂",
                line=dict(color="#0066FF", width=3),
                mode="lines",
                fill="tozeroy",
                fillcolor="rgba(0, 102, 255, 0.1)",
            )
        )

        fig_city.add_trace(
            go.Scatter(
                x=df_city["Timestamp"],
                y=df_city["CO_Level"] * 10,
                name="CO (×10)",
                line=dict(color="#10B981", width=3),
                mode="lines",
                fill="tozeroy",
                fillcolor="rgba(16, 185, 129, 0.1)",
            )
        )

    elif chart_style == "Area":
        fig_city = go.Figure()
        fig_city.add_trace(
            go.Scatter(
                x=df_city["Timestamp"],
                y=df_city["PM25"],
                fill="tozeroy",
                name="PM2.5",
                line=dict(color="#0066FF", width=2),
                fillcolor="rgba(0, 102, 255, 0.2)",
            )
        )
    else:
        fig_city = px.scatter(
            df_city,
            x="Timestamp",
            y="PM25",
            color="PM25",
            size=np.abs(df_city["PM25"]) + 0.1,
            color_continuous_scale=[[0, "#10B981"], [0.5, "#F59E0B"], [1, "#EF4444"]],
        )

    fig_city.update_layout(
        height=450,
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=60, r=30, t=40, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E5E7EB",
            borderwidth=1,
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
    )

    st.plotly_chart(fig_city, use_container_width=True)

    # Statistics
    st.markdown("#### 📈 Statistical Summary")

    stat1, stat2, stat3, stat4, stat5 = st.columns(5)

    with stat1:
        st.metric("AVG PM2.5", f"{df_city['PM25'].mean():.1f}")
    with stat2:
        st.metric("MAX PM2.5", f"{df_city['PM25'].max():.1f}")
    with stat3:
        st.metric("MIN PM2.5", f"{df_city['PM25'].min():.1f}")
    with stat4:
        st.metric("STD DEV", f"{df_city['PM25'].std():.1f}")
    with stat5:
        st.metric("HIGH RISK %", f"{(df_city['PM25'] > 75).mean() * 100:.1f}%")

    st.markdown("---")

    # Map Section
    st.markdown("### 🗺️ Geographic Distribution")

    # FIXED LATEST ROW BUG → USING idxmax() for TRUE latest record
    df_clean = df_all[df_all["Timestamp"].notna()]
    latest_data = df_clean.loc[
        df_clean.groupby("city")["Timestamp"].idxmax()
    ].reset_index(drop=True)

    latest_data["Alert_Level"] = latest_data["PM25"].apply(_compute_alert_level)
    latest_data["lat"] = latest_data["city"].map(lambda c: CITY_COORDS[c][0])
    latest_data["lon"] = latest_data["city"].map(lambda c: CITY_COORDS[c][1])
    latest_data["PM25_size"] = latest_data["PM25"].clip(lower=1)
    latest_data["city_display"] = latest_data["city"].map(CITY_DISPLAY)

    st.markdown("#### 📋 Current Status Table")

    display_df = latest_data[
        ["city_display", "Timestamp", "PM25", "NO2", "CO_Level", "Alert_Level"]
    ].rename(
        columns={
            "city_display": "City",
            "PM25": "PM2.5 (µg/m³)",
            "NO2": "NO₂ (ppb)",
            "CO_Level": "CO (ppm)",
            "Alert_Level": "Status",
        }
    )

    st.dataframe(display_df, use_container_width=True, height=220)

    st.markdown("#### 🌍 Interactive Map")

    fig_map = px.scatter_mapbox(
        latest_data,
        lat="lat",
        lon="lon",
        size="PM25_size",
        color="PM25",
        hover_name="city_display",
        hover_data={
            "Timestamp": True,
            "PM25": ":.1f",
            "NO2": ":.1f",
            "CO_Level": ":.2f",
            "Alert_Level": True,
            "PM25_size": False,
            "lat": False,
            "lon": False,
        },
        color_continuous_scale=[[0, "#10B981"], [0.4, "#F59E0B"], [1, "#EF4444"]],
        zoom=4.8,
        height=580,
        mapbox_style="carto-positron",
    )

    fig_map.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title=dict(text="PM2.5 (µg/m³)", font=dict(size=12)),
            thickness=18,
            len=0.75,
        ),
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    # Control Panel
    st.markdown("### 🎛️ Command Center Controls")

    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns(4)

    with ctrl1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Data refreshed")
            st.rerun()

    with ctrl2:
        st.download_button(
            "📥 Export CSV",
            latest_data.to_csv(index=False),
            file_name=f"report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with ctrl3:
        st.download_button(
            "📥 Export JSON",
            latest_data.to_json(orient="records", indent=2),
            file_name=f"report_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True,
        )

    with ctrl4:
        show_summary = st.button("📄 System Summary", use_container_width=True)

    if show_summary:
        st.markdown(
            f"""
            <div style='background: white; padding: 2rem; border-radius: 14px; 
                        border: 2px solid #0066FF; margin-top: 1.5rem;
                        box-shadow: 0 4px 16px rgba(0, 102, 255, 0.1);'>
                <h4 style='color: #1F2937; margin: 0 0 1.25rem 0; font-size: 1.5rem; font-weight: 700;'>
                    📊 System Monitoring Summary
                </h4>
                <p style='color: #374151; margin: 0; line-height: 2; font-size: 1.05rem;'>
                    <b>Cities Monitored:</b> {total_cities}<br>
                    <b>Total Records:</b> {total_records:,}<br>
                    <b>Average PM2.5:</b> {avg_pm25:.1f} µg/m³<br>
                    <b>High-Risk Cities:</b> {high_risk}/{total_cities}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        summary_text = (
            f"System Monitoring Summary\n"
            f"========================\n"
            f"Cities Monitored: {total_cities}\n"
            f"Total Records: {total_records:,}\n"
            f"Average PM2.5: {avg_pm25:.1f} µg/m³\n"
            f"High-Risk Cities: {high_risk}/{total_cities}\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        st.download_button(
            "⬇️ Download Summary Report",
            summary_text,
            file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("---")
    st.info(
        "💡 **System Note**: Real-time data visualization with professional charts and analytics."
    )
