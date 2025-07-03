import streamlit as st
import pandas as pd
import os

CSV_FILE = 'references.csv'

# Initialize CSV if it doesn't exist
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=[
        "Base de Dados", "Autor(es)", "Ano", "Título do Artigo",
        "Tipo de Modelo", "Resumo da Abordagem", "Principais Resultados"
    ])
    df_init.to_csv(CSV_FILE, index=False)

df = pd.read_csv(CSV_FILE)

st.title("Matriz de Leitura – Módulo de Resiliência")

# Sidebar filters
st.sidebar.header("Filtros de Visualização")
min_year = int(df['Ano'].min()) if not df.empty else 2000
max_year = int(df['Ano'].max()) if not df.empty else 2025
filtro_ano = st.sidebar.slider("Ano mínimo", min_year, max_year, min_year)
tipos_disponiveis = df['Tipo de Modelo'].unique().tolist() if not df.empty else []
filtro_tipo = st.sidebar.multiselect("Tipos de Modelo", tipos_disponiveis)

# Apply filters
df_filtered = df[df['Ano'] >= filtro_ano]
if filtro_tipo:
    df_filtered = df_filtered[df_filtered['Tipo de Modelo'].isin(filtro_tipo)]

st.subheader("Lista de Referências")
st.dataframe(df_filtered)

# Add new reference
with st.expander("➕ Adicionar nova referência"):
    db   = st.text_input("Base de Dados")
    auth = st.text_input("Autor(es)")
    yr   = st.number_input("Ano", min_value=1900, max_value=2100, step=1)
    ttl  = st.text_input("Título do Artigo")
    mtype= st.selectbox("Tipo de Modelo", ["Empírico", "Regressão", "ANN", "GA", "GEP", "Outros"])
    summ = st.text_area("Resumo da Abordagem")
    res  = st.text_area("Principais Resultados")
    if st.button("Salvar Referência"):
        new_entry = {
            "Base de Dados": db,
            "Autor(es)": auth,
            "Ano": yr,
            "Título do Artigo": ttl,
            "Tipo de Modelo": mtype,
            "Resumo da Abordagem": summ,
            "Principais Resultados": res
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("Referência adicionada com sucesso! Atualize a página para ver a lista.")

# Download CSV
st.download_button(
    label="📥 Baixar planilha CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='references.csv',
    mime='text/csv'
)
