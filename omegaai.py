import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
import folium
from streamlit_folium import st_folium

# ================= PAGE CONFIG =================
st.set_page_config(page_title="OMEGA AI", layout="wide")

# ================= FUTURISTIC UI =================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f2027, #000000 70%);
    color: #e6f1ff;
}
.glass {
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(0,255,255,0.2);
}
.high { border-left: 6px solid #ff004c; }
.medium { border-left: 6px solid #ffaa00; }
.low { border-left: 6px solid #00ff99; }
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="glass">
    <h1>OMEGA AI</h1>
    <p>Predict • Prevent • Protect</p>
</div>
""", unsafe_allow_html=True)

# ================= CRIME DATA =================
data = pd.DataFrame({
    "Latitude": [28.6139, 28.7041, 28.5355, 28.4595, 28.4089],
    "Longitude": [77.2090, 77.1025, 77.3910, 77.0266, 77.3178],
    "CrimeType": ["Theft", "Robbery", "Assault", "Theft", "Robbery"],
    "Hour": [14, 22, 20, 11, 23]
})

crime_map = {"Theft": 0, "Robbery": 1, "Assault": 2}
data["CrimeEncoded"] = data["CrimeType"].map(crime_map)

# ================= AI MODEL =================
X = data[["Hour", "Latitude", "Longitude"]]
y = data["CrimeEncoded"]

ai_model = RandomForestClassifier(n_estimators=150, random_state=42)
ai_model.fit(X, y)

# ================= METRICS =================
total_crimes = len(data)
high_risk_crimes = (data["CrimeType"] == "Assault").sum()
night_crimes = data[data["Hour"] >= 20].shape[0]

# ================= LAYOUT =================
left, right = st.columns([1, 2])

# ================= LEFT PANEL =================
with left:
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.subheader("Crime Intelligence Snapshot")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Crimes", total_crimes)
    c2.metric("High Risk Crimes", high_risk_crimes)
    c3.metric("Night Crimes", night_crimes)

    st.markdown("---")
    st.subheader("Live AI Crime Risk Prediction")

    hour = st.slider("Hour of Day", 0, 23, 12)
    lat = st.number_input("Latitude", value=28.61)
    lon = st.number_input("Longitude", value=77.20)

    input_data = [[hour, lat, lon]]
    prediction = ai_model.predict(input_data)[0]
    probability = ai_model.predict_proba(input_data)[0]
    confidence = round(max(probability) * 100, 2)

    if prediction == 2:
        risk, css, msg = "HIGH", "high", "Immediate intervention required"
    elif prediction == 1:
        risk, css, msg = "MEDIUM", "medium", "Increase monitoring"
    else:
        risk, css, msg = "LOW", "low", "Normal patrol sufficient"

    st.markdown(f"""
    <div class="glass {css}">
        <h3>{risk} CRIME RISK</h3>
        <p>{msg}</p>
        <p><b>AI Confidence:</b> {confidence}%</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("AI Risk Meter")
    st.progress(confidence / 100)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Crime Data Table")
    st.dataframe(data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= RIGHT PANEL =================
with right:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Crime Hotspot Map")

    kmeans = KMeans(n_clusters=2, random_state=42)
    data["Zone"] = kmeans.fit_predict(data[["Latitude", "Longitude"]])

    crime_map = folium.Map(location=[28.61, 77.20], zoom_start=11)

    for _, row in data.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=9,
            color="red" if row["Zone"] == 1 else "green",
            fill=True,
            fill_opacity=0.8,
            popup=f"{row['CrimeType']} at {row['Hour']} hrs"
        ).add_to(crime_map)

    st_folium(crime_map, width=750, height=480)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("OMEGA AI | Predict • Prevent • Protect")
