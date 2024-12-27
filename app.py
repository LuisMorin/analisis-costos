import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial de la página
st.set_page_config(page_title="Análisis de Costos Navideño", layout="wide", page_icon="🎄")

# Estilo personalizado para Navidad
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #B22222;
            text-align: center;
            background-color: #FFFAF0;
            padding: 10px;
            border-radius: 10px;
        }
        .section-title {
            font-size: 1.75rem;
            font-weight: bold;
            margin-top: 20px;
            color: #228B22;
            border-bottom: 2px solid #228B22;
            padding-bottom: 5px;
        }
        body {
            background-color: #F5F5F5;
        }
        .sidebar .sidebar-content {
            background-color: #FFFACD;
        }
        .highlight {
            background-color: #FFD700;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Encabezado navideño
st.markdown("<div class='main-title'>🎄 Análisis de Costos con Espíritu Navideño 🎁</div>", unsafe_allow_html=True)

# Agregar imagen navideña
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Christmas_tree.svg/1200px-Christmas_tree.svg.png", caption="Árbol de Navidad 🎄", use_column_width="always")

# Datos del Paracetamol
st.markdown("<div class='section-title'>📋 Cédulas para Producto: Paracetamol</div>", unsafe_allow_html=True)

# Cédula I: Hoja de Costo Unitario Estándar
data_cedula_i = {
    "Elemento": ["MP", "MOD", "CIV", "CIF"],
    "Requerimiento Unitario": [20, 1.5, 3, 3],
    "Costo Unitario Estándar ($)": [3, 20, 4, 5]
}

cedula_i = pd.DataFrame(data_cedula_i)
cedula_i["Costo Unitario Total ($)"] = cedula_i["Requerimiento Unitario"] * cedula_i["Costo Unitario Estándar ($)"]

st.markdown("<div class='section-title'>📋 Cédula I: Hoja de Costo Unitario Estándar</div>", unsafe_allow_html=True)
st.dataframe(cedula_i.style.format({
    "Requerimiento Unitario": "{:.2f}",
    "Costo Unitario Estándar ($)": "${:.2f}",
    "Costo Unitario Total ($)": "${:.2f}"
}))

# Cédula II: Valuación de Producción Terminada
data_cedula_ii = cedula_i.copy()
data_cedula_ii["Requerimiento Total"] = data_cedula_ii["Requerimiento Unitario"] * 70000
data_cedula_ii["Costo Total Producción Terminada ($)"] = data_cedula_ii["Requerimiento Total"] * data_cedula_ii["Costo Unitario Estándar ($)"]

st.markdown("<div class='section-title'>📋 Cédula II: Valuación de Producción Terminada</div>", unsafe_allow_html=True)
st.dataframe(data_cedula_ii.style.format({
    "Requerimiento Total": "{:.0f}",
    "Costo Total Producción Terminada ($)": "${:.2f}"
}))

# Cédula III: Inventario Final en Proceso
data_cedula_iii = cedula_i.copy()
data_cedula_iii["Requerimiento Total"] = data_cedula_iii["Requerimiento Unitario"] * 18000
data_cedula_iii["Avance Proceso (%)"] = [1, 0.5, 0.33, 0.33]
data_cedula_iii["Costo Total Inventario Proceso ($)"] = (
    data_cedula_iii["Requerimiento Total"] * data_cedula_iii["Costo Unitario Estándar ($)"] * data_cedula_iii["Avance Proceso (%)"]
)

st.markdown("<div class='section-title'>📋 Cédula III: Inventario Final en Proceso</div>", unsafe_allow_html=True)
st.dataframe(data_cedula_iii.style.format({
    "Requerimiento Total": "{:.0f}",
    "Avance Proceso (%)": "{:.2%}",
    "Costo Total Inventario Proceso ($)": "${:.2f}"
}))

# Cédula IV: Informe de Desviaciones
data_cedula_iv = {
    "Elemento": ["MP", "MOD", "CIV", "CIF"],
    "Costo Unitario Real ($)": [19.6, 2.4, 5.2, 4.7],
    "Costo Unitario Estándar ($)": [3, 20, 4, 5]
}

cedula_iv = pd.DataFrame(data_cedula_iv)
cedula_iv["Desviación ($)"] = cedula_iv["Costo Unitario Real ($)"] - cedula_iv["Costo Unitario Estándar ($)"]
cedula_iv["Tipo"] = cedula_iv["Desviación ($)"].apply(lambda x: "FAVORABLE" if x < 0 else "DESFAVORABLE")

st.markdown("<div class='section-title'>📋 Cédula IV: Informe de Desviaciones</div>", unsafe_allow_html=True)
st.dataframe(cedula_iv.style.format({
    "Costo Unitario Real ($)": "${:.2f}",
    "Costo Unitario Estándar ($)": "${:.2f}",
    "Desviación ($)": "${:.2f}"
}))

# Visualización de Desviaciones
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(cedula_iv["Elemento"], cedula_iv["Desviación ($)"],
       color=["green" if x < 0 else "red" for x in cedula_iv["Desviación ($)"]])
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_title("Desviaciones por Elemento", fontsize=14, color="#B22222")
ax.set_ylabel("Desviación ($)", fontsize=12, color="#B22222")
ax.set_xlabel("Elemento", fontsize=12, color="#B22222")
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)
