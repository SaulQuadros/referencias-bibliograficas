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

# Load existing references
try:
    df = pd.read_csv(CSV_FILE)
except Exception as e:
    st.error(f"Erro ao ler {CSV_FILE}: {e}")
    df = pd.DataFrame(columns=[
        "Base de Dados", "Autor(es)", "Ano", "Título do Artigo",
        "Tipo de Modelo", "Resumo da Abordagem", "Principais Resultados"
    ])

# Ensure 'Ano' is numeric
df['Ano'] = pd.to_numeric(df.get('Ano', pd.Series()), errors='coerce')

st.title("Matriz de Leitura – Módulo de Resiliência")

# Sidebar filters
st.sidebar.header("Filtros de Visualização")
if not df['Ano'].dropna().empty:
    min_year = int(df['Ano'].min())
    max_year = int(df['Ano'].max())
else:
    min_year, max_year = 2000, 2025

# Ensure proper ordering
if min_year > max_year:
    min_year, max_year = max_year, min_year

# Slider or fallback for filtro_ano
if min_year < max_year:
    filtro_ano = st.sidebar.slider(
        "Ano mínimo", min_value=min_year, max_value=max_year, value=min_year
    )
else:
    # Se não há variação, usamos number_input fixo
    filtro_ano = st.sidebar.number_input(
        "Ano mínimo", min_value=min_year, max_value=max_year, value=min_year
    )

tipos_disponiveis = df['Tipo de Modelo'].dropna().unique().tolist()
filtro_tipo = st.sidebar.multiselect("Tipos de Modelo", tipos_disponiveis)

# Apply filters
df_filtered = df.copy()
df_filtered = df_filtered[df_filtered['Ano'] >= filtro_ano]
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
        try:
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
        except Exception as e:
            st.error(f"Erro ao salvar referência: {e}")

# Download CSV
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar planilha CSV",
    data=csv_data,
    file_name='references.csv',
    mime='text/csv'
)
