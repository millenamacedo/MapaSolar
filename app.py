import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mapa de Irradiação Solar", layout="wide")
st.title("☀️ Mapa Interativo - Irradiação Solar Anual")

st.write("""
Este aplicativo exibe um mapa interativo com os níveis de irradiação solar anual, 
baseado em dados geográficos.  
Faça upload de um CSV com colunas: **LON**, **LAT**, **ANNUAL**.
""")

uploaded_file = st.file_uploader("📂 Faça upload do arquivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=None, engine="python")

        st.subheader("📋 Pré-visualização dos Dados")
        st.dataframe(df.head())

        if all(col in df.columns for col in ["LON", "LAT", "ANNUAL"]):

            # --- Legenda em formato de tabela ---
            st.markdown("""
            <div style="
                background-color: white;
                border: 2px solid grey;
                border-radius: 8px;
                width: 320px;
                padding: 10px;
                font-size: 15px;
                color: black;
                margin-bottom: 15px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.15);
            ">
            <b style="color:#003366;">Legenda - Irradiação (kWh/m²/ano)</b>
            <table style="width:100%; border-collapse:collapse; margin-top:8px;">
                <tr>
                    <td style="background:#313695; width:40px; height:18px; border-radius:3px;"></td>
                    <td>&lt; 4.000</td>
                </tr>
                <tr>
                    <td style="background:#74add1; width:40px; height:18px; border-radius:3px;"></td>
                    <td>4.000 – 4.199</td>
                </tr>
                <tr>
                    <td style="background:#fee090; width:40px; height:18px; border-radius:3px;"></td>
                    <td>4.200 – 4.399</td>
                </tr>
                <tr>
                    <td style="background:#fdae61; width:40px; height:18px; border-radius:3px;"></td>
                    <td>4.400 – 4.599</td>
                </tr>
                <tr>
                    <td style="background:#d73027; width:40px; height:18px; border-radius:3px;"></td>
                    <td>&ge; 4.600</td>
                </tr>
            </table>
            </div>
            """, unsafe_allow_html=True)

            # --- Cria o mapa ---
            m = folium.Map(location=[df["LAT"].mean(), df["LON"].mean()], zoom_start=5)

            # --- Mapeamento discreto de cores ---
            def cor_por_faixa(valor):
                try:
                    v = float(valor)
                except Exception:
                    return "#808080"
                if v < 4000:
                    return "#313695"
                elif v < 4200:
                    return "#74add1"
                elif v < 4400:
                    return "#fee090"
                elif v < 4600:
                    return "#fdae61"
                else:
                    return "#d73027"

            # --- Adiciona marcadores ---
            for _, row in df.iterrows():
                color = cor_por_faixa(row["ANNUAL"])
                folium.CircleMarker(
                    location=[row["LAT"], row["LON"]],
                    radius=6,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.8,
                    popup=f"Irradiação: {row['ANNUAL']} kWh/m²/ano"
                ).add_to(m)

            # --- Exibe o mapa ---
            st.subheader("🗺️ Mapa de Irradiação Solar")
            st_folium(m, width=1000, height=600)

        else:
            st.error("❌ O CSV deve conter as colunas: LON, LAT e ANNUAL.")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")
else:
    st.info("Por favor, faça o upload de um arquivo CSV contendo as colunas: LON, LAT e ANNUAL.")
