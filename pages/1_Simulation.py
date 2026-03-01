import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

st.title("🚦 AI Cooperative GLOSA Simulation")

# ===================================================
# IEEE AI Cooperative GLOSA – CLEAN PREMIUM FINAL
# Glow Border + Brake Indicator
# SOC Bar Removed (Layout Preserved)
# ===================================================

import numpy as np
import plotly.graph_objects as go

road_length = 1200
dt = 0.3
total_time = 100
steps = int(total_time / dt)

signals = [
    {"pos": 400, "cycle": 40, "green": 18, "offset": 0},
    {"pos": 800, "cycle": 45, "green": 20, "offset": 12},
]

car1 = {"pos": 0, "speed": 50/3.6, "base": 50/3.6, "soc": 25}
car2 = {"pos": 0, "speed": 50/3.6, "base": 50/3.6}
car3 = {"pos": -200, "speed": 50/3.6, "base": 50/3.6, "soc": 85}

fuel_car1 = fuel_car2 = fuel_car3 = 0
frames = []

def signal_state(signal, t):
    cycle_time = (t + signal["offset"]) % signal["cycle"]
    if cycle_time < signal["green"]:
        return "GREEN", signal["green"] - cycle_time
    else:
        return "RED", signal["cycle"] - cycle_time

def apply_glosa(car, signal_info):
    next_state, next_timer, distance = "NONE", 0, 0
    recommended_speed = car["base"]

    for idx, s in enumerate(signals):
        if s["pos"] > car["pos"]:
            next_state, next_timer = signal_info[idx]
            distance = s["pos"] - car["pos"]
            break

    if next_state == "RED":
        recommended_speed = min(distance/max(next_timer,0.1), car["base"])

    alpha = 0.15
    car["speed"] = (1-alpha)*car["speed"] + alpha*recommended_speed
    car["pos"] += car["speed"] * dt

    return next_state, distance, recommended_speed

