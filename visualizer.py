import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

BG_DARK = "#09090b"
BG_CARD = "#18181b"
TEXT_PRIMARY = "#fafafa"
TEXT_MUTED = "#a1a1aa"

ACCENT_BLUE = "#3b82f6"
ACCENT_GREEN = "#10b981"
ACCENT_RED = "#ef4444"
ACCENT_YELLOW = "#f59e0b"


class Visualizer:

    @staticmethod
    def _dark_layout(fig, title=""):
        fig.update_layout(
            title=dict(
                text=title, 
                font=dict(color=ACCENT_BLUE, size=15, family="Inter")
            ),
            paper_bgcolor=BG_DARK,
            plot_bgcolor=BG_CARD,
            font=dict(color=TEXT_PRIMARY, family="Inter"),
            margin=dict(l=20, r=20, t=50, b=20),
            hoverlabel=dict(
                bgcolor="#18181b",
                font_size=13,
                font_family="Inter",
                bordercolor="#3f3f46"
            )
        )
        return fig

    @staticmethod
    def campus_3d(df, optimized=False):
        buildings = [
            {"name": "Lab A",     "x": 1, "y": 1, "occ": 0.15, "h": 3},
            {"name": "Lab B",     "x": 4, "y": 1, "occ": 0.75, "h": 3},
            {"name": "Lab C",     "x": 7, "y": 1, "occ": 0.08, "h": 3},
            {"name": "Lab D",     "x": 10,"y": 1, "occ": 0.60, "h": 3},
            {"name": "Hall 1",    "x": 1, "y": 5, "occ": 0.90, "h": 2},
            {"name": "Hall 2",    "x": 5, "y": 5, "occ": 0.35, "h": 2},
            {"name": "Hostel A",  "x": 1, "y": 9, "occ": 0.88, "h": 5},
            {"name": "Hostel B",  "x": 5, "y": 9, "occ": 0.72, "h": 5},
            {"name": "Admin",     "x": 3, "y": 3, "occ": 0.55, "h": 4},
            {"name": "Canteen",   "x": 8, "y": 6, "occ": 0.95, "h": 1},
            {"name": "Seminar 1", "x": 8, "y": 3, "occ": 0.12, "h": 2},
            {"name": "Seminar 2", "x": 11,"y": 5, "occ": 0.18, "h": 2},
        ]
        
        fig = go.Figure()
        
        for b in buildings:
            occ = 0.9 if optimized else b["occ"]
            r = int(255 * (1 - occ))
            g = int(200 * occ)
            color = f"rgb({r},{g},60)"
            monthly_waste = int((1 - occ) * 18000)
            
            # Building pillar
            fig.add_trace(go.Scatter3d(
                x=[b["x"]], y=[b["y"]], z=[b["h"]],
                mode='markers+text',
                marker=dict(
                    size=18 + occ * 12,
                    color=color,
                    symbol='square',
                    opacity=0.85,
                    line=dict(color='white', width=1)
                ),
                text=[f"{b['name']}"],
                textfont=dict(size=9, color=TEXT_PRIMARY, family="Inter"),
                textposition="top center",
                name=b["name"],
                hovertemplate=(
                    f"<b>{b['name']}</b><br>"
                    f"Occupancy: {int(occ*100)}%<br>"
                    f"Status: {'✅ Efficient' if occ > 0.7 else '⚠️ Moderate' if occ > 0.3 else '🔴 WASTING ENERGY'}<br>"
                    f"Monthly waste: ₹{monthly_waste:,}<br>"
                    f"Suggestion: {'No action needed' if occ > 0.7 else 'Turn off AC during empty hours'}"
                    "<extra></extra>"
                )
            ))
        
        # Ground plane
        gx = np.linspace(0, 13, 15)
        gy = np.linspace(0, 11, 15)
        GX, GY = np.meshgrid(gx, gy)
        GZ = np.zeros_like(GX)
        
        fig.add_trace(go.Surface(
            x=GX, y=GY, z=GZ,
            colorscale=[[0, "#18181b"], [1, "#27272a"]],
            showscale=False, opacity=0.9, hoverinfo='skip'
        ))
        
        title = "✅ Campus Optimized — All Buildings Efficient" if optimized else \
                "⚠️ Campus Twin — RED = Energy Waste | GREEN = Efficient"
        
        fig.update_layout(
            title=dict(text=title, font=dict(color=ACCENT_BLUE, size=14, family="Inter")),
            paper_bgcolor=BG_DARK,
            font=dict(color=TEXT_PRIMARY, family="Inter"),
            scene=dict(
                bgcolor="#09090b",
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=False, visible=False),
                zaxis=dict(showgrid=False, visible=False, range=[0, 8]),
                camera=dict(eye=dict(x=1.6, y=1.6, z=1.0))
            ),
            height=560,
            showlegend=False
        )
        return fig

    @staticmethod
    def campus_overview_chart(df, optimized=False):
        """Bar chart of room occupancy — quick overview"""
        rooms = ["Lab A","Lab B","Lab C","Lab D",
                 "Hall 1","Hall 2","Seminar 1","Seminar 2",
                 "Hostel A","Hostel B"]
        base_occ = [15,75,8,60,90,35,12,18,88,72]
        
        if optimized:
            occs = [max(x, 70) for x in base_occ]
        else:
            occs = base_occ
        
        colors = [ACCENT_RED if o < 20 else 
                  ACCENT_YELLOW if o < 70 else 
                  ACCENT_GREEN for o in occs]
        
        fig = go.Figure(go.Bar(
            x=rooms, y=occs,
            marker_color=colors,
            marker_line=dict(color=BG_DARK, width=1),
            text=[f"{o}%" for o in occs],
            textposition='outside',
            textfont=dict(color=TEXT_PRIMARY, family="Inter"),
            hovertemplate="<b>%{x}</b><br>Occupancy: %{y}%<extra></extra>"
        ))
        
        fig.add_hline(y=20, line_dash="dash", 
                     line_color=ACCENT_RED, 
                     annotation_text="Waste threshold (20%)")
        fig.add_hline(y=70, line_dash="dash",
                     line_color=ACCENT_GREEN,
                     annotation_text="Efficient threshold (70%)")
        
        fig.update_layout(
            title="Room Occupancy Overview",
            paper_bgcolor=BG_DARK,
            plot_bgcolor=BG_CARD,
            font=dict(color=TEXT_PRIMARY, family="Inter"),
            yaxis=dict(range=[0,110], ticksuffix="%"),
            height=380
        )
        return fig

    @staticmethod
    def room_heatmap(df):
        hours = list(range(8, 19))
        rooms = df['room'].unique().tolist()
        
        data = np.random.uniform(0.1, 0.9, (len(rooms), len(hours)))
        # Force some waste zones
        data[0][5:8] = 0.08    # Lab A afternoon
        data[2][:] = 0.10      # Lab C mostly empty
        data[6][3:7] = 0.05    # Seminar Room mostly empty
        
        fig = px.imshow(
            data,
            x=[f"{h}:00" for h in hours],
            y=rooms,
            color_continuous_scale=[
                [0.0, ACCENT_RED],
                [0.2, ACCENT_RED],
                [0.4, ACCENT_YELLOW],
                [0.7, "#aaff00"],
                [1.0, ACCENT_GREEN]
            ],
            title="Occupancy Heatmap — Red = Energy Waste Zone",
            labels=dict(x="Hour of Day", y="Room", color="Occupancy")
        )
        fig.update_layout(
            paper_bgcolor=BG_DARK,
            plot_bgcolor=BG_CARD,
            font=dict(color=TEXT_PRIMARY, family="Inter"),
            height=420
        )
        return fig

    @staticmethod
    def schedule_grid(df):
        hours = list(range(8, 19))
        rooms = ["Lab A","Lab B","Lab C","Lab D",
                 "Hall 1","Hall 2","Seminar 1","Seminar 2"]
        
        grid = np.random.choice(
            [0, 0, 0.1, 0.5, 0.8, 0.9],
            size=(len(rooms), len(hours)),
            p=[0.25, 0.15, 0.15, 0.15, 0.15, 0.15]
        )
        
        fig = px.imshow(
            grid,
            x=[f"{h}:00" for h in hours],
            y=rooms,
            color_continuous_scale=[[0,ACCENT_RED],[0.25,"#ea580c"],
                                     [0.5,ACCENT_YELLOW],[0.75,"#84cc16"],
                                     [1.0,ACCENT_GREEN]],
            title="Schedule Grid — Empty slots = ₹570/day wasted",
            labels=dict(x="Time Slot", y="Room", color="Occupancy")
        )
        fig.update_layout(
            paper_bgcolor=BG_DARK, plot_bgcolor=BG_CARD, font=dict(color=TEXT_PRIMARY, family="Inter"), height=380
        )
        return fig

    @staticmethod
    def weekly_occupancy(df):
        hours = list(range(8, 19))
        avg_occ = [45, 72, 81, 65, 32, 20, 18, 25, 60, 78, 55]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[f"{h}:00" for h in hours],
            y=avg_occ,
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(37,99,235,0.08)',
            line=dict(color=ACCENT_BLUE, width=3),
            marker=dict(size=8, color=ACCENT_BLUE),
            name="Avg Occupancy %"
        ))
        fig.add_hrect(y0=0, y1=20, fillcolor=ACCENT_RED,
                     opacity=0.08, line_width=0,
                     annotation_text="Waste Zone",
                     annotation_font_color=ACCENT_RED)
        
        fig.update_layout(
            title="Average Campus Occupancy by Hour",
            paper_bgcolor=BG_DARK, plot_bgcolor=BG_CARD,
            font=dict(color=TEXT_PRIMARY, family="Inter"),
            yaxis=dict(ticksuffix="%"),
            height=380
        )
        return fig

    @staticmethod
    def savings_projection():
        months = ["Jan","Feb","Mar","Apr","May","Jun",
                  "Jul","Aug","Sep","Oct","Nov","Dec"]
        baseline = [28000 + np.random.randint(-3000, 3000) for _ in months]
        optimized = [205000 + np.random.randint(-5000, 5000) for _ in months]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months, y=baseline,
                            name="Before Optimization",
                            marker_color=ACCENT_RED, opacity=0.7))
        fig.add_trace(go.Bar(x=months, y=optimized,
                            name="After Optimization",
                            marker_color=ACCENT_GREEN, opacity=0.7))
        
        fig.update_layout(
            title="Monthly Savings: Before vs After Optimization",
            paper_bgcolor=BG_DARK, plot_bgcolor=BG_CARD,
            font=dict(color=TEXT_PRIMARY, family="Inter"),
            barmode='group',
            yaxis=dict(tickprefix="₹"),
            height=380
        )
        return fig

    @staticmethod
    def room_efficiency_ranking(df):
        rooms = ["Lab A","Seminar 1","Lab C","Seminar 2",
                 "Hall 2","Admin","Lab D","Lab B",
                 "Hostel B","Hostel A","Hall 1","Canteen"]
        scores = [15,18,20,22,35,55,60,75,72,88,90,95]
        colors = [ACCENT_RED if s < 30 else 
                  ACCENT_YELLOW if s < 70 else 
                  ACCENT_GREEN for s in scores]
        
        fig = go.Figure(go.Bar(
            x=scores, y=rooms,
            orientation='h',
            marker_color=colors,
            text=[f"{s}% — {'🔴 Wasteful' if s<30 else '🟡 Average' if s<70 else '✅ Efficient'}" 
                  for s in scores],
            textposition='outside',
            textfont=dict(color=TEXT_PRIMARY, size=10, family="Inter")
        ))
        fig.update_layout(
            title="Room Efficiency Ranking (Lowest to Highest)",
            paper_bgcolor=BG_DARK, plot_bgcolor=BG_CARD,
            font=dict(color=TEXT_PRIMARY, family="Inter"),
            xaxis=dict(ticksuffix="%", range=[0, 120]),
            height=420
        )
        return fig
