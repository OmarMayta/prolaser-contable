import streamlit as st
from supabase import create_client
import pandas as pd
import os

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Sistema Contable - ProLaser")

# Sección: Gestión de Clientes
st.subheader("Clientes")
clientes = supabase.table("clientes").select("*").execute().data
df_clientes = pd.DataFrame(clientes)
st.dataframe(df_clientes)

# Sección: Registrar Nueva Proforma
st.subheader("Registrar Proforma")
cliente_id = st.selectbox("Selecciona un cliente", options=df_clientes["id"].tolist())
total = st.number_input("Total S/.", min_value=0.0, format="%.2f")

if st.button("Crear Proforma"):
    supabase.table("proformas").insert({"cliente_id": cliente_id, "total": total}).execute()
    st.success("Proforma creada exitosamente!")

# Sección: Ver Proformas
st.subheader("Listado de Proformas")
proformas = supabase.table("proformas").select("*").execute().data
df_proformas = pd.DataFrame(proformas)
st.dataframe(df_proformas)