for step in range(steps):

    t = step * dt
    blink = (step // 5) % 2 == 0

    signal_info = []
    signal_shapes = []

    for s in signals:
        state, timer = signal_state(s, t)
        signal_info.append((state, timer))
        signal_shapes.append(
            dict(type="line",
                 x0=s["pos"], x1=s["pos"],
                 y0=0.93, y1=0.99,
                 xref="x", yref="paper",
                 line=dict(color="green" if state=="GREEN" else "red", width=6))
        )

    state1, dist1, rec1 = apply_glosa(car1, signal_info)
    state3, dist3, rec3 = apply_glosa(car3, signal_info)

    stop = False
    for idx, s in enumerate(signals):
        state2, _ = signal_info[idx]
        dist2 = s["pos"] - car2["pos"]
        if 0 < dist2 < 8 and state2 == "RED":
            stop = True
            break

    car2["speed"] = 0 if stop else car2["base"]
    car2["pos"] += car2["speed"] * dt

    car1["soc"] -= 0.03
    car3["soc"] -= 0.01
    low_battery = car1["soc"] < 20

    if low_battery and car3["pos"] < car1["pos"] - 15:
        car3["speed"] += 0.4

    fuel_car1 += car1["speed"] * dt * 0.0003
    fuel_car2 += car2["speed"] * dt * 0.0005
    fuel_car3 += car3["speed"] * dt * 0.0003

    fuel_saved_1 = fuel_car2 - fuel_car1
    fuel_saved_3 = fuel_car2 - fuel_car3
    emission_1 = fuel_saved_1 * 2.31
    emission_3 = fuel_saved_3 * 2.31

    border1_color = "red" if low_battery else "#00BFFF"
    border1_width = 5 if low_battery else 3

    frames.append(go.Frame(
        data=[

            go.Scatter(x=[car1["pos"]], y=[0.985],
                       mode="markers", marker=dict(size=14,color="#00BFFF")),
            go.Scatter(x=[car2["pos"]], y=[0.965],
                       mode="markers", marker=dict(size=14,color="#FFA500")),
            go.Scatter(x=[car3["pos"]], y=[0.945],
                       mode="markers", marker=dict(size=14,color="lime")),

            go.Indicator(mode="gauge+number",
                         value=car1["speed"]*3.6,
                         domain={'x':[0.05,0.29],'y':[0.38,0.52]},
                         gauge={'axis':{'range':[0,80]}}),

            go.Indicator(mode="gauge+number",
                         value=car2["speed"]*3.6,
                         domain={'x':[0.37,0.61],'y':[0.38,0.52]},
                         gauge={'axis':{'range':[0,80]}}),

            go.Indicator(mode="gauge+number",
                         value=car3["speed"]*3.6,
                         domain={'x':[0.69,0.93],'y':[0.38,0.52]},
                         gauge={'axis':{'range':[0,80]}}),
        ],

        layout=go.Layout(
            shapes=signal_shapes + [

                dict(type="rect",xref="paper",yref="paper",
                     x0=0.02,x1=0.32,y0=0.56,y1=0.90,
                     line=dict(color=border1_color,width=border1_width)),

                dict(type="rect",xref="paper",yref="paper",
                     x0=0.34,x1=0.64,y0=0.56,y1=0.90,
                     line=dict(color="#FFA500",width=3)),

                dict(type="rect",xref="paper",yref="paper",
                     x0=0.66,x1=0.96,y0=0.56,y1=0.90,
                     line=dict(color="lime",width=3)),
            ],

       annotations=[

    # -------- CAR 1 --------
    dict(x=0.17,y=0.88,text="<b>CAR 1 – AI</b>",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.17,y=0.84,text=f"Actual: {car1['speed']*3.6:.1f} km/h",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.17,y=0.80,text=f"Recommended: {rec1*3.6:.1f} km/h",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.17,y=0.76,text=f"Distance: {dist1:.1f} m",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.17,y=0.72,text=f"SOC: {car1['soc']:.1f} %",
         font=dict(color="red" if low_battery else "white"),
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.17,y=0.68,text=f"Fuel Saved: {fuel_saved_1:.3f} L",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.17,y=0.64,text=f"CO₂ Reduced: {emission_1:.3f} kg",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.17,y=0.60,
         text="⚡ LOW BATTERY<br>REQUESTING ASSIST"
              if low_battery and blink else "",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center",
         font=dict(size=11)),

    # -------- CAR 2 --------
    dict(x=0.49,y=0.88,text="<b>CAR 2 – BASELINE</b>",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.49,y=0.84,text=f"Actual: {car2['speed']*3.6:.1f} km/h",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.49,y=0.80,text="🛑 BRAKING" if stop else "",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center",
         font=dict(color="red")),

    # -------- CAR 3 --------
    dict(x=0.81,y=0.88,text="<b>CAR 3 – SUPPORT</b>",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.81,y=0.84,text=f"Actual: {car3['speed']*3.6:.1f} km/h",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.81,y=0.80,text=f"Recommended: {rec3*3.6:.1f} km/h",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.81,y=0.76,text=f"Distance: {dist3:.1f} m",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.81,y=0.72,text=f"SOC: {car3['soc']:.1f} %",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.81,y=0.68,text=f"Fuel Saved: {fuel_saved_3:.3f} L",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.81,y=0.64,text=f"CO₂ Reduced: {emission_3:.3f} kg",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center"),

    dict(x=0.81,y=0.60,
         text="🔋 REQUEST<br>ACCEPTED"
              if low_battery and blink else "",
         xref="paper",yref="paper",showarrow=False,
         align="center",xanchor="center",
         font=dict(size=11)),
]
        )
    ))

fig = go.Figure(
    data=frames[0].data,
    layout=go.Layout(
        xaxis=dict(range=[-300, road_length]),
        yaxis=dict(domain=[0.93, 1.0], visible=False),
        height=1050,
        title=" AI Cooperative GLOSA – ",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None,{"frame":{"duration":35},"fromcurrent":True}])])]
    ),
    frames=frames
)

st.plotly_chart(fig, use_container_width=True)
