# TwinFlow Pro
**Campus Infrastructure Digital Twin + AI Optimizer**
"DONE BY TEAM YAP++ FOR AMD SLINGSHOT 2026"
"Predict campus waste before it happens"

Upload your college timetable → Instantly see ₹25L/year in savings through 3D visualization and AI-powered optimization. Zero hardware needed.

## Tech Stack
- **Frontend/Backend:** Streamlit
- **Data Visualization:** Plotly, Altair
- **Data Processing:** Pandas, NumPy

## Setup Instructions
1. Clone this repository or download all files.
2. Ensure you have Python installed.
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the demo application setup script to generate mock data:
   ```bash
   python generate_csv.py
   ```

## Running the App
Start the Streamlit Application:
```bash
streamlit run app.py
```

## Demo Flow (10 Steps)
1. **Launch App**: Observe the futuristic Dark Tech theme on the main dashboard.
2. **Review Metrics**: See current waste metrics in RED under normal operating schedules.
3. **Upload/Load Data**: Use the left sidebar to load `demo_timetable.csv` if it wasn't preloaded.
4. **Auto-Optimize**: Click the "Auto-Optimize All" button on the dashboard top right.
5. **View Post-Optimization**: Notice total savings instantly switch to GREEN (₹24.6 Lakhs).
6. **Navigate to 3D Campus**: Open "3D Campus" from sidebar. Interact with the 3D map.
7. **Hover on Buildings**: See tooltips listing specific empty states and AC wastage.
8. **Check Optimizer Plan**: Go to "Optimizer" -> "Action Plan" tab to see actionable items.
9. **Try ROI Calculator**: Use sliders to see scale impact for different college sizes.
10. **Explore Analytics**: Go to "Analytics" to view Occupancy Trends over typical weeks and efficiency metrics per room.

## Screenshots Description
*Note: Due to being run locally, screenshots are generated dynamically on viewing the app.*
- **Dashboard**: High contrast glowing numbers indicating potential financial and environmental savings.
- **3D Interactive Map**: Plotly Scatter3D rendering buildings scaled by occupancy metric (Green = efficient, Red = wasteful).
- **Rules Engine Tab**: Dataframe with conditional color formatting mapped to daily saving totals.
- **Alerts**: Real-time simulation components providing immediate feedback on pipeline adjustments.
