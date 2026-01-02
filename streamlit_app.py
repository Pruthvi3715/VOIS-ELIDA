import streamlit as st
import requests
import pandas as pd
import json
import re

# Page Config
st.set_page_config(
    page_title="ELIDA | AI Financial Assistant",
    page_icon="🧠",
    layout="wide"
)

# Backend URL
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
dev_mode = True # Default to True for visibility, sidebar can toggle it off if needed (but currently we want it ON)

# Styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2563eb;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- UI Helper Functions ---

def get_color(score, inverse=False):
    """Return color based on score (0-100)."""
    if inverse:
        return "#ef5350" if score > 70 else "#f59e0b" if score > 40 else "#10b981"
    return "#10b981" if score > 70 else "#f59e0b" if score > 40 else "#ef5350"

def render_verdict(match_data):
    """Render the top-level Verdict section."""
    score = match_data.get("score", 0)
    rec = match_data.get("recommendation", "N/A")
    risk = match_data.get("risk_assessment", {}).get("risk_level", "Medium")
    
    # Dynamic styling
    score_color = get_color(score)
    rec_color = "#10b981" if rec.upper() == "BUY" else "#ef5350" if rec.upper() == "AVOID" else "#f59e0b"
    
    # Layout
    c1, c2, c3 = st.columns([1, 1, 2])
    
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:0.9em; color:#6b7280; margin-bottom: 5px;">Match Score</div>
            <div style="font-size:3.5em; font-weight:800; color:{score_color}; line-height:1;">{score}</div>
            <div style="font-size:0.8em; color:#6b7280;">out of 100</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:0.9em; color:#6b7280; margin-bottom: 5px;">Verdict</div>
            <div style="font-size:1.8em; font-weight:700; color:{rec_color};">{rec.upper()}</div>
            <div style="margin-top:10px; font-size:0.9em; color:#6b7280;">Risk: <b>{risk}</b></div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        # Generate a synthetic summary if one isn't provided
        summary = match_data.get("summary", 
            f"This asset aligns { 'well' if score > 70 else 'poorly' if score < 40 else 'moderately'} with your profile. "
            f"The primary driver is {rec.lower()} signals from the analysis agents."
        )
        st.markdown(f"""
        <div class="metric-card" style="text-align:left; height:100%;">
            <div style="font-size:0.9em; color:#6b7280; margin-bottom: 5px;">Executive Summary</div>
            <div style="font-size:1.1em; color:#374151; line-height:1.5;">{summary}</div>
        </div>
        """, unsafe_allow_html=True)

