import streamlit as st
import pandas as pd
from db import get_all, insert, update, delete

st.title("Referências Bibliográficas")

# Initialize edit state
if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# Carrega todos os registros
df = get_all()

# Formulário de inclusão de nova referência
with st.expander("➕ Adicionar nova referência", expanded=True):
    base_de_dados = st.text_input("Base de Dados", key="new_base")
    periodico = st.text_input("Periódico", key="new_periodico")
    autores = st.text_input("Autor(es)", key="new_autores")
    ano = st.number_input("Ano", min_value=1900, max_value=2100, key="new_ano")
    titulo_artigo = st.text_input("Título do Artigo", key="new_titulo")
    qualis = st.text_input("Qualis", key="new_qualis")
    jcr = st.text_input("JCR", key="new_jcr")
    tipo_modelo = st.selectbox("Tipo de Modelo", ["Empírico","Regressão","ANN","GA","GEP","Outros"], key="new_tipo")
    resumo_abordagem = st.text_area("Resumo da Abordagem", key="new_resumo")
    principais_resultados = st.text_area("Principais Resultados", key="new_resultados")
    relevancia_uso = st.text_area("Relevância e Uso", key="new_relevancia")
    if st.button("Salvar Referência", key="save_new"):
        record = {
            "base_de_dados": base_de_dados,
            "periodico": periodico,
            "autores": autores,
            "ano": int(ano),
            "titulo_artigo": titulo_artigo,
            "qualis": qualis,
            "jcr": jcr,
            "tipo_modelo": tipo_modelo,
            "resumo_abordagem": resumo_abordagem,
            "principais_resultados": principais_resultados,
            "relevancia_uso": relevancia_uso
        }
        insert(record)
        st.success("Referência adicionada!")
        st.experimental_rerun()

# Fluxo de edição
if st.session_state.edit_id is not None:
    rec_id = st.session_state.edit_id
    rec = df.loc[df["id"] == rec_id].iloc[0]
    st.warning(f'Editando registro {rec_id} - "{rec["titulo_artigo"]}"')
    with st.form("edit_form"):
        base_de_dados = st.text_input("Base de Dados", value=rec["base_de_dados"], key="edit_base")
        periodico = st.text_input("Periódico", value=rec["periodico"], key="edit_periodico")
        autores = st.text_input("Autor(es)", value=rec["autores"], key="edit_autores")
        ano = st.number_input("Ano", min_value=1900, max_value=2100, value=int(rec["ano"]), key="edit_ano")
        titulo_artigo = st.text_input("Título do Artigo", value=rec["titulo_artigo"], key="edit_titulo")
        qualis = st.text_input("Qualis", value=rec["qualis"], key="edit_qualis")
        jcr = st.text_input("JCR", value=rec["jcr"], key="edit_jcr")
        tipo_modelo = st.selectbox("Tipo de Modelo", ["Empírico","Regressão","ANN","GA","GEP","Outros"], index=["Empírico","Regressão","ANN","GA","GEP","Outros"].index(rec["tipo_modelo"]), key="edit_tipo")
        resumo_abordagem = st.text_area("Resumo da Abordagem", value=rec["resumo_abordagem"], key="edit_resumo")
        principais_resultados = st.text_area("Principais Resultados", value=rec["principais_resultados"], key="edit_resultados")
        relevancia_uso = st.text_area("Relevância e Uso", value=rec["relevancia_uso"], key="edit_relevancia")
        confirm = st.form_submit_button("Confirmar Alteração")
        cancel = st.form_submit_button("Cancelar")
    if confirm:
        record = {
            "base_de_dados": base_de_dados,
            "periodico": periodico,
            "autores": autores,
            "ano": int(ano),
            "titulo_artigo": titulo_artigo,
            "qualis": qualis,
            "jcr": jcr,
            "tipo_modelo": tipo_modelo,
            "resumo_abordagem": resumo_abordagem,
            "principais_resultados": principais_resultados,
            "relevancia_uso": relevancia_uso
        }
        update(rec_id, record)
        st.success("Registro atualizado!")
        st.session_state.edit_id = None
        st.experimental_rerun()
    if cancel:
        st.session_state.edit_id = None
        st.experimental_rerun()

# Listagem de referências
st.subheader("Lista de Referências")
if df.empty:
    st.info("Nenhuma referência cadastrada.")
else:
    for row in df.itertuples():
        cols = st.columns([8, 1, 1])
        cols[0].write(f'**{row.id}** | {row.autores} ({row.ano}) - {row.titulo_artigo}')
        if cols[1].button("✏️", key=f"edit_{row.id}"):
            st.session_state.edit_id = row.id
        if cols[2].button("🗑️", key=f"delete_{row.id}"):
            delete(row.id)
            st.success("Registro excluído!")
            st.experimental_rerun()
