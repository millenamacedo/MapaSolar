import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from branca.element import Template, MacroElement

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

            # --- Cria o mapa ---
            m = folium.Map(location=[df["LAT"].mean(), df["LON"].mean()], zoom_start=5)

            # --- Mapeamento discreto de cores por faixa ---
            def cor_por_faixa(valor):
                try:
                    v = float(valor)
                except Exception:
                    return "#808080"  # cinza para valores inválidos
                if v < 4000:
                    return "#313695"   # azul escuro
                elif v < 4200:
                    return "#74add1"   # azul claro / transição
                elif v < 4400:
                    return "#fee090"   # amarelo claro
                elif v < 4600:
                    return "#fdae61"   # laranja
                else:
                    return "#d73027"   # vermelho (valores mais altos)

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

            # --- Legenda incorporada no mapa ---
            legend_template = """
            {% macro html(this, kwargs) %}
            <div style="
                position: fixed;
                bottom: 50px;
                left: 50px;
                width: 260px;
                background-color: white;
                border:2px solid grey;
                z-index:9999;
                font-size:14px;
                padding: 10px;
                border-radius: 8px;
                color: black;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
            ">
            <b style="color:#003366;">Legenda - Irradiação (kWh/m²/ano)</b><br><br>

            <div style="display:flex;align-items:center;margin-bottom:6px;">
                <div style="background:#313695;width:24px;height:18px;margin-right:8px;border-radius:3px;"></div>
                <div>&lt; 4.000</div>
            </div>
            <div style="display:flex;align-items:center;margin-bottom:6px;">
                <div style="background:#74add1;width:24px;height:18px;margin-right:8px;border-radius:3px;"></div>
                <div>4.000 – 4.199</div>
            </div>
            <div style="display:flex;align-items:center;margin-bottom:6px;">
                <div style="background:#fee090;width:24px;height:18px;margin-right:8px;border-radius:3px;"></div>
                <div>4.200 – 4.399</div>
            </div>
            <div style="display:flex;align-items:center;margin-bottom:6px;">
                <div style="background:#fdae61;width:24px;height:18px;margin-right:8px;border-radius:3px;"></div>
                <div>4.400 – 4.599</div>
            </div>
            <div style="display:flex;align-items:center;">
                <div style="background:#d73027;width:24px;height:18px;margin-right:8px;border-radius:3px;"></div>
                <div>&ge; 4.600</div>
            </div>
            </div>
            {% endmacro %}
            """

            legend = MacroElement()
            legend._template = Template(legend_template)
            m.get_root().add_child(legend)

            # --- Exibe o mapa ---
            st.subheader("🗺️ Mapa de Irradiação Solar")
            st_folium(m, width=1000, height=600)

        else:
            st.error("❌ O CSV deve conter as colunas: LON, LAT e ANNUAL.")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")
else:
    st.info("Por favor, faça o upload de um arquivo CSV contendo as colunas: LON, LAT e ANNUAL.")
