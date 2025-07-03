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
    if not os.path.exists(CSV_FILE):
        pd.DataFrame(columns=COLS).to_csv(CSV_FILE, index=False)
    df = pd.read_csv(CSV_FILE)
    df = df.reindex(columns=COLS).fillna('')
    df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce').fillna(0).astype(int)
    return df

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Inicialização
st.title("Matriz de Leitura – Módulo de Resiliência")
df = load_data()

# Formulário de nova referência
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
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df)
        st.success("Referência adicionada com sucesso!")
        st.experimental_rerun()

st.markdown("---")
st.subheader("Lista de Referências")

if df.empty:
    st.info("Nenhuma referência cadastrada.")
else:
    # Exibe header
    cols = st.columns([1,1,1,2,1,2,2,2,1,1])
    for i, col_name in enumerate(COLS):
        cols[i].markdown(f"**{col_name}**")
    cols[-2].markdown("**Editar**")
    cols[-1].markdown("**Excluir**")
    # Exibe linhas
    for idx, row in df.iterrows():
        cols = st.columns([1,1,1,2,1,2,2,2,1,1])
        cols[0].write(row["Base de Dados"])
        cols[1].write(row["Autor(es)"])
        cols[2].write(row["Ano"])
        cols[3].write(row["Título do Artigo"])
        cols[4].write(row["Tipo de Modelo"])
        cols[5].write(row["Resumo da Abordagem"])
        cols[6].write(row["Principais Resultados"])
        cols[7].write(row["Relevância e Uso"])
        # Botões de ação
        if cols[8].button("✏️", key=f"edit_{idx}"):
            st.session_state['edit_idx'] = idx
        if cols[9].button("🗑️", key=f"del_{idx}"):
            st.session_state['del_idx'] = idx

    # Edição inline com confirmação
    if 'edit_idx' in st.session_state:
        i = st.session_state['edit_idx']
        record = df.loc[i]
        st.warning(f"Você está editando o registro {i} - "{record['Título do Artigo']}"")
        db_e   = st.text_input("Base de Dados", value=record["Base de Dados"], key="edit_db")
        auth_e = st.text_input("Autor(es)", value=record["Autor(es)"], key="edit_auth")
        yr_e   = st.number_input("Ano", min_value=1900, max_value=2100, value=int(record["Ano"]), key="edit_yr")
        ttl_e  = st.text_input("Título do Artigo", value=record["Título do Artigo"], key="edit_ttl")
        mtype_e= st.selectbox("Tipo de Modelo", ["Empírico","Regressão","ANN","GA","GEP","Outros"], index=["Empírico","Regressão","ANN","GA","GEP","Outros"].index(record["Tipo de Modelo"]), key="edit_mtype")
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

    # Exclusão inline com confirmação
    if 'del_idx' in st.session_state:
        i = st.session_state['del_idx']
        record = df.loc[i]
        st.error(f"Tem certeza que deseja excluir o registro {i} - "{record['Título do Artigo']}"? Esta ação é definitiva.")
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
