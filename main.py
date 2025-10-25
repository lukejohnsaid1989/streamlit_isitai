import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import hashlib

# --- Streamlit setup
st.set_page_config(page_title="Traffic Accident Extractor (demo)", layout="wide")
st.title("📰 LocalNews — Headline Analyzer (demo)")
st.caption("Enter a news headline. If it's about a traffic accident in a Maltese village, the village will be shown on a map.")

# --- Database of Maltese villages/towns (simplified)
VILLAGES = {
    # --- Main Island (Malta) ---
    "valletta": (35.8989, 14.5146),
    "birkirkara": (35.8796, 14.4610),
    "qormi": (35.8763, 14.4622),
    "mosta": (35.8986, 14.4426),
    "sliema": (35.9126, 14.5040),
    "san gwann": (35.9050, 14.4750),
    "san ġwann": (35.9050, 14.4750),
    "st. julian's": (35.9121, 14.4885),
    "st julians": (35.9121, 14.4885),
    "st. paul's bay": (35.9363, 14.3850),
    "st pauls bay": (35.9363, 14.3850),
    "naxxar": (35.9120, 14.4150),
    "għargħur": (35.9169, 14.4310),
    "attard": (35.8895, 14.4428),
    "balzan": (35.8890, 14.4570),
    "lija": (35.8952, 14.4476),
    "mdina": (35.8869, 14.4007),
    "rabat": (35.8855, 14.4039),
    "dingli": (35.8767, 14.3754),
    "siggiewi": (35.8469, 14.4364),
    "siġġiewi": (35.8469, 14.4364),
    "mqabba": (35.8446, 14.4423),
    "qrendi": (35.8412, 14.4606),
    "zebbug": (35.8781, 14.3904),
    "żebbuġ": (35.8781, 14.3904),
    "luqa": (35.8589, 14.4885),
    "paola": (35.8614, 14.5033),
    "tarxien": (35.8573, 14.5158),
    "fgura": (35.8700, 14.5200),
    "marsaskala": (35.8611, 14.5653),
    "marsaxlokk": (35.8380, 14.5350),
    "zejtun": (35.8522, 14.5351),
    "żejtun": (35.8522, 14.5351),
    "birzebbuga": (35.8289, 14.5325),
    "birżebbuġa": (35.8289, 14.5325),
    "santa lucija": (35.8530, 14.5100),
    "gudja": (35.8443, 14.4948),
    "ghaxaq": (35.8447, 14.5162),
    "għaxaq": (35.8447, 14.5162),
    "kirkop": (35.8417, 14.4850),
    "mqabba": (35.8446, 14.4423),
    "zurrieq": (35.8314, 14.4748),
    "żurrieq": (35.8314, 14.4748),
    "hamrun": (35.8860, 14.4933),
    "ħaġar qim": (35.8303, 14.4470),
    "bormla": (35.8856, 14.5262),
    "cospicua": (35.8856, 14.5262),
    "senglea": (35.8878, 14.5169),
    "isla": (35.8878, 14.5169),
    "birgu": (35.8874, 14.5214),
    "vittoriosa": (35.8874, 14.5214),
    "pieta": (35.8933, 14.4957),
    "gzira": (35.9051, 14.4951),
    "msida": (35.9040, 14.4920),
    "ta' xbiex": (35.8990, 14.4980),
    "swieqi": (35.9194, 14.4753),
    "safi": (35.8333, 14.4833),
    "marsa": (35.8715, 14.4950),

    # --- Gozo Island ---
    "victoria": (36.0447, 14.2510),
    "rabat (gozo)": (36.0447, 14.2510),
    "xewkija": (36.0369, 14.2583),
    "ghajnsielem": (36.0250, 14.2778),
    "għajnsielem": (36.0250, 14.2778),
    "nadur": (36.0445, 14.2945),
    "qala": (36.0372, 14.3088),
    "munxar": (36.0280, 14.2375),
    "sannat": (36.0245, 14.2478),
    "xaghra": (36.0544, 14.2675),
    "xagħra": (36.0544, 14.2675),
    "ghasri": (36.0612, 14.2267),
    "għasri": (36.0612, 14.2267),
    "kerċem": (36.0405, 14.2357),
    "kercem": (36.0405, 14.2357),
    "għarb": (36.0600, 14.2088),
    "gharb": (36.0600, 14.2088),
    "san lawrenz": (36.0555, 14.2048),
    "santa lucija (gozo)": (36.0370, 14.2365),
    "marsalforn": (36.0693, 14.2640),
}

ACCIDENT_KEYWORDS = [
    "accident", "crash", "collision", "road traffic", "pile-up", "vehicle", "hit", "hit-and-run",
    "road crash", "car crash", "traffic accident", "bus crash", "truck crash", "fatal", "injured",
    "injury", "killed", "dies", "dead", "serious injuries", "serious injury"
]

# --- Input box
headline = st.text_input("🧾 News headline", value="")

# --- Helpers
def contains_accident_keyword(text: str):
    text = text.lower()
    return any(kw in text for kw in ACCIDENT_KEYWORDS)

def find_village_in_text(text: str):
    text = text.lower()
    for name in VILLAGES.keys():
        if name in text:
            return name
    return None

# --- Run button
if st.button("🚀 Run LocalNews Analysis"):
    if not headline.strip():
        st.warning("Please enter a headline first.")
    else:
        headline_norm = headline.lower().strip()
        is_accident = contains_accident_keyword(headline_norm)
        village = find_village_in_text(headline_norm)

        # fake confidence using md5 hash
        h = hashlib.md5(headline_norm.encode("utf-8")).hexdigest()
        conf = (int(h[:8], 16) % 61) + 40  # 40–100
        st.success(f"✅ LocalNews analysis complete — confidence: {conf}%")

        if is_accident and village:
            lat, lon = VILLAGES[village]
            st.markdown(f"**Detected:** Traffic accident near **{village.title()}** 🇲🇹")

            # Create map with red marker and blue text above it
            fig = go.Figure()

            # Red marker
            fig.add_trace(go.Scattermapbox(
                lat=[lat],
                lon=[lon],
                mode="markers+text",
                marker=dict(size=50, color="red", opacity=0.85),
                text=["🚨 Accident detected here"],
                textfont=dict(color="green", size=40),
                textposition="top center",
                hovertext=[village.title()],
                hoverinfo="text",
            ))

            # Zoomed in twice (roughly)
            fig.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    center=dict(lat=lat, lon=lon),
                    zoom=13,  # was 12, doubled zoom
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=600,
            )

            st.plotly_chart(fig, use_container_width=True)

        elif is_accident:
            st.info("Traffic accident detected, but no Maltese village name found.")
            fig = go.Figure(go.Scattermapbox(
                lat=[35.9375],
                lon=[14.3754],
                mode="markers+text",
                marker=dict(size=18, color="red", opacity=0.85),
                text=["Possible accident in Malta"],
                textfont=dict(color="blue", size=14),
                textposition="top center",
            ))
            fig.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    center=dict(lat=35.9375, lon=14.3754),
                    zoom=10,
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No traffic accident or Maltese village detected in the headline.")

# --- Example headlines
st.markdown("---")
st.subheader("🧪 Try these examples:")
examples = [
    "Two cars crash near Birgu — several injured",
    "Minor collision in Zurrieq  causes traffic delays",
    "Bus and truck collision leaves one killed in Rabat",
    "Sports update: Local team wins cup",
]
for ex in examples:
    st.code(ex, language="text")
