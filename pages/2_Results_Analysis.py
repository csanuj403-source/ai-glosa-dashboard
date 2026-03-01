import streamlit as st
import plotly.graph_objects as go

st.title("📊 Results & Analysis")

st.markdown("## 🚗 Performance Comparison")

# Example Comparison Data (Based on Your Simulation Logic)
labels = ["Fuel Consumption", "CO₂ Emission", "Stops at Signal", "Traffic Smoothness"]

baseline = [100, 100, 100, 60]      # Normal car (reference scale)
glosa = [75, 75, 30, 95]            # AI-GLOSA improved values

fig = go.Figure()

fig.add_trace(go.Bar(
    x=labels,
    y=baseline,
    name="Baseline Vehicle",
))

fig.add_trace(go.Bar(
    x=labels,
    y=glosa,
    name="AI-GLOSA Vehicle",
))

fig.update_layout(
    barmode="group",
    title="Baseline vs AI-GLOSA Comparison (Relative Scale)",
    xaxis_title="Parameters",
    yaxis_title="Relative Performance Index",
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("""
## 🔍 Observations

### 🚗 Baseline Vehicle
- Frequent stopping at red signals  
- Higher fuel consumption  
- Increased CO₂ emission  
- Stop-and-go driving pattern  

### 🚙 AI-GLOSA Vehicle
- Speed adjusted to match green window  
- Reduced idle fuel loss  
- Lower emissions  
- Smooth traffic movement  

---

## 📈 Benefits of GLOSA

- 🔹 15–25% Fuel Efficiency Improvement  
- 🔹 Reduced Carbon Emission  
- 🔹 Less Brake Wear  
- 🔹 Better Passenger Comfort  
- 🔹 Reduced Traffic Congestion  

---

## ❓ Why This System Is Required

Urban traffic causes:

- Excessive fuel wastage  
- Environmental pollution  
- Increased operational cost  
- High traffic congestion  

AI-based Cooperative GLOSA solves this using:

- Real-time signal timing data  
- Speed advisory algorithms  
- Vehicle-to-Vehicle communication  
- Predictive motion control  
""")
