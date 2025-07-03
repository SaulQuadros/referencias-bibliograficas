
import streamlit as st
import pandas as pd
import os

CSV_FILE = 'references.csv'
COLS = [
    "Base de Dados", "Autor(es)", "Ano", "Título do Artigo",
    "Tipo de Modelo", "Resumo da Abordagem", "Principais Resultados",
    "Relevância e Uso"
]

# Função para truncar texto com ellipsis
def truncate(text, max_len):
    txt = str(text)
    return txt if len(txt) <= max_len else txt[:max_len-3] + "..."

def load_data():
    if not os.path.exists(CSV_FILE):
        pd.DataFrame(columns=COLS).to_csv(CSV_FILE, index=False)
    df = pd.read_csv(CSV_FILE)
    df = df.reindex(columns=COLS).fillna('')
    df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce').fillna(0).astype(int)
    return df

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Título da aplicação
st.title("Matriz de Leitura – Módulo de Resiliência")

# Carrega dados
df = load_data()

# --- Ferramentas de busca (filtros) ---
st.sidebar.header("Filtros de Visualização")
if not df['Ano'].dropna().empty:
    min_year, max_year = int(df['Ano'].min()), int(df['Ano'].max())
else:
    min_year, max_year = 2000, 2025
if min_year > max_year:
    min_year, max_year = max_year, min_year

if min_year < max_year:
    filtro_ano = st.sidebar.slider("Ano mínimo", min_value=min_year, max_value=max_year, value=min_year)
else:
    filtro_ano = st.sidebar.number_input("Ano mínimo", min_value=min_year, max_value=max_year, value=min_year)

tipos_disponiveis = df['Tipo de Modelo'].dropna().unique().tolist()
filtro_tipo = st.sidebar.multiselect("Tipos de Modelo", tipos_disponiveis)

# Aplica filtros
filtered = df[df['Ano'] >= filtro_ano]
if filtro_tipo:
    filtered = filtered[filtered['Tipo de Modelo'].isin(filtro_tipo)]

# --- Formulário de nova referência ---
with st.expander("➕ Adicionar nova referência", expanded=True):
    db   = st.text_input("Base de Dados", key="new_db")
    auth = st.text_input("Autor(es)", key="new_auth")
    yr   = st.number_input("Ano", min_value=1900, max_value=2100, step=1, key="new_yr")
    ttl  = st.text_input("Título do Artigo", key="new_ttl")
    mtype= st.selectbox("Tipo de Modelo", ["Empírico", "Regressão", "ANN", "GA", "GEP", "Outros"], key="new_mtype")
    summ = st.text_area("Resumo da Abordagem", key="new_summ")
    res  = st.text_area("Principais Resultados", key="new_res")
    rel  = st.text_area("Relevância e Uso", key="new_rel")
    if st.button("Salvar Referência", key="save_new"):
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
        df2 = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df2)
        st.success("Referência adicionada com sucesso!")
        st.experimental_rerun()

st.markdown("---")
st.subheader("Lista de Referências")

# Exibe a lista em uma caixa com rolagem
if filtered.empty:
    st.info("Nenhuma referência cadastrada.")
else:
    # Container scrollable
    st.markdown('<div style="overflow-x:auto; overflow-y:auto; max-height:500px; border:1px solid #ddd; padding:10px;">', unsafe_allow_html=True)
    # Cabeçalhos
    header_cols = st.columns([1,1,1,3,1,3,3,3,1,1])
    for i, col_name in enumerate(COLS):
        header_cols[i].markdown(f"**{col_name}**")
    header_cols[-2].markdown("**Editar**")
    header_cols[-1].markdown("**Excluir**")
    # Linhas de dados
    for idx, row in filtered.iterrows():
        row_cols = st.columns([1,1,1,3,1,3,3,3,1,1])
        row_cols[0].write(truncate(row["Base de Dados"], 15))
        row_cols[1].write(truncate(row["Autor(es)"], 25))
        row_cols[2].write(row["Ano"])
        row_cols[3].write(truncate(row["Título do Artigo"], 40))
        row_cols[4].write(truncate(row["Tipo de Modelo"], 10))
        row_cols[5].write(truncate(row["Resumo da Abordagem"], 50))
        row_cols[6].write(truncate(row["Principais Resultados"], 50))
        row_cols[7].write(truncate(row["Relevância e Uso"], 50))
        # Botões de ação
        if row_cols[8].button("✏️", key=f"edit_{idx}"):
            st.session_state['edit_idx'] = idx
        if row_cols[9].button("🗑️", key=f"del_{idx}"):
            st.session_state['del_idx'] = idx
    st.markdown('</div>', unsafe_allow_html=True)

    # Edição e exclusão inline seguem como antes...
    if 'edit_idx' in st.session_state:
        i = st.session_state['edit_idx']
        record = df.loc[i]
        st.warning(f'Você está editando o registro {i} - "{record["Título do Artigo"]}"')
        db_e   = st.text_input("Base de Dados", value=record["Base de Dados"], key="edit_db")
        auth_e = st.text_input("Autor(es)", value=record["Autor(es)"], key="edit_auth")
        yr_e   = st.number_input("Ano", min_value=1900, max_value=2100, value=int(record["Ano"]), key="edit_yr")
        ttl_e  = st.text_input("Título do Artigo", value=record["Título do Artigo"], key="edit_ttl")
        model_types = ["Empírico","Regressão","ANN","GA","GEP","Outros"]
        default_idx = model_types.index(record["Tipo de Modelo"]) if record["Tipo de Modelo"] in model_types else 0
        mtype_e= st.selectbox("Tipo de Modelo", model_types, index=default_idx, key="edit_mtype")
        summ_e = st.text_area("Resumo da Abordagem", value=record["Resumo da Abordagem"], key="edit_summ")
        res_e  = st.text_area("Principais Resultados", value=record["Principais Resultados"], key="edit_res")
        rel_e  = st.text_area("Relevância e Uso", value=record["Relevância e Uso"], key="edit_rel")
        if st.button("Confirmar Alteração", key="confirm_edit"):
            df.at[i, COLS] = [db_e, auth_e, yr_e, ttl_e, mtype_e, summ_e, res_e, rel_e]
            save_data(df)
            st.success("Registro alterado com sucesso!")
            del st.session_state['edit_idx']
            st.experimental_rerun()
        if st.button("Cancelar Edição", key="cancel_edit"):
            del st.session_state['edit_idx']
            st.info("Edição cancelada.")
            st.experimental_rerun()

    if 'del_idx' in st.session_state:
        i = st.session_state['del_idx']
        record = df.loc[i]
        st.error(f'Tem certeza que deseja excluir o registro {i} - "{record["Título do Artigo"]}"? Esta ação é definitiva.')
        if st.button("Sim, excluir", key="confirm_del"):
            df = df.drop(i).reset_index(drop=True)
            save_data(df)
            st.success("Registro excluído com sucesso!")
            del st.session_state['del_idx']
            st.experimental_rerun()
        if st.button("Cancelar Exclusão", key="cancel_del"):
            del st.session_state['del_idx']
            st.info("Exclusão cancelada.")
            st.experimental_rerun()

# Botão de download
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Baixar planilha CSV", data=csv_data, file_name='references.csv', mime='text/csv')
