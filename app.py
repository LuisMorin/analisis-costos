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
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Christmas_tree_with_gifts.svg/1200px-Christmas_tree_with_gifts.svg.png",
    caption="Árbol de Navidad 🎄",
    use_container_width=True
)

# Sección para ingresar datos
st.sidebar.header("🔧 Ingreso de Datos Reales 🎅")

# Ingresar datos reales
nivel_produccion = st.sidebar.number_input("Nivel de Producción (unidades)", value=20000, step=1000)
data_real = {
    "Elemento": ["Materia Prima", "Mano de Obra", "Cargos Indirectos Variables", "Cargos Indirectos Fijos"],
    "Cantidad Real": [
        st.sidebar.number_input("Cantidad Real - Materia Prima (litros)", value=32000, step=100),
        st.sidebar.number_input("Cantidad Real - Mano de Obra (HH)", value=48000, step=100),
        st.sidebar.number_input("Cantidad Real - Cargos Indirectos Variables (horas máquina)", value=26000, step=100),
        st.sidebar.number_input("Cantidad Real - Cargos Indirectos Fijos", value=88000, step=100),
    ],
    "Costo Unitario Real ($)": [
        st.sidebar.number_input("Costo Unitario Real - Materia Prima ($/litro)", value=10.20, step=0.1),
        st.sidebar.number_input("Costo Unitario Real - Mano de Obra ($/HH)", value=11.90, step=0.1),
        st.sidebar.number_input("Costo Unitario Real - Cargos Indirectos Variables ($/hora máquina)", value=2.40, step=0.1),
        st.sidebar.number_input("Costo Unitario Real - Cargos Indirectos Fijos ($)", value=4.00, step=0.1),
    ]
}

df_real = pd.DataFrame(data_real)
df_real["Costo Total Real ($)"] = df_real["Cantidad Real"] * df_real["Costo Unitario Real ($)"]

# Datos estándar predefinidos
data_estandar = {
    "Elemento": ["Materia Prima", "Mano de Obra", "Cargos Indirectos Variables", "Cargos Indirectos Fijos"],
    "Requerimiento Unitario": [1.5, 2.5, 1.5, 1.5],
    "Costo Unitario Estándar ($)": [10, 12, 2, 4.5],
}

df_estandar = pd.DataFrame(data_estandar)
df_estandar["Costo Total Estándar ($)"] = df_estandar["Requerimiento Unitario"] * nivel_produccion

# Cédula I: Hoja de Costo Unitario Estándar
df_cedula_i = df_estandar.copy()
df_cedula_i["Costo Unitario Total ($)"] = df_cedula_i["Requerimiento Unitario"] * df_cedula_i["Costo Unitario Estándar ($)"]

# Cédula II: Valuación de Producción Terminada
total_prod_terminada = st.sidebar.number_input("Unidades de Producción Terminada", value=16000, step=1000)
df_cedula_ii = df_estandar.copy()
df_cedula_ii["Requerimiento Total"] = df_cedula_ii["Requerimiento Unitario"] * total_prod_terminada
df_cedula_ii["Costo Total Producción Terminada ($)"] = df_cedula_ii["Requerimiento Total"] * df_cedula_ii["Costo Unitario Estándar ($)"]

# Cédula III: Inventario Final en Proceso
total_prod_proceso = st.sidebar.number_input("Unidades en Proceso", value=6000, step=1000)
df_cedula_iii = df_estandar.copy()
df_cedula_iii["Requerimiento Total"] = df_cedula_iii["Requerimiento Unitario"] * total_prod_proceso
df_cedula_iii["Avance Proceso (%)"] = [1, 0.5, 0.33, 0.33]
df_cedula_iii["Costo Total Inventario Proceso ($)"] = (
    df_cedula_iii["Requerimiento Total"] * df_cedula_iii["Costo Unitario Estándar ($)"] * df_cedula_iii["Avance Proceso (%)"]
)

# Cédula IV: Informe de Desviaciones
df_cedula_iv = df_real.copy()
df_cedula_iv["Costo Total Estándar ($)"] = df_estandar["Costo Total Estándar ($)"]
df_cedula_iv["Desviación ($)"] = df_cedula_iv["Costo Total Real ($)"] - df_cedula_iv["Costo Total Estándar ($)"]
df_cedula_iv["Tipo"] = df_cedula_iv["Desviación ($)"].apply(lambda x: "FAVORABLE" if x < 0 else "DESFAVORABLE")

# Cédula V: Valuación de Ventas y Costo de lo Vendido
precio_venta = st.sidebar.number_input("Precio de Venta por Unidad ($)", value=100.0, step=0.5)
unidades_vendidas = st.sidebar.number_input("Unidades Vendidas", value=10000, step=1000)
df_cedula_v = pd.DataFrame({
    "Unidades Vendidas": [unidades_vendidas],
    "Precio de Venta ($)": [precio_venta],
    "Ingresos Totales ($)": [unidades_vendidas * precio_venta],
    "Costo Unitario Producción ($)": [df_cedula_ii["Costo Total Producción Terminada ($)"].sum() / total_prod_terminada],
    "Costo Total Vendido ($)": [(df_cedula_ii["Costo Total Producción Terminada ($)"].sum() / total_prod_terminada) * unidades_vendidas]
})

# Datos farmacéuticos: Paracetamol
st.markdown("<div class='section-title'>📋 Cédulas para Producto: Paracetamol</div>", unsafe_allow_html=True)

