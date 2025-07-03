import streamlit as st
import pandas as pd
import os

CSV_FILE = 'references.csv'
COLS = [
    "Base de Dados", "Autor(es)", "Ano", "Título do Artigo",
    "Tipo de Modelo", "Resumo da Abordagem", "Principais Resultados",
    "Relevância e Uso"
]

def load_data():
    # Cria CSV com colunas padrão se não existir
    if not os.path.exists(CSV_FILE):
        df_init = pd.DataFrame(columns=COLS)
        df_init.to_csv(CSV_FILE, index=False)
    # Carrega dados
    df = pd.read_csv(CSV_FILE)
    # Garante que todas as colunas estejam presentes
    df = df.reindex(columns=COLS)
    # Preenche valores faltantes em "Relevância e Uso"
    if 'Relevância e Uso' in df.columns:
        df['Relevância e Uso'] = df['Relevância e Uso'].fillna('')
    # Converte coluna Ano para numérico
    df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')
    return df

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Carrega o DataFrame
df = load_data()

st.title("Matriz de Leitura – Módulo de Resiliência")

# --- Filtros na barra lateral ---
st.sidebar.header("Filtros de Visualização")
if not df['Ano'].dropna().empty:
    min_year, max_year = int(df['Ano'].min()), int(df['Ano'].max())
else:
    min_year, max_year = 2000, 2025
if min_year > max_year:
    min_year, max_year = max_year, min_year

# Slider ou campo único dependendo do intervalo
if min_year < max_year:
    filtro_ano = st.sidebar.slider(
        "Ano mínimo", min_value=min_year, max_value=max_year, value=min_year
    )
else:
    filtro_ano = st.sidebar.number_input(
        "Ano mínimo", min_value=min_year, max_value=max_year, value=min_year
    )

tipos_disponiveis = df['Tipo de Modelo'].dropna().unique().tolist()
filtro_tipo = st.sidebar.multiselect("Tipos de Modelo", tipos_disponiveis)

# Aplica filtros
df_filtered = df[df['Ano'] >= filtro_ano]
if filtro_tipo:
    df_filtered = df_filtered[df_filtered['Tipo de Modelo'].isin(filtro_tipo)]

# Exibe tabela com altura fixa para ver pelo menos 5 registros
st.subheader("Lista de Referências")
st.dataframe(df_filtered, height=300)  # Ajuste de altura

# --- Adicionar nova referência ---
with st.expander("➕ Adicionar nova referência"):
    db   = st.text_input("Base de Dados")
    auth = st.text_input("Autor(es)")
    yr   = st.number_input("Ano", min_value=1900, max_value=2100, step=1)
    ttl  = st.text_input("Título do Artigo")
    mtype= st.selectbox("Tipo de Modelo", ["Empírico", "Regressão", "ANN", "GA", "GEP", "Outros"])
    summ = st.text_area("Resumo da Abordagem")
    res  = st.text_area("Principais Resultados")
    rel  = st.text_area("Relevância e Uso")
    if st.button("Salvar Referência"):
        new_entry = {
            "Base de Dados": db,
            "Autor(es)": auth,
            "Ano": yr,
            "Título do Artigo": ttl,
            "Tipo de Modelo": mtype,
            "Resumo da Abordagem": summ,
            "Principais Resultados": res,
            "Relevância e Uso": rel
        }
        df_local = df.copy()
        df_local = pd.concat([df_local, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df_local)
        st.success("Referência adicionada com sucesso! Atualize a página para ver a lista.")

# --- Editar referência existente ---
with st.expander("✏️ Editar referência existente"):
    if not df.empty:
        options = [
            f"{i} - {str(row['Título do Artigo'])[:30]}..." 
            for i, row in df.iterrows()
        ]
        selected = st.selectbox("Selecione o registro para editar", options)
        idx = int(selected.split(" - ")[0])
        record = df.loc[idx]
        db_e   = st.text_input("Base de Dados", value=record.get("Base de Dados", ""))
        auth_e = st.text_input("Autor(es)", value=record.get("Autor(es)", ""))
        yr_e   = st.number_input("Ano", min_value=1900, max_value=2100, value=int(record['Ano']) if pd.notnull(record['Ano']) else min_year, step=1)
        ttl_e  = st.text_input("Título do Artigo", value=record.get("Título do Artigo", ""))
        model_types = ["Empírico", "Regressão", "ANN", "GA", "GEP", "Outros"]
        default_idx = model_types.index(record.get("Tipo de Modelo","Empírico")) if record.get("Tipo de Modelo") in model_types else 0
        mtype_e = st.selectbox("Tipo de Modelo", model_types, index=default_idx)
        summ_e  = st.text_area("Resumo da Abordagem", value=record.get("Resumo da Abordagem", ""))
        res_e   = st.text_area("Principais Resultados", value=record.get("Principais Resultados", ""))
        rel_e   = st.text_area("Relevância e Uso", value=record.get("Relevância e Uso", ""))
        if st.button("Salvar Alterações"):
            df.at[idx, "Base de Dados"] = db_e
            df.at[idx, "Autor(es)"]     = auth_e
            df.at[idx, "Ano"]           = yr_e
            df.at[idx, "Título do Artigo"] = ttl_e
            df.at[idx, "Tipo de Modelo"] = mtype_e
            df.at[idx, "Resumo da Abordagem"] = summ_e
            df.at[idx, "Principais Resultados"] = res_e
            df.at[idx, "Relevância e Uso"] = rel_e
            save_data(df)
            st.success("Referência atualizada com sucesso! Atualize a página para ver as mudanças.")
    else:
        st.info("Nenhuma referência disponível para edição.")

# Botão de download
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar planilha CSV",
    data=csv_data,
    file_name='references.csv',
    mime='text/csv'
)