def render_agent_card(agent_name, agent_data, collapsed=True, show_raw=False):
    """Render a clean card for an agent's analysis."""
    # Extract data gracefully
    if isinstance(agent_data, dict):
        score = agent_data.get("score") or agent_data.get("risk_score") or 0
        analysis = agent_data.get("analysis", "")
        # If output is nested
        if "output" in agent_data and isinstance(agent_data["output"], dict):
             details = agent_data["output"]
             analysis = details.get("analysis", analysis)
             score = details.get("score", score)
        else:
             details = agent_data
             
    else:
        score = 0
        analysis = str(agent_data)
        details = {}

    # Determine Status
    status_color = get_color(score) # Default logic
    status_icon = "✅" if score > 70 else "⚠️" if score > 40 else "❌"
    
    # Auto-expand if show_raw is True
    is_expanded = (not collapsed) or show_raw
    
    # Header
    with st.expander(f"{status_icon} **{agent_name}**  (Score: {score})", expanded=is_expanded):
        # 1. Takeaway (First sentence of analysis)
        if analysis:
            takeaway = analysis.split('.')[0] + "."
            st.info(f"**Takeaway:** {takeaway}")

        # --- NEW: Structured Data Visualization ---
        
        # A. Quant Agent (Financial Metrics)
        if "metrics_values" in details and details["metrics_values"]:
            st.markdown("###### 📊 Key Financial Metrics")
            m_cols = st.columns(4)
            for i, (k, v) in enumerate(details["metrics_values"].items()):
                label = k.replace("_", " ").title().replace("Pe", "P/E").replace("Peg", "PEG")
                val_str = f"{v:.2f}" if isinstance(v, float) else str(v)
                if "margin" in k or "return" in k or "growth" in k:
                    val_str = f"{v*100:.1f}%" if v < 1 else f"{v}%"
                with m_cols[i % 4]:
                    st.metric(label, val_str)
            st.markdown("---")

        # B. Macro Agent (Indicators Table)
        if "indicators_analyzed" in details and details["indicators_analyzed"]:
            st.markdown("###### 🌍 Macro Indicators")
            # Create cleaner DF for display
            try:
                df = pd.DataFrame(details["indicators_analyzed"])
                if not df.empty:
                    disp_df = df.rename(columns={"name": "Indicator", "value": "Current", "signal": "Signal", "impact": "Market Impact"})
                    # Reorder if columns exist
                    cols_to_show = [c for c in ["Indicator", "Current", "Signal", "Market Impact"] if c in disp_df.columns]
                    st.dataframe(disp_df[cols_to_show], use_container_width=True, hide_index=True)
            except:
                pass

        # C. Regret Agent (Scenarios Table)
        if "scenarios" in details and details["scenarios"]:
            st.markdown("###### 🌩️ Tail Risk Scenarios")
            try:
                df = pd.DataFrame(details["scenarios"])
                if not df.empty:
                    disp_df = df.rename(columns={"name": "Scenario", "probability": "Prob", "estimated_drawdown": "Est. Drawdown", "impact": "Impact"})
                    cols_to_show = [c for c in ["Scenario", "Prob", "Est. Drawdown", "Impact"] if c in disp_df.columns]
                    st.dataframe(disp_df[cols_to_show], use_container_width=True, hide_index=True)
            except:
                pass
            
            # Show Max Drawdown as big number
            if "max_drawdown_estimate" in details:
                st.metric("Expected Worst Case Drawdown", details["max_drawdown_estimate"], delta="-Risk", delta_color="inverse")
            st.markdown("---")

        # --- End Structured Data ---
        
        # 2. Structured Details (Strengths/Weaknesses)
        cols = st.columns(2)
        with cols[0]:
            if "strengths" in details and isinstance(details["strengths"], list):
                st.markdown("**✅ Strengths**")
                for item in details["strengths"]:
                    st.markdown(f"- {item}")
            elif "pros" in details:
                 st.markdown("**✅ Pros**")
                 st.write(details["pros"])

        with cols[1]:
            if "weaknesses" in details and isinstance(details["weaknesses"], list):
                st.markdown("**❌ Risks/Weaknesses**")
                for item in details["weaknesses"]:
                    st.markdown(f"- {item}")
            elif "cons" in details:
                 st.markdown("**❌ Cons**")
                 st.write(details["cons"])
        
        # 3. Full Analysis Text (Always show if available)
        if analysis:
             st.markdown("**📝 Full Analysis**")
             st.write(analysis)
        
        # 4. Raw Data Toggle
        if show_raw or st.checkbox(f"Show Raw JSON ({agent_name})", key=f"raw_{agent_name}", value=show_raw):
            st.json(agent_data)


# --- End Helpers ---

# --- Sidebar: Developer Mode & Profile Settings ---
with st.sidebar:
    # Developer Mode Toggle
    if "dev_mode" not in st.session_state:
        st.session_state.dev_mode = True  # Default ON
    
    st.session_state.dev_mode = st.toggle("🛠️ Developer Mode", value=st.session_state.dev_mode)
    dev_mode = st.session_state.dev_mode  # Local alias for compatibility
    
    st.markdown("---")
    st.markdown("### 🧬 Investor DNA")
    
    # Check if profile exists
    try:
        profile_res = requests.get(f"{API_URL}/api/v1/profile/default_user")
        current_profile = profile_res.json() if profile_res.status_code == 200 else {}
    except:
        current_profile = {}
        st.error("Backend not connected")

    risk_tolerance = st.slider("Risk Tolerance", 1, 10, int(current_profile.get("risk_tolerance", 5)))
    time_horizon = st.selectbox("Time Horizon", ["Short Term", "Medium Term", "Long Term"], 
                                index=["Short Term", "Medium Term", "Long Term"].index(current_profile.get("investment_horizon", "Medium Term")))
    
    custom_rules_input = st.text_area("Custom Rules (one per line)", 
                                      value="\n".join(current_profile.get("custom_rules", [])))
    
    if st.button("Update Profile"):
        payload = {
            "user_id": "default_user",
            "risk_tolerance": risk_tolerance,
            "investment_horizon": time_horizon,
            "custom_rules": [r.strip() for r in custom_rules_input.split("\n") if r.strip()],
            "goals": ["Growth", "Stability"] 
        }
        requests.post(f"{API_URL}/api/v1/profile", json=payload)
        st.success("Profile Updated!")

