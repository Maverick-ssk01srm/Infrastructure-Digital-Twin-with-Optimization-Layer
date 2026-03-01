import streamlit as st
import pandas as pd
import numpy as np
import time
from streamlit_option_menu import option_menu
from optimizer import Optimizer
from visualizer import Visualizer
from alerts import AlertSystem
from timetable_parser import TimetableParser

st.set_page_config(
    page_title="TwinFlow Pro | Campus Digital Twin",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

.stApp {
    background: #09090b;
    color: #fafafa;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
}

[data-testid="stSidebar"] {
    background: #18181b;
    border-right: 1px solid #27272a;
}

[data-testid="stSidebar"] .css-1d391kg {
    padding-top: 2rem;
}

h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.15;
    color: #ffffff;
}

.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.3rem;
    letter-spacing: -0.04em;
}

.hero-subtitle {
    font-size: 1rem;
    color: #a1a1aa;
    font-weight: 400;
    line-height: 1.5;
}

.savings-number {
    font-family: 'JetBrains Mono', 'SF Mono', Consolas, monospace;
    font-size: 2.75rem;
    font-weight: 600;
    color: #10b981;
    text-align: center;
    padding: 1.5rem;
    letter-spacing: -0.02em;
    background: #18181b;
    border-radius: 12px;
    border: 1px solid #27272a;
    box-shadow: 0 1px 3px rgba(0,0,0,0.5);
}

.savings-label {
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #a1a1aa;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.savings-sublabel {
    font-size: 0.875rem;
    color: #71717a;
    font-weight: 400;
    margin-top: 0.5rem;
}

.metric-box {
    background: #18181b;
    border: 1px solid #27272a;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.75rem 0;
    box-shadow: 0 1px 2px rgba(0,0,0,0.5);
    transition: all 0.15s ease;
}

.metric-box:hover {
    border-color: #3f3f46;
    box-shadow: 0 4px 12px rgba(0,0,0,0.8);
    transform: translateY(-1px);
}

div[data-testid="stMetricValue"] {
    color: #10b981;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 1.75rem;
}

div[data-testid="stMetricLabel"] {
    color: #a1a1aa;
    font-weight: 500;
    font-size: 0.875rem;
}

div[data-testid="stMetricDelta"] {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
}

.alert-red {
    background: #450a0a;
    border-left: 3px solid #ef4444;
    border-radius: 6px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.875rem;
    font-weight: 400;
    line-height: 1.5;
    color: #fca5a5;
    transition: all 0.15s ease;
}

.alert-red:hover {
    background: #7f1d1d;
    transform: translateX(3px);
}

.alert-green {
    background: #064e3b;
    border-left: 3px solid #10b981;
    border-radius: 6px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.875rem;
    font-weight: 400;
    line-height: 1.5;
    color: #6ee7b7;
    transition: all 0.15s ease;
}

.alert-green:hover {
    background: #022c22;
    transform: translateX(3px);
}

.alert-yellow {
    background: #451a03;
    border-left: 3px solid #f59e0b;
    border-radius: 6px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.875rem;
    font-weight: 400;
    line-height: 1.5;
    color: #fcd34d;
    transition: all 0.15s ease;
}

.alert-yellow:hover {
    background: #78350f;
    transform: translateX(3px);
}

.alert-blue {
    background: #1e3a8a;
    border-left: 3px solid #3b82f6;
    border-radius: 6px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.875rem;
    font-weight: 400;
    line-height: 1.5;
    color: #93c5fd;
    transition: all 0.15s ease;
}

.alert-blue:hover {
    background: #172554;
    transform: translateX(3px);
}

