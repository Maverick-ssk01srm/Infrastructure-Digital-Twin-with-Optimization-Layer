import streamlit as st

ALERTS = [
    ("🔴", "Lab A empty since 10AM — AC still running — ₹570/day loss",   "alert-red"),
    ("🔴", "Lab C: 8% occupancy all week — ₹2,500 waste this week",       "alert-red"),
    ("🟡", "Shuttle #3 at 18% capacity — suggest merge with Route 2",     "alert-yellow"),
    ("🟡", "Hall 2: only 35% used — reschedule 2 classes to Hall 1",      "alert-yellow"),
    ("🟢", "Lab B optimized — ₹1,200 saved today",                        "alert-green"),
    ("🔵", "Hostel B water usage +45% above baseline — check pipes",       "alert-blue"),
    ("⚡", "Admin block: peak load 2-4PM — shift AC cycle by 30 min",     "alert-yellow"),
]

POST_ALERTS = [
    ("✅", "Lab A: AC off 10AM-2PM — ₹570 saved today",       "alert-green"),
    ("✅", "Shuttle routes merged — 28% fuel reduction",       "alert-green"),
    ("✅", "Hall 2 schedule consolidated — ₹1,200 saved",     "alert-green"),
    ("🔵", "Hostel B: plumber notified — monitoring ongoing", "alert-blue"),
    ("✅", "All 4 labs optimized — ₹2,280 saved today",       "alert-green"),
]

class AlertSystem:
    @staticmethod
    def render_all(optimized=False):
        alerts = POST_ALERTS if optimized else ALERTS
        for icon, msg, css_class in alerts:
            st.markdown(
                f'<div class="{css_class}">{icon} {msg}</div>',
                unsafe_allow_html=True
            )
