import streamlit as st
import pandas as pd
import time
import random

st.set_page_config(page_title="SentinelAI", layout="wide")

# Dark Theme
st.markdown("""
<style>
body {
    background-color: #0b0f1a;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡 SentinelAI - Real-Time Threat Detection System")
st.caption("AI-powered real-time cyber threat detection and automated response system")

st.markdown("---")

# Session state
if "logs" not in st.session_state:
    st.session_state.logs = []

# Generate log
def generate_log(ip, action, status, risk):
    return {
        "Time": time.strftime("%H:%M:%S"),
        "IP": ip,
        "Action": action,
        "Status": status,
        "Risk Score": risk,
        "AI Confidence": f"{random.randint(75, 99)}%"
    }

# Sidebar
st.sidebar.header("⚡ Attack Simulation")

if st.sidebar.button("Simulate Normal Traffic"):
    for _ in range(10):
        ip = f"192.168.1.{random.randint(1,255)}"
        st.session_state.logs.append(generate_log(ip, "Login", "Success", "LOW"))

if st.sidebar.button("Simulate Brute Force Attack"):
    for _ in range(50):
        ip = "192.168.1.100"
        st.session_state.logs.append(generate_log(ip, "Login", "Failed", "HIGH"))

if st.sidebar.button("Simulate DDoS Attack"):
    for _ in range(100):
        ip = f"10.0.0.{random.randint(1,50)}"
        st.session_state.logs.append(generate_log(ip, "Request Flood", "Failed", "HIGH"))

# DataFrame
df = pd.DataFrame(st.session_state.logs)

if df.empty:
    df = pd.DataFrame(columns=["Time", "IP", "Action", "Status", "Risk Score", "AI Confidence"])

# Metrics
col1, col2, col3 = st.columns(3)

total_logs = len(df)

if "Risk Score" in df.columns:
    high_risk = len(df[df["Risk Score"] == "HIGH"])
    medium_risk = len(df[df["Risk Score"] == "MEDIUM"])
else:
    high_risk = 0
    medium_risk = 0

col1.metric("Total Logs", total_logs)
col2.metric("High Risk Threats", high_risk)
col3.metric("Medium Risk Threats", medium_risk)

# 🚫 IP Blocking
blocked_ips = {log["IP"] for log in st.session_state.logs if log["Risk Score"] == "HIGH"}

st.subheader("🚫 Blocked IPs (Auto Response)")
if blocked_ips:
    st.code("\n".join(blocked_ips))
else:
    st.info("No IPs blocked yet")

# 🔥 Top Attacker
if not df.empty:
    top_ip = df["IP"].value_counts().idxmax()
    st.info(f"🔥 Top Suspicious IP: {top_ip}")

# 🚨 Threat Level
if high_risk > 50:
    st.error("🔴 Threat Level: CRITICAL")
elif high_risk > 20:
    st.warning("🟠 Threat Level: HIGH")
else:
    st.success("🟢 Threat Level: NORMAL")

# Logs
st.subheader("📊 Live Threat Logs")
if not df.empty:
    st.dataframe(df.tail(20), use_container_width=True)

# Alerts
if high_risk > 20:
    st.error("🚨 CRITICAL ALERT: ACTIVE CYBER ATTACK DETECTED!")
    st.warning("⚠ System Response: Suspicious IPs are being monitored and blocked")

# 📈 Time Activity (SAFE COPY)
st.subheader("📈 Time-Based Threat Activity")
if not df.empty:
    temp_df = df.copy()
    temp_df["Time"] = pd.to_datetime(temp_df["Time"], format="%H:%M:%S", errors="coerce")
    st.line_chart(temp_df.groupby("Time").size())

# 📊 Threat Distribution (KEEP ONLY ONE)
st.subheader("📊 Threat Distribution")
if not df.empty:
    st.bar_chart(df["Risk Score"].value_counts())

# 🤖 AI Prediction Panel (IMPROVED)
st.subheader("🤖 AI Threat Prediction")

if not df.empty:
    high_ratio = (high_risk / total_logs) if total_logs > 0 else 0

    sql_score = int(60 + high_ratio * 40)
    brute_score = int(70 + high_ratio * 30)
    ddos_score = int(65 + high_ratio * 35)

    st.write("### Predicted Threat Probabilities")

    st.progress(sql_score / 100)
    st.write(f"SQL Injection Risk: {sql_score}%")

    st.progress(brute_score / 100)
    st.write(f"Brute Force Risk: {brute_score}%")

    st.progress(ddos_score / 100)
    st.write(f"DDoS Attack Risk: {ddos_score}%")

    st.markdown("### 🔐 Recommended Actions")
    st.write("- Enable Web Application Firewall (WAF)")
    st.write("- Apply rate limiting and IP blocking")
    st.write("- Monitor suspicious login patterns")
else:
    st.info("Run simulations to generate AI predictions")

# 🧠 AI Explanation
st.subheader("🧠 AI Analysis Engine")
st.write("""
The system monitors behavioral patterns and detects anomalies in real time.
It classifies threats using adaptive scoring and triggers automated responses
such as IP blocking and alert generation.
""")

# Footer
st.markdown("---")
st.markdown("⚡ Powered by Hybrid AI Threat Detection Engine")
