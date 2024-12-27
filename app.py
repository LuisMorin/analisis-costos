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

# Sección para ingresar datos
st.sidebar.header("🔧 Ingreso de Datos Reales 🎅")

# Ingreso y modificación de datos reales
def obtener_datos_usuario():
    datos = {
        "Elemento": ["MP", "MOD", "CIV", "CIF"],
        "Cantidad": [
            st.sidebar.number_input("Cantidad - Materia Prima (MP)", value=20, step=1),
            st.sidebar.number_input("Cantidad - Mano de Obra (MOD)", value=1.5, step=0.1),
            st.sidebar.number_input("Cantidad - Cargos Indirectos Variables (CIV)", value=3, step=1),
            st.sidebar.number_input("Cantidad - Cargos Indirectos Fijos (CIF)", value=3, step=1),
        ],
        "Costo Unitario ($)": [
            st.sidebar.number_input("Costo Unitario - Materia Prima (MP)", value=3.0, step=0.1),
            st.sidebar.number_input("Costo Unitario - Mano de Obra (MOD)", value=20.0, step=0.1),
            st.sidebar.number_input("Costo Unitario - Cargos Indirectos Variables (CIV)", value=4.0, step=0.1),
            st.sidebar.number_input("Costo Unitario - Cargos Indirectos Fijos (CIF)", value=5.0, step=0.1),
        ]
    }
    return pd.DataFrame(datos)

data_real = obtener_datos_usuario()
data_real["Costo Total ($)"] = data_real["Cantidad"] * data_real["Costo Unitario ($)"]

# Mostrar datos iniciales modificables
st.markdown("<div class='section-title'>📋 Datos Reales Modificables</div>", unsafe_allow_html=True)
st.dataframe(data_real.style.format({
    "Cantidad": "{:.1f}",
    "Costo Unitario ($)": "${:.2f}",
    "Costo Total ($)": "${:.2f}"
}))

# Cédula I: Hoja de Costo Unitario Estándar
st.markdown("<div class='section-title'>📋 Cédula I: Hoja de Costo Unitario Estándar</div>", unsafe_allow_html=True)
data_cedula_i = data_real.copy()
data_cedula_i.rename(columns={"Cantidad": "Requerimiento Unitario"}, inplace=True)
st.dataframe(data_cedula_i.style.format({
    "Requerimiento Unitario": "{:.1f}",
    "Costo Unitario ($)": "${:.2f}",
    "Costo Total ($)": "${:.2f}"
}))

# Cédula II: Valuación de Producción Terminada
unidades_terminadas = st.sidebar.number_input("Unidades de Producción Terminada", value=70000, step=1000)
data_cedula_ii = data_cedula_i.copy()
data_cedula_ii["Requerimiento Total"] = data_cedula_ii["Requerimiento Unitario"] * unidades_terminadas
data_cedula_ii["Costo Total Producción Terminada ($)"] = data_cedula_ii["Requerimiento Total"] * data_cedula_ii["Costo Unitario ($)"]

st.markdown("<div class='section-title'>📋 Cédula II: Valuación de Producción Terminada</div>", unsafe_allow_html=True)
st.dataframe(data_cedula_ii.style.format({
    "Requerimiento Total": "{:.0f}",
    "Costo Total Producción Terminada ($)": "${:.2f}"
}))

# Cédula III: Inventario Final en Proceso
unidades_proceso = st.sidebar.number_input("Unidades en Proceso", value=18000, step=1000)
data_cedula_iii = data_cedula_i.copy()
data_cedula_iii["Requerimiento Total"] = data_cedula_iii["Requerimiento Unitario"] * unidades_proceso
data_cedula_iii["Avance Proceso (%)"] = [1, 0.5, 0.33, 0.33]
data_cedula_iii["Costo Total Inventario Proceso ($)"] = (
    data_cedula_iii["Requerimiento Total"] * data_cedula_iii["Costo Unitario ($)"] * data_cedula_iii["Avance Proceso (%)"]
)

st.markdown("<div class='section-title'>📋 Cédula III: Inventario Final en Proceso</div>", unsafe_allow_html=True)
st.dataframe(data_cedula_iii.style.format({
    "Requerimiento Total": "{:.0f}",
    "Avance Proceso (%)": "{:.2%}",
    "Costo Total Inventario Proceso ($)": "${:.2f}"
}))

# Cédula IV: Informe de Desviaciones
data_cedula_iv = data_cedula_i.copy()
data_cedula_iv["Costo Unitario Real ($)"] = [19.6, 2.4, 5.2, 4.7]
data_cedula_iv["Desviación ($)"] = data_cedula_iv["Costo Unitario Real ($)"] - data_cedula_iv["Costo Unitario ($)"]
data_cedula_iv["Tipo"] = data_cedula_iv["Desviación ($)"].apply(lambda x: "FAVORABLE" if x < 0 else "DESFAVORABLE")

st.markdown("<div class='section-title'>📋 Cédula IV: Informe de Desviaciones</div>", unsafe_allow_html=True)
st.dataframe(data_cedula_iv.style.format({
    "Costo Unitario Real ($)": "${:.2f}",
    "Costo Unitario ($)": "${:.2f}",
    "Desviación ($)": "${:.2f}"
}))

# Visualización de Desviaciones
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(data_cedula_iv["Elemento"], data_cedula_iv["Desviación ($)"],
       color=["green" if x < 0 else "red" for x in data_cedula_iv["Desviación ($)"]])
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_title("Desviaciones por Elemento", fontsize=14, color="#B22222")
ax.set_ylabel("Desviación ($)", fontsize=12, color="#B22222")
ax.set_xlabel("Elemento", fontsize=12, color="#B22222")
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)

# Exportar resultados
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_cedula_i = convert_df_to_csv(data_cedula_i)
csv_cedula_ii = convert_df_to_csv(data_cedula_ii)
csv_cedula_iii = convert_df_to_csv(data_cedula_iii)
csv_cedula_iv = convert_df_to_csv(data_cedula_iv)

st.sidebar.download_button(
    label="📥 Descargar Cédula I (CSV)",
    data=csv_cedula_i,
    file_name="cedula_i.csv",
    mime="text/csv",
)

st.sidebar.download_button(
    label="📥 Descargar Cédula II (CSV)",
    data=csv_cedula_ii,
    file_name="cedula_ii.csv",
    mime="text/csv",
)

st.sidebar.download_button(
    label="📥 Descargar Cédula III (CSV)",
    data=csv_cedula_iii,
    file_name="cedula_iii.csv",
    mime="text/csv",
)

st.sidebar.download_button(
    label="📥 Descargar Cédula IV (CSV)",
    data=csv_cedula_iv,
    file_name="cedula_iv.csv",
    mime="text/csv",
)

# Mensaje navideño
st.markdown("<div class='main-title'>🎅 ¡Feliz Navidad y próspero análisis de costos! 🎁</div>", unsafe_allow_html=True)