# --- Navigation ---
mode = st.sidebar.selectbox("Navigation", ["🔍 Analysis", "💼 Portfolio Scanner", "📜 History"])
st.sidebar.markdown("---")

# --- Intent Classification Logic ---

def normalize_query(query):
    """Normalize query for classification."""
    return query.strip().lower()

def classify_intent(query):
    """
    Deterministically classify intent into 'COMPANY' or 'TERM_SEARCH'.
    """
    normalized = normalize_query(query)
    
    # 1. Ticker Pattern (Strongest Signal)
    if re.match(r'^\$?[A-Z0-9]{1,6}(\.[A-Z]{2,3})?$', query.strip().upper()):
        return "COMPANY"

    # 2. explicit Company Keywords
    company_keywords = [
        "company", "startup", "brand", "stock", "share", "shares",
        "ceo", "revenue", "valuation", "market cap", "ipo", "earnings",
        "dividend", "price", "chart", "analyze", "analysis", "forecast", "target"
    ]
    if any(k in normalized for k in company_keywords):
        return "COMPANY"

    # 3. Legal Suffixes
    legal_suffixes = [" ltd", " inc", " corp", " llp", " plc", " pvt"]
    if any(s in normalized for s in legal_suffixes):
        return "COMPANY"

    # 4. Term Search Indicators
    term_indicators = ["what is", "define", "explain", "meaning of", "how to", "difference", "who is"]
    if any(normalized.startswith(t) for t in term_indicators):
        return "TERM_SEARCH"

    # 5. Fallback
    return "TERM_SEARCH"

# --- End Intent Classification ---