# Cédula 1: Hoja de Costo Unitario
data_cedula_1 = {
    "Elemento": ["MP", "MOD", "CIV", "CIF"],
    "Cantidad": [20, 1.5, 3, 3],
    "Costo Unitario ($)": [3, 20, 4, 5],
    "Costo Total ($)": [60, 30, 12, 15],
}
df_cedula_1 = pd.DataFrame(data_cedula_1)
st.markdown("<div class='section-title'>📋 Cédula 1: Hoja de Costo Unitario</div>", unsafe_allow_html=True)
st.dataframe(df_cedula_1.style.format({"Cantidad": "{:.1f}", "Costo Unitario ($)": "${:.2f}", "Costo Total ($)": "${:.2f}"}))

# Cédula 2: Valuación de Producción Terminada
unidades_terminadas = 70000
data_cedula_2 = {
    "Elemento": ["MP", "MOD", "CIV", "CIF"],
    "Cantidad Total": [20 * unidades_terminadas, 2 * unidades_terminadas, 5 * unidades_terminadas, 5 * unidades_terminadas],
    "Costo Unitario ($)": [3, 20, 4, 5],
    "Costo Total ($)": [1400000, 1400000, 350000, 350000],
}
df_cedula_2 = pd.DataFrame(data_cedula_2)
st.markdown("<div class='section-title'>📋 Cédula 2: Producción Terminada</div>", unsafe_allow_html=True)
st.dataframe(df_cedula_2.style.format({"Cantidad Total": "{:.0f}", "Costo Unitario ($)": "${:.2f}", "Costo Total ($)": "${:.2f}"}))

# Cédula 3: Inventario Final en Proceso
unidades_proceso = 18000
data_cedula_3 = {
    "Elemento": ["MP", "MOD", "CIV", "CIF"],
    "Cantidad Total": [20 * unidades_proceso, 2 * unidades_proceso, 5 * unidades_proceso, 5 * unidades_proceso],
    "Costo Unitario ($)": [3, 20, 4, 5],
    "Costo Total ($)": [360000, 360000, 90000, 90000],
}
df_cedula_3 = pd.DataFrame(data_cedula_3)
st.markdown("<div class='section-title'>📋 Cédula 3: Inventario Final en Proceso</div>", unsafe_allow_html=True)
st.dataframe(df_cedula_3.style.format({"Cantidad Total": "{:.0f}", "Costo Unitario ($)": "${:.2f}", "Costo Total ($)": "${:.2f}"}))

# Costos reales
data_costos_reales = {
    "Elemento": ["MP", "MOD", "CIV", "CIF"],
    "Costo Real ($)": [19.6, 2.4, 5.2, 4.7],
}
df_costos_reales = pd.DataFrame(data_costos_reales)
st.markdown("<div class='section-title'>📋 Costos Reales</div>", unsafe_allow_html=True)
st.dataframe(df_costos_reales.style.format({"Costo Real ($)": "${:.2f}"}))

# Mostrar tablas
st.markdown("<div class='section-title'>📋 Cédula I: Hoja de Costo Unitario Estándar</div>", unsafe_allow_html=True)
st.dataframe(df_cedula_i.style.format({
    "Requerimiento Unitario": "{:.2f}",
    "Costo Unitario Estándar ($)": "${:.2f}",
    "Costo Unitario Total ($)": "${:.2f}"
}))

st.markdown("<div class='section-title'>📋 Cédula II: Valuación de Producción Terminada</div>", unsafe_allow_html=True)
st.dataframe(df_cedula_ii.style.format({
    "Requerimiento Total": "{:.2f}",
    "Costo Total Producción Terminada ($)": "${:.2f}"
}))

st.markdown("<div class='section-title'>📋 Cédula III: Inventario Final en Proceso</div>", unsafe_allow_html=True)
st.dataframe(df_cedula_iii.style.format({
    "Requerimiento Total": "{:.2f}",
    "Avance Proceso (%)": "{:.2%}",
    "Costo Total Inventario Proceso ($)": "${:.2f}"
}))

st.markdown("<div class='section-title'>📋 Cédula IV: Informe de Desviaciones</div>", unsafe_allow_html=True)
st.dataframe(df_cedula_iv.style.format({
    "Cantidad Real": "{:.0f}",
    "Costo Total Real ($)": "${:.2f}",
    "Costo Total Estándar ($)": "${:.2f}",
    "Desviación ($)": "${:.2f}"
}))

st.markdown("<div class='section-title'>📋 Cédula V: Ventas y Costo de lo Vendido</div>", unsafe_allow_html=True)
st.dataframe(df_cedula_v.style.format({
    "Unidades Vendidas": "{:.0f}",
    "Precio de Venta ($)": "${:.2f}",
    "Ingresos Totales ($)": "${:.2f}",
    "Costo Unitario Producción ($)": "${:.2f}",
    "Costo Total Vendido ($)": "${:.2f}"
}))

# Visualización de Gráficos
st.markdown("<div class='section-title'>📈 Visualización de Desviaciones</div>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df_real["Elemento"], df_real["Costo Total Real ($)"] - df_estandar["Costo Total Estándar ($)"],
       color=["green" if x < 0 else "red" for x in df_real["Costo Total Real ($)"] - df_estandar["Costo Total Estándar ($)"]])
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

csv_cedula_i = convert_df_to_csv(df_cedula_i)
csv_cedula_ii = convert_df_to_csv(df_cedula_ii)
csv_cedula_iii = convert_df_to_csv(df_cedula_iii)
csv_cedula_iv = convert_df_to_csv(df_cedula_iv)
csv_cedula_v = convert_df_to_csv(df_cedula_v)

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

st.sidebar.download_button(
    label="📥 Descargar Cédula V (CSV)",
    data=csv_cedula_v,
    file_name="cedula_v.csv",
    mime="text/csv",
)

# Mensaje navideño
st.markdown("<div class='main-title'>🎅 ¡Feliz Navidad y próspero análisis de costos! 🎁</div>", unsafe_allow_html=True)
