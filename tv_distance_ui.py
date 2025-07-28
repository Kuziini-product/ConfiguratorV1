
import streamlit as st
import openpyxl
from openpyxl import load_workbook
import io

# Constante
INCH_CM = 2.54
RAPORT_16_9 = (16 / ((16**2 + 9**2)**0.5), 9 / ((16**2 + 9**2)**0.5))

def calculeaza_diagonala(d_m):
    return round(d_m * 39.37 * 0.84)

def dimensiuni_televizor(diagonala_inch):
    diagonala_cm = diagonala_inch * INCH_CM
    latime = diagonala_cm * RAPORT_16_9[0]
    inaltime = diagonala_cm * RAPORT_16_9[1]
    return round(latime / 100, 2), round(inaltime / 100, 2)

# Selector limbă cu emoji steag
LANG = st.sidebar.selectbox("🌍 Language / Limba", ["🇷🇴 Română", "🇬🇧 English"])
IS_RO = LANG == "🇷🇴 Română"

# Texte dinamice
TXT = {
    "title": "📐 Configurator diagonala TV în funcție de distanță" if IS_RO else "📐 TV Diagonal Configurator by Viewing Distance",
    "distance_label": "📏 Alege distanța de vizionare (m)" if IS_RO else "📏 Choose viewing distance (m)",
    "export_button": "💾 Exportă în Excel cu aceste valori" if IS_RO else "💾 Export to Excel with these values",
    "download_label": "📥 Descarcă fișierul Excel actualizat" if IS_RO else "📥 Download updated Excel file",
    "recommend": "Kuziini recomandă" if IS_RO else "Kuziini recommends",
    "for_distance": "pentru distanța de" if IS_RO else "for a viewing distance of",
    "size": "lățime" if IS_RO else "width",
    "height": "înălțime" if IS_RO else "height",
    "tv_models": "📺 Modele TV recomandate" if IS_RO else "📺 Recommended TV Models",
    "see_on_samsung": "🔗 Vezi pe Samsung" if IS_RO else "🔗 View on Samsung"
}

# Config pagină
st.set_page_config(page_title="Kuziini TV Configurator", layout="wide")
st.image("Kuziini_logo_negru.png", width=320)
st.markdown(f"<h2 style='text-align:center; color:black;'>{TXT['title']}</h2>", unsafe_allow_html=True)

wb = load_workbook("www.xlsx", data_only=True)
ws = wb.active

col1, col2 = st.columns([1, 1])

with col1:
    distanta = st.slider(TXT["distance_label"], 1.0, 5.0, 2.5, 0.1)
    diagonala_inch = calculeaza_diagonala(distanta)
    latime_m, inaltime_m = dimensiuni_televizor(diagonala_inch)

    st.markdown(f"""
    <div style='background-color:#F0F9FF;padding:1.5rem;border-radius:12px;
                border:2px solid #0B5394;text-align:center;'>
        <h1 style='color:#FF5722;font-size:3rem;'>{diagonala_inch}"</h1>
        <h3 style='color:#0B5394;'>{TXT['recommend']}</h3>
        <p>{TXT['for_distance']} {distanta} m</p>
        <p style='font-weight:bold;'>🖼️ {TXT['size']} {latime_m} m × {TXT['height']} {inaltime_m} m</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(TXT["export_button"]):
        ws["B1"] = distanta
        ws["B6"] = round(distanta / 30, 2)
        ws["B7"] = round(distanta / 25, 2)
        output = io.BytesIO()
        wb.save(output)
        st.download_button(TXT["download_label"], output.getvalue(), "recomandare_tv_actualizat.xlsx")

    st.markdown(f"<h4 style='margin-top:2rem;'>{TXT['tv_models']}</h4>", unsafe_allow_html=True)

    if diagonala_inch > 55:
        model_1 = {
            "name": "Samsung QN85C",
            "link": "https://www.samsung.com/ro/tvs/neo-qled-4k/qe55qn85catxxh/",
            "features": {
                "Neo QLED": True,
                "Mini LED": True,
                "Quantum HDR": True,
                "Dolby Atmos": False
            }
        }
        model_2 = {
            "name": "Samsung QN90B",
            "link": "https://www.samsung.com/ro/tvs/qled-tv/qn90b-neo-qled-4k-smart-tv/",
            "features": {
                "Neo QLED": True,
                "Mini LED": True,
                "Quantum HDR": True,
                "Dolby Atmos": True
            }
        }

        f1, f2 = st.columns(2)

        with f1:
            st.markdown(f"### {model_1['name']}")
            st.markdown(f"[{TXT['see_on_samsung']}]({model_1['link']})")
            for feat in model_1["features"]:
                icon = "✅" if model_1["features"][feat] else "🔴"
                st.markdown(f"{icon} {feat}")

        with f2:
            st.markdown(f"### {model_2['name']}")
            st.markdown(f"[{TXT['see_on_samsung']}]({model_2['link']})")
            for feat in model_2["features"]:
                icon = "✅" if model_2["features"][feat] else "🔴"
                st.markdown(f"{icon} {feat}")
    else:
        st.info("📺 Modelele comparabile sunt afișate pentru diagonale peste 55".")

with col2:
    st.image("TV.png", caption="Kuziini × Samsung", use_container_width=True)
    st.markdown("<p style='text-align:center;font-weight:bold;color:black;'>Living Kuziini × Samsung</p>", unsafe_allow_html=True)