.stButton button {
    background: #3b82f6;
    color: white;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.25rem;
    font-size: 0.9rem;
    letter-spacing: -0.01em;
    transition: all 0.15s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.stButton button:hover {
    background: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

.stButton button:active {
    transform: translateY(0);
}

.stButton button[kind="secondary"] {
    background: #18181b;
    color: #fafafa;
    border: 1px solid #3f3f46;
    box-shadow: 0 1px 2px rgba(0,0,0,0.5);
}

.stButton button[kind="secondary"]:hover {
    background: #27272a;
    border-color: #52525b;
}

[data-testid="stFileUploader"] {
    background: #18181b;
    border: 2px dashed #3f3f46;
    border-radius: 10px;
    padding: 1.2rem;
    transition: all 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #3b82f6;
    background: #27272a;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.25rem;
    background: transparent;
    border-bottom: 1px solid #27272a;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #a1a1aa;
    border-radius: 6px 6px 0 0;
    padding: 0.65rem 1.2rem;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    border: none;
    transition: all 0.15s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: #27272a;
    color: #fafafa;
}

.stTabs [aria-selected="true"] {
    background: transparent;
    color: #3b82f6;
    border-bottom: 2px solid #3b82f6;
    font-weight: 600;
}

[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #27272a;
    background: #18181b;
}

[data-testid="stDataFrame"] table {
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
}

[data-testid="stDataFrame"] thead {
    background: #27272a;
    color: #fafafa;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
}

[data-testid="stDataFrame"] tbody tr:hover {
    background: #27272a;
}

.stSlider [data-baseweb="slider"] {
    background: #3f3f46;
}

.stSlider [role="slider"] {
    background: #3b82f6;
    border: 2px solid #18181b;
    box-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.stSlider [data-baseweb="slider-track-fill"] {
    background: #3b82f6;
}

hr {
    border: none;
    height: 1px;
    background: #27272a;
    margin: 1.5rem 0;
}

.stAlert {
    background: #1e3a8a;
    border: 1px solid #1e40af;
    border-left: 4px solid #3b82f6;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: 'Inter', sans-serif;
    color: #bfdbfe;
}

.stSuccess {
    background: #064e3b;
    border: 1px solid #065f46;
    border-left: 4px solid #10b981;
    color: #a7f3d0;
}

.stWarning {
    background: #451a03;
    border: 1px solid #78350f;
    border-left: 4px solid #f59e0b;
    color: #fde68a;
}

.css-16huue1, [data-testid="stCaptionContainer"] {
    color: #a1a1aa;
    font-size: 0.875rem;
    font-weight: 400;
    font-family: 'Inter', sans-serif;
}

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #18181b;
}

::-webkit-scrollbar-thumb {
    background: #3f3f46;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: #52525b;
}

[data-testid="stSidebar"] h1 {
    color: #ffffff;
    font-size: 1.5rem;
    font-weight: 700;
}

[data-testid="stSidebar"] .css-1lcbmhc {
    color: #a1a1aa;
}

input, select, textarea {
    background: #18181b !important;
    border: 1px solid #3f3f46 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

input:focus, select:focus, textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
}

.js-plotly-plot {
    background: #18181b;
    border-radius: 12px;
    border: 1px solid #27272a;
    padding: 0.5rem;
}

.badge-high {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: #450a0a;
    color: #fca5a5;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.025em;
}

.badge-medium {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: #451a03;
    color: #fcd34d;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.025em;
}

.badge-low {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: #064e3b;
    color: #6ee7b7;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.025em;
}

* {
    animation: none !important;
    text-shadow: none !important;
}

* {
    transition: all 0.15s ease;
}

</style>
""", unsafe_allow_html=True)

if 'optimized' not in st.session_state:
    st.session_state.optimized = False
if 'savings_counter' not in st.session_state:
    st.session_state.savings_counter = 0

@st.cache_data
def load_demo_data():
    try:
        return pd.read_csv("data/demo_timetable.csv")
    except FileNotFoundError:
        import os
        os.system("python generate_csv.py")
        return pd.read_csv("data/demo_timetable.csv")

df = load_demo_data()

with st.sidebar:
    st.markdown('<p class="hero-title">TwinFlow Pro</p>', unsafe_allow_html=True)
    st.caption("🏛️ Campus Digital Twin")
    st.divider()
    
    page = option_menu(
        menu_title=None,
        options=["Dashboard", "3D Campus", "Optimizer", "Analytics"],
        icons=["speedometer2", "building", "lightning-charge", "graph-up-arrow"],
        default_index=0,
        styles={
            "container": {"background-color": "#10101F"},
            "nav-link": {"color": "#aaa", "font-size": "0.9rem"},
            "nav-link-selected": {"background-color": "#00D4FF22", "color": "#00D4FF"},
        }
    )
    
    st.divider()
    st.markdown("**📁 Upload Timetable**")
    uploaded_file = st.file_uploader("CSV File", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file:
        df = TimetableParser.parse(uploaded_file)
        st.success("✅ Timetable loaded!")
    
    st.divider()
    if st.button("🚀 Load Demo Campus", use_container_width=True, type="primary"):
        st.session_state.optimized = False
        st.rerun()
    
    st.markdown("---")
    st.caption("⚡ Powered by TwinFlow AI")
    st.caption("🌿 Built for Smart Cities")

if page == "Dashboard":
    
    st.markdown('<p class="hero-title">Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Real-time optimization dashboard for SRM Kattankulathur Campus</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_hero, col_action = st.columns([2.5, 1])
    
    with col_hero:
        savings_val = 2460000 if st.session_state.optimized else 340000
        label = "Annual Cost Savings" if st.session_state.optimized else "Current Annual Waste"
        sublabel = "Optimization active. System running at max efficiency." if st.session_state.optimized else "Action required: High energy waste detected."
        num_color = "#059669" if st.session_state.optimized else "#dc2626"
        bg_color = "#f0fdf4" if st.session_state.optimized else "#fef2f2"
        border_color = "#bbf7d0" if st.session_state.optimized else "#fecaca"
        
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1.5rem; display: flex; flex-direction: column; justify-content: center;">
            <p class="savings-label" style="text-align: left; margin: 0;">{label}</p>
            <p class="savings-number" style="color: {num_color}; background: {bg_color}; border: 1px solid {border_color}; text-align: left; padding: 1rem; margin-top: 0.5rem; margin-bottom: 0.5rem; font-size: 2.5rem;">₹ {savings_val:,}</p>
            <p class="savings-sublabel" style="margin: 0;">{sublabel}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_action:
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1.25rem; margin-bottom: 0.5rem;">
            <p style="font-weight: 600; color: #111827; margin-bottom: 0.25rem;">System Status</p>
            <p style="color: {'#059669' if st.session_state.optimized else '#dc2626'}; font-weight: 500; font-size: 0.9rem; margin-bottom: 1rem;">
                {'● Optimized' if st.session_state.optimized else '● Needs Attention'}
            </p>
            <p style="color: #6b7280; font-size: 0.85rem; margin-bottom: 0; line-height: 1.4;">
                {'Zero energy waste currently detected across the campus.' if st.session_state.optimized else 'AI has identified schedule conflicts & energy leaks.'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.optimized:
            if st.button("⚡ Resolve Issues", type="primary", use_container_width=True):
                st.session_state.optimized = True
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    m1_val, m1_delta = (f"₹2,05,000", "+₹1,77,000") if st.session_state.optimized else (f"₹28,000", "Baseline")
    m2_val, m2_delta = (f"187 tons", "+175 tons reduced") if st.session_state.optimized else (f"12 tons", "High emissions")
    m3_val, m3_delta = (f"28%", "2 routes merged") if st.session_state.optimized else (f"0%", "Unoptimized")
    m4_val, m4_delta = (f"2", "16 issues fixed") if st.session_state.optimized else (f"18", "Empty ACs running")

    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
        <div class="metric-box" style="margin: 0;">
            <div data-testid="stMetricLabel" style="margin-bottom: 0.5rem;">Monthly Savings</div>
            <div data-testid="stMetricValue" style="color: {'#059669' if st.session_state.optimized else '#111827'};">{m1_val}</div>
            <div data-testid="stMetricDelta" style="color: {'#059669' if st.session_state.optimized else '#6b7280'}; margin-top: 0.25rem;">{m1_delta}</div>
        </div>
        <div class="metric-box" style="margin: 0;">
            <div data-testid="stMetricLabel" style="margin-bottom: 0.5rem;">CO₂ Reduced</div>
            <div data-testid="stMetricValue" style="color: {'#059669' if st.session_state.optimized else '#111827'};">{m2_val}</div>
            <div data-testid="stMetricDelta" style="color: {'#059669' if st.session_state.optimized else '#dc2626'}; margin-top: 0.25rem;">{m2_delta}</div>
        </div>
        <div class="metric-box" style="margin: 0;">
            <div data-testid="stMetricLabel" style="margin-bottom: 0.5rem;">Shuttle Efficiency</div>
            <div data-testid="stMetricValue" style="color: {'#059669' if st.session_state.optimized else '#111827'};">{m3_val}</div>
            <div data-testid="stMetricDelta" style="color: {'#059669' if st.session_state.optimized else '#6b7280'}; margin-top: 0.25rem;">{m3_delta}</div>
        </div>
        <div class="metric-box" style="margin: 0;">
            <div data-testid="stMetricLabel" style="margin-bottom: 0.5rem;">Rooms Flagged</div>
            <div data-testid="stMetricValue" style="color: {'#059669' if st.session_state.optimized else '#dc2626'}">{m4_val}</div>
            <div data-testid="stMetricDelta" style="color: {'#059669' if st.session_state.optimized else '#dc2626'}; margin-top: 0.25rem;">{m4_delta}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    left_col, right_col = st.columns([2.5, 1])
    
    with left_col:
        st.markdown('<p style="font-weight: 600; color: #374151; font-size: 1.1rem; margin-bottom: 0.5rem; font-family: Inter, sans-serif;">Live Campus Overview</p>', unsafe_allow_html=True)
        fig = Visualizer.campus_overview_chart(df, st.session_state.optimized)
        st.plotly_chart(fig, use_container_width=True)
    
    with right_col:
        st.markdown('<p style="font-weight: 600; color: #374151; font-size: 1.1rem; margin-bottom: 0.5rem; font-family: Inter, sans-serif;">Recent Alerts</p>', unsafe_allow_html=True)
        AlertSystem.render_all(optimized=st.session_state.optimized)

elif page == "3D Campus":
    
    st.markdown('<h1 class="hero-title">🗺️ 3D Campus Digital Twin</h1>', 
               unsafe_allow_html=True)
    st.caption("Hover over any building to see occupancy stats and optimization suggestions")
    
    if st.button("⚡ Optimize All Buildings", type="primary"):
        st.session_state.optimized = True
    
    st.divider()
    
    tab1, tab2 = st.tabs(["🏛️ 3D Building View", "🗺️ 2D Campus Heatmap"])
    
    with tab1:
        fig_3d = Visualizer.campus_3d(df, st.session_state.optimized)
        st.plotly_chart(fig_3d, use_container_width=True)
        
        st.info("💡 **How to read this map:** "
               "RED = <20% occupancy (energy waste) | "
               "YELLOW = 20-70% (moderate) | "
               "GREEN = >70% (efficient)")
    
    with tab2:
        fig_heat = Visualizer.room_heatmap(df)
        st.plotly_chart(fig_heat, use_container_width=True)

elif page == "Optimizer":
    
    st.markdown('<h1 class="hero-title">⚡ AI Optimization Engine</h1>', 
               unsafe_allow_html=True)
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["💰 ROI Calculator", "📋 Action Plan", "🔄 Schedule Optimizer"])
    
    with tab1:
        st.subheader("💰 Calculate Your Campus Savings")
        st.caption("Adjust sliders to match your college size")
        
        c1, c2, c3 = st.columns(3)
        labs = c1.slider("🔬 Number of Labs", 5, 50, 20)
        hostels = c2.slider("🏠 Number of Hostels", 1, 10, 4)
        halls = c3.slider("🎓 Lecture Halls", 2, 20, 8)
        days = st.slider("📅 Working Days/Year", 180, 250, 220)
        
        roi = Optimizer.calculate_roi(labs, hostels, halls, days)
        
        st.divider()
        
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("💰 Annual Savings", f"₹{roi['annual']:,}")
        r2.metric("📅 Monthly Savings", f"₹{roi['monthly']:,}")
        r3.metric("🌿 CO2 Reduced", f"{roi['co2']} tons/yr")
        r4.metric("🚌 Fuel Saved", f"{roi['shuttle_fuel']}%")
        
        st.success(f"⚡ **Payback Period: {roi['payback']}** — Zero hardware investment needed!")
    
    with tab2:
        st.subheader("📋 Optimization Action Plan")
        actions_df = Optimizer.generate_actions(df)
        
        col1, col2 = st.columns([2,1])
        with col1:
            st.dataframe(
                actions_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "priority": st.column_config.TextColumn("Priority"),
                    "room": st.column_config.TextColumn("Room"),
                    "action": st.column_config.TextColumn("Action"),
                    "daily_saving": st.column_config.NumberColumn(
                        "Daily Saving", format="₹%d"),
                    "monthly_saving": st.column_config.NumberColumn(
                        "Monthly Saving", format="₹%d"),
                }
            )
        with col2:
            total_daily = actions_df['daily_saving'].sum()
            total_monthly = actions_df['monthly_saving'].sum()
            st.metric("Total Daily Savings", f"₹{total_daily:,}")
            st.metric("Total Monthly Savings", f"₹{total_monthly:,}")
            st.metric("Total Annual Savings", f"₹{total_monthly*12:,}")
            
            if st.button("✅ Apply All Actions", type="primary", use_container_width=True):
                st.session_state.optimized = True
                st.success("All optimizations applied!")
    
    with tab3:
        st.subheader("🔄 Smart Schedule Optimizer")
        st.caption("AI finds empty slots and suggests energy-saving schedules")
        
        fig_schedule = Visualizer.schedule_grid(df)
        st.plotly_chart(fig_schedule, use_container_width=True)
        
        st.warning("🔴 **Red cells** = empty rooms with AC running. "
                  "**18 rooms** identified for immediate action.")

elif page == "Analytics":
    
    st.markdown('<h1 class="hero-title">📊 Campus Analytics</h1>', 
               unsafe_allow_html=True)
    st.caption("Data-driven insights from your campus timetable")
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📈 Occupancy Trends", 
                                  "💰 Savings Projection", 
                                  "🏆 Room Rankings"])
    
    with tab1:
        fig1 = Visualizer.weekly_occupancy(df)
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        fig2 = Visualizer.savings_projection()
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        fig3 = Visualizer.room_efficiency_ranking(df)
        st.plotly_chart(fig3, use_container_width=True)