# --- MODE 1: ANALYSIS (Existing Logic) ---
if mode == "🔍 Analysis":
    # Main Header
    st.title("ELIDA")
    st.markdown("### AI-Powered Investment Decision Support")

    # Check if a history item was clicked (Session State)
    if "selected_query" in st.session_state and st.session_state.selected_query:
        default_q = st.session_state.selected_query
        st.session_state.selected_query = "" # Clear after using
    else:
        default_q = ""

    # Search Input
    query = st.text_input("Analyze a stock (e.g., TCS.NS) or ask a question...", value=default_q, placeholder="TCS.NS or 'What is EBITDA?'")

    # Routing Logic
    if query:
        intent = classify_intent(query)
        
        # --- PATH A: COMPANY PIPELINE ---
        if intent == "COMPANY":
            # Extract symbol
            symbol = None
            clean_q = query.strip().upper()
            
            # Regex Match
            match = re.match(r'^\$?([A-Z0-9]{1,6}(\.[A-Z]{2,3})?)$', clean_q)
            if match:
                symbol = match.group(1)
            else:
                # Flexible Match: Remove common words
                ignore_words = ["ANALYZE", "ANALYSIS", "STOCK", "SHARE", "SHARES", "PRICE", "CHART", "REPORT", "OF", "FOR", "LTD", "INC"]
                tokens = clean_q.split()
                filtered = [t for t in tokens if t not in ignore_words]
                if filtered:
                    candidate = filtered[0] # Take first valid token
                    if re.match(r'^[A-Z0-9]{1,6}(\.[A-Z]{2,3})?$', candidate):
                        symbol = candidate

            # If we found a valid symbol, proceed
            if symbol:
                # 1. Fast Path: Market Data & Charts
                st.subheader(f"📊 Analysis: {symbol}")
                
                market_placeholder = st.empty()
                market_data = {}
                with st.spinner(f"Fetching market data for {symbol}..."):
                     try:
                        m_res = requests.get(f"{API_URL}/market-data/{symbol}")
                        if m_res.status_code == 200:
                            market_data = m_res.json().get("technicals", {})
                        else:
                            st.warning("Could not fetch market data quickly. Proceeding to deep analysis...")
                     except Exception as e:
                         st.error(f"Market Data Error: {e}")
                
                # Charts
                if market_data:
                    import plotly.graph_objects as go
                    from plotly.subplots import make_subplots
                    with st.container():
                         chart_col1, chart_col2 = st.columns([2, 1])
                         with chart_col1:
                             st.markdown("##### 📈 Price History & Technicals")
                             history = market_data.get("history", [])
                             if history:
                                 df = pd.DataFrame(history)
                                 if not df.empty and 'Date' in df.columns:
                                     if all(c in df.columns for c in ['Open', 'High', 'Low', 'Close']):
                                         fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
                                         fig.add_trace(go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
                                         if 'Volume' in df.columns:
                                             colors = ['#26a69a' if c >= o else '#ef5350' for c, o in zip(df['Close'], df['Open'])]
                                             fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], marker_color=colors, name='Volume'), row=2, col=1)
                                         fig.update_layout(height=400, showlegend=False, xaxis_rangeslider_visible=False, template='plotly_white')
                                         st.plotly_chart(fig, use_container_width=True)
                         with chart_col2:
                             rsi = market_data.get("rsi_14")
                             if rsi:
                                 st.markdown("##### 📊 RSI Indicator")
                                 fig_rsi = go.Figure(go.Indicator(mode="gauge+number", value=rsi, domain={'x': [0, 1], 'y': [0, 1]}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': '#2563eb'}, 'steps': [{'range': [0, 30], 'color': '#dcfce7'}, {'range': [30, 70], 'color': '#fef9c3'}, {'range': [70, 100], 'color': '#fee2e2'}], 'threshold': {'line': {'color': 'red', 'width': 2}, 'thickness': 0.75, 'value': rsi}}))
                                 fig_rsi.update_layout(height=180, margin=dict(l=20, r=20, t=30, b=10))
                                 st.plotly_chart(fig_rsi, use_container_width=True)

                # 2. Slow Path: Full AI Analysis
                with st.spinner(f"Running AI Agents for {symbol} (This may take ~60s)..."):
                     try:
                        analyze_res = requests.get(f"{API_URL}/analyze/{symbol}")
                        analysis_data = analyze_res.json()
                        
                        if "match_result" in analysis_data:
                            render_verdict(analysis_data["match_result"])
                        
                        if "match_result" in analysis_data:
                            st.markdown("---")
                            st.markdown("##### 🧠 Deep Agent Analysis")
                            ac1, ac2 = st.columns([1, 2])
                            with ac1:
                                st.markdown("###### Score Pillars")
                                bd = analysis_data["match_result"].get("breakdown", {})
                                if bd:
                                    cats = ['Fundamental', 'Macro', 'Philosophy', 'Risk', 'DNA Match']
                                    vals = [bd.get('fundamental',50), bd.get('macro',50), bd.get('philosophy',50), bd.get('risk',50), bd.get('dna_match',50)]
                                    vals.append(vals[0]); cats.append(cats[0])
                                    fig_radar = go.Figure()
                                    fig_radar.add_trace(go.Scatterpolar(r=vals, theta=cats, fill='toself', fillcolor='rgba(37, 99, 235, 0.3)', line=dict(color='#2563eb', width=2)))
                                    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=300, margin=dict(l=40, r=40, t=20, b=20))
                                    st.plotly_chart(fig_radar, use_container_width=True)
                            with ac2:
                                st.success("Analysis Complete. Review the agent reports below for details.")
                        
                        st.markdown("##### Agent Reports")
                        res = analysis_data.get("results", {})
                        render_agent_card("Quant Agent (Fundamentals)", res.get("quant", {}), collapsed=False, show_raw=dev_mode)
                        render_agent_card("Macro Agent (Economics)", res.get("macro", {}), collapsed=False, show_raw=dev_mode)
                        render_agent_card("Philosopher Agent (Business Quality)", res.get("philosopher", {}), collapsed=False, show_raw=dev_mode)
                        render_agent_card("Regret Simulation (Risk)", res.get("regret", {}), collapsed=False, show_raw=dev_mode)

                     except Exception as e:
                        st.error(f"Analysis Failed: {e}")
                        if dev_mode: st.write(e)
            
            else:
                 # Intent is COMPANY but input is NOT a ticker (e.g. "Apple revenue")
                 # Fallback to Term Search for now as we lack Resolver
                 intent = "TERM_SEARCH"

        # --- PATH B: GEMINI SEARCH ---
        if intent == "TERM_SEARCH":
            st.subheader("📝 Intelligent Search")
            with st.spinner("Consulting knowledge base..."):
                try:
                    res = requests.post(f"{API_URL}/chat/general", json={"query": query})
                    if res.status_code == 200:
                        answer = res.json().get("response", "")
                        st.success("Search Complete")
                        with st.container():
                            st.markdown(answer)
                    else:
                        st.error("Could not retrieve info.")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# --- MODE 2: PORTFOLIO SCANNER ---
elif mode == "💼 Portfolio Scanner":
    st.title("💼 Portfolio Intelligence")
    st.markdown("Scan multiple assets simultaneously and get a consolidated verdict table.")
    
    tickers_input = st.text_area("Enter Tickers (comma separated)", placeholder="TCS.NS, RELIANCE.NS, INFY.NS, HDFCBANK.NS, TATAMOTORS.NS", height=100)
    
    if st.button("🚀 Scan Portfolio"):
        if not tickers_input:
            st.error("Please enter at least one ticker.")
        else:
            tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Initializing agents...")
            
            try:
                res = requests.post(f"{API_URL}/api/portfolio/scan", json={"user_id": "default_user", "tickers": tickers})
                if res.status_code == 200:
                    data = res.json().get("results", [])
                    st.success("Scan Complete!")
                    
                    # Convert to DataFrame
                    if data:
                        df = pd.DataFrame(data)
                        
                        # Apply Color Coding functions
                        def color_score(val):
                            color = '#ef5350' if val < 40 else '#f59e0b' if val < 70 else '#10b981'
                            return f'color: {color}'
                            
                        # Display
                        st.markdown("### 📊 Consolidated Verdicts")
                        st.dataframe(
                            df.style.map(color_score, subset=['score']),
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        st.markdown("---")
                        st.info("Tip: Go to 'Analysis' mode to deep dive into any specific asset.")
                        
                else:
                    st.error("Portfolio Scan Failed.")
            except Exception as e:
                st.error(f"Error: {e}")

# --- MODE 3: HISTORY ---
elif mode == "📜 History":
    st.title("📜 Research History")
    
    try:
        res = requests.get(f"{API_URL}/api/history/default_user")
        if res.status_code == 200:
            history_items = res.json()
            
            if not history_items:
                st.info("No history found yet. Start analyzing assets!")
            
            for item in history_items:
                # Card for history
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        icon = "📊" if item['type'] == 'analysis' else "📝"
                        st.markdown(f"**{icon} {item['query']}**")
                        st.caption(f"{item['type'].title()} • {item['timestamp'][:16].replace('T', ' ')}")
                    with col2:
                        # Re-Analyze Button (Loads into Analysis Mode)
                        if st.button("Open", key=item['id']):
                            st.session_state.selected_query = item['query']
                            # We can't switch mode programmatically easily in Streamlit sidebar nav, 
                            # but setting session state and asking user to switch is MVP.
                            # Or we force reload.
                            st.toast(f"Loaded '{item['query']}'. Switch to Analysis tab!")
                    st.markdown("---")
        else:
            st.error("Could not fetch history.")
    except Exception as e:
         st.error(f"Connection Error: {e}")

