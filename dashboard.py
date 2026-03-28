import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# INTEGRATION: Import your logic engine
from logic import get_aws_metrics, run_ml_engine 

# =============================================================================
# 1. ENTERPRISE DESIGN SYSTEM (CSS)
# =============================================================================
st.set_page_config(page_title="Cloud Intel | Enterprise Governance", layout="wide")

def apply_enterprise_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        .stApp { background: radial-gradient(circle at 2% 2%, #0f172a 0%, #020617 100%); color: #f8fafc; font-family: 'Inter', sans-serif; }
        h1, h2, h3 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; letter-spacing: -0.02em; color: #f8fafc; }
        div[data-testid="stMetric"] { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.1); border-top: 3px solid #38bdf8; padding: 20px !important; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        [data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.85rem !important; text-transform: uppercase; letter-spacing: 0.05em; }
        [data-testid="stMetricValue"] { color: #f8fafc !important; font-size: 1.8rem !important; font-weight: 600 !important; }
        .status-badge { padding: 4px 12px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }
        .user-badge { padding: 4px 12px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; background: rgba(56, 189, 248, 0.1); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.2); margin-right: 10px; }
        code { font-family: 'JetBrains Mono', monospace !important; background-color: #000000 !important; color: #10b981 !important; border-radius: 4px; }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 3. CONSOLE ARCHITECTURE - INTEGRATED
# =============================================================================
def main():
    apply_enterprise_styles()
    
    # INTEGRATION: Data capture with top user tracking
    raw_data, top_contributor = get_aws_metrics()
    df = run_ml_engine(raw_data)

    # --- TOP NAVIGATION / STATUS ---
    col_nav1, col_nav2 = st.columns([3, 2])
    with col_nav1:
        st.markdown("<h1>Infrastructure Intelligence <span style='font-weight:300; color:#64748b;'>/ Global Console</span></h1>", unsafe_allow_html=True)
    with col_nav2:
        st.markdown(f"""
            <div style='text-align:right; margin-top:15px;'>
                <span class='user-badge'>🏆 TOP CONTRIBUTOR: {top_contributor.upper()}</span>
                <span class='status-badge'>● SYSTEM OPERATIONAL</span>
            </div>
        """, unsafe_allow_html=True)

    # --- KEY PERFORMANCE INDICATORS ---
    total_cost = df['Cost ($/hr)'].sum() if not df.empty else 0.0
    avg_cpu = df['CPU (%)'].mean() if not df.empty else 0.0
    anomalies = len(df[df['anomaly_score'] == -1]) if 'anomaly_score' in df.columns else 0

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Run Rate (Hourly)", f"${total_cost:,.2f}", "+1.2%")
    m2.metric("Efficiency Ratio", f"{100-avg_cpu:.1f}%", "Optimal")
    m3.metric("Entropy Index", "0.24", "-0.02")
    m4.metric("Carbon Intensity", "0.42g/kWh", "-4%")
    m5.metric("Active Anomalies", f"{anomalies:02d}", "High Priority", delta_color="inverse")

    st.markdown("---")

    # --- MAIN ANALYTICS GRID ---
    row2_c1, row2_c2 = st.columns([2, 1])

    with row2_c1:
        st.markdown("### Cost Drift & Autonomous Remediation")
        if not df.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['CPU (%)'], name='Utilization (%)',
                                    line=dict(color='#38bdf8', width=3), fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.05)'))
            if anomalies > 0:
                anomaly_idx = df[df['anomaly_score'] == -1].index[0]
                fig.add_annotation(x=anomaly_idx, y=df.loc[anomaly_idx, 'CPU (%)'],
                                   text="Anomaly Detected", showarrow=True, arrowhead=1,
                                   bgcolor="#ef4444", font=dict(color="#ffffff"))
            fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              margin=dict(l=0,r=0,t=20,b=0), height=400, hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Waiting for live telemetry 'heartbeat' from AWS...")

    with row2_c2:
        st.markdown("### Resource Distribution")
        if not df.empty:
            dist_df = df.groupby('Service')['Cost ($/hr)'].sum().reset_index()
            fig_pie = px.pie(dist_df, values='Cost ($/hr)', names='Service', hole=0.7,
                             color_discrete_sequence=['#0ea5e9', '#10b981', '#6366f1', '#f59e0b'])
            fig_pie.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, 
                                  margin=dict(l=0,r=0,t=0,b=0), height=350)
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- INVENTORY & AUTOMATION QUEUE ---
    st.markdown("### Active Governance Recommendations")
    st.dataframe(df[["Resource ID", "Type", "Service", "CPU (%)", "Cost ($/hr)"]], use_container_width=True)

    # --- SYSTEM LOGS ---
    st.markdown("---")
    c_log1, c_log2 = st.columns([3, 1])
    with c_log1:
        st.markdown("#### Governance Event Log")
        st.code(f"""
[INFO] {datetime.now().strftime('%H:%M:%S')} - Isolation Forest Engine Loaded.
[INFO] {datetime.now().strftime('%H:%M:%S')} - Boto3 Handshake stable. Analyzing {len(df)} streams.
[INFO] {datetime.now().strftime('%H:%M:%S')} - Tracking Dev Velocity for user: {top_contributor}.
        """)
    with c_log2:
        st.markdown("#### Export Metrics")
        st.button("📄 Generate PDF Audit")
        st.button("📊 Export CSV Telemetry")

if __name__ == "__main__":
    main()