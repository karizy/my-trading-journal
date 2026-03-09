import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="ICT Trading Journal", page_icon="📈", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- APP TITLE ---
st.title("📈 ICT Master Journal")
st.write(f"Logged in as: **Funding Pips Trader** | Date: {datetime.now().strftime('%Y-%m-%d')}")

# --- SIDEBAR: ACCOUNT TRACKER ---
with st.sidebar:
    st.header("💰 Account Health")
    initial_cap = 10000.0
    # လက်ရှိ balance ကို ဒီမှာ update လုပ်ပါ
    current_bal = st.number_input("Current Balance ($)", value=9732.32, step=0.01)
    target_payout = 10200.0  # 2% Profit target
    
    # Calculations
    drawdown_amt = initial_cap - current_bal
    drawdown_pct = (drawdown_amt / initial_cap) * 100
    needed_for_payout = target_payout - current_bal
    
    st.divider()
    st.metric("Total Drawdown", f"-{drawdown_pct:.2f}%", f"-${drawdown_amt:.2f}", delta_color="inverse")
    st.metric("To Payout (2%)", f"${needed_for_payout:.2f}")
    
    # Progress Bar to Payout
    progress = max(0, min(100, int((current_bal / target_payout) * 100)))
    st.write(f"Progress to Payout: {progress}%")
    st.progress(progress)

# --- MAIN INTERFACE: TRADE LOGGING ---
st.subheader("📝 New Trade Entry")
with st.form("trade_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pair = st.selectbox("Pair", ["EURUSD", "GBPUSD", "XAUUSD", "AUDUSD", "USDJPY"])
        direction = st.radio("Direction", ["Long 🔵", "Short 🔴"])
        risk_pct = st.select_slider("Risk (%)", options=[0.25, 0.5, 0.75, 1.0], value=0.5)

    with col2:
        st.write("**ICT Confluences**")
        c1 = st.checkbox("4H FVG / PD Array Tap")
        c2 = st.checkbox("15m MSS (Structure Shift)")
        c3 = st.checkbox("Liquidity Sweep (SSL/BSL)")
        entry_type = st.selectbox("Entry Logic", ["Normal Entry", "Sharp Turn Entry"])

    with col3:
        rr_target = st.number_input("Target RR (e.g. 2.5)", value=2.0, step=0.1)
        potential_win = (current_bal * (risk_pct/100)) * rr_target
        st.info(f"Potential Profit: ${potential_win:.2f}")

    notes = st.text_area("Trading Narrative / Psychology")
    
    submitted = st.form_submit_submit_button("Save Trade to Journal")
    if submitted:
        if c1 and c2:
            st.success(f"✅ Trade on {pair} saved! You followed your rules. Good job!")
        else:
            st.warning("⚠️ Rules not fully met. Remember: 4H FVG + 15m MSS is your edge.")

# --- RULES REMINDER ---
st.divider()
st.subheader("📌 Trading Rules Checklist")
col_a, col_b = st.columns(2)
with col_a:
    st.info("""
    **Before Entry:**
    1. Identify 4H FVG (HTF Context).
    2. Wait for price to tap the FVG.
    3. Drop to 15m for MSS.
    """)
with col_b:
    st.warning("""
    **Risk Management:**
    - Max Risk: 1% (As per your plan).
    - Goal: 10R to reach 2% Payout.
    - Don't Revenge Trade!
    """)
