import streamlit as st
from supabase import create_client, Client
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar Supabase
SUPABASE_URL = os.getenv("https://woouwzzsajbmfbhragho.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indvb3V3enpzYWpibWZiaHJhZ2hvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI4NjcyOTUsImV4cCI6MjA1ODQ0MzI5NX0.wiv0F8jsuW9M1ONuL6O2OpvXXhu1DL7PW_B4HVym4hQ")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ ERROR: No se encontraron las credenciales de Supabase. Verifica el archivo .env o las variables en Streamlit Cloud.")
    st.stop()

# Crear cliente de Supabase
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"⚠️ ERROR: No se pudo conectar con Supabase. Detalles: {e}")
    st.stop()

# ------------------------------
# 📌 INTERFAZ DE LA APLICACIÓN
# ------------------------------

st.title("📊 Sistema Contable - ProLaser")

# ------------------------------
# 📌 SECCIÓN: GESTIÓN DE CLIENTES
# ------------------------------
st.subheader("📂 Lista de Clientes")

try:
    clientes = supabase.table("clientes").select("*").execute().data
    if clientes:
        df_clientes = pd.DataFrame(clientes)
        st.dataframe(df_clientes)
    else:
        st.info("ℹ️ No hay clientes registrados.")
except Exception as e:
    st.error(f"⚠️ ERROR al cargar clientes: {e}")

# ------------------------------
# 📌 SECCIÓN: REGISTRAR PROFORMA
# ------------------------------
st.subheader("📝 Registrar Nueva Proforma")

try:
    cliente_opciones = supabase.table("clientes").select("id, nombre").execute().data
    if cliente_opciones:
        cliente_dict = {c["nombre"]: c["id"] for c in cliente_opciones}
        cliente_seleccionado = st.selectbox("Selecciona un cliente", options=list(cliente_dict.keys()))
        cliente_id = cliente_dict[cliente_seleccionado]

        total = st.number_input("Total S/.", min_value=0.0, format="%.2f")

        if st.button("✅ Crear Proforma"):
            supabase.table("proformas").insert({"cliente_id": cliente_id, "total": total}).execute()
            st.success("🎉 Proforma creada exitosamente!")
            st.experimental_rerun()
    else:
        st.warning("⚠️ No hay clientes registrados. Agrega clientes primero.")
except Exception as e:
    st.error(f"⚠️ ERROR al registrar proforma: {e}")

# ------------------------------
# 📌 SECCIÓN: LISTADO DE PROFORMAS
# ------------------------------
st.subheader("📄 Listado de Proformas")

try:
    proformas = supabase.table("proformas").select("id, cliente_id, total, fecha").execute().data
    if proformas:
        df_proformas = pd.DataFrame(proformas)
        st.dataframe(df_proformas)
    else:
        st.info("ℹ️ No hay proformas registradas.")
except Exception as e:
    st.error(f"⚠️ ERROR al cargar proformas: {e}")
