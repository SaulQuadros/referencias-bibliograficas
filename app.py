import streamlit as st
import pandas as pd
from db import get_all, insert, update, delete

st.title("Referências Bibliográficas")

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
        st.set_query_params()

# Exibir lista de referências
st.subheader("Lista de Referências")
if df.empty:
    st.info("Nenhuma referência cadastrada.")
else:
    table_html = ['<div style="overflow-x:auto; overflow-y:auto; max-height:400px; border:1px solid #ddd;">']
    table_html.append('<table style="border-collapse: collapse; width:100%;">')
    table_html.append('<thead><tr>')
    headers = ["ID", "Base de Dados", "Periódico", "Autor(es)", "Ano", "Título do Artigo",
               "Qualis", "JCR", "Tipo de Modelo", "Resumo da Abordagem",
               "Principais Resultados", "Relevância e Uso"]
    for h in headers:
        table_html.append(f'<th style="border:1px solid #ccc; padding:6px; min-width:120px; white-space:nowrap;">{h}</th>')
    table_html.append('<th style="border:1px solid #ccc; padding:6px;">Editar</th><th style="border:1px solid #ccc; padding:6px;">Excluir</th>')
    table_html.append('</tr></thead><tbody>')
    for row in df.itertuples():
        table_html.append('<tr>')
        values = [row.id, row.base_de_dados, row.periodico, row.autores, row.ano,
                  row.titulo_artigo, row.qualis, row.jcr, row.tipo_modelo,
                  row.resumo_abordagem, row.principais_resultados, row.relevancia_uso]
        for val in values:
            txt = str(val)
            truncated = txt if len(txt) <= 50 else txt[:47] + "..."
            table_html.append(f'<td style="border:1px solid #ddd; padding:6px; max-width:200px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{truncated}</td>')
        table_html.append(f'<td style="border:1px solid #ddd; padding:6px; text-align:center;"><a href="?edit_id={row.id}">✏️</a></td>')
        table_html.append(f'<td style="border:1px solid #ddd; padding:6px; text-align:center;"><a href="?del_id={row.id}">🗑️</a></td>')
        table_html.append('</tr>')
    table_html.append('</tbody></table></div>')
    st.markdown("".join(table_html), unsafe_allow_html=True)

# Tratar parâmetros de edição/exclusão
params = st.query_params
edit_id = int(params.get("edit_id", [None])[0]) if "edit_id" in params else None
del_id = int(params.get("del_id", [None])[0]) if "del_id" in params else None

# Fluxo de edição
if edit_id is not None:
    rec = df.loc[df["id"] == edit_id].iloc[0]
    st.warning(f'Editando registro {edit_id} - "{rec["titulo_artigo"]}"')
    with st.form("edit_form"):
        base_de_dados = st.text_input("Base de Dados", value=rec["base_de_dados"])
        periodico = st.text_input("Periódico", value=rec["periodico"])
        autores = st.text_input("Autor(es)", value=rec["autores"])
        ano = st.number_input("Ano", min_value=1900, max_value=2100, value=int(rec["ano"]))
        titulo_artigo = st.text_input("Título do Artigo", value=rec["titulo_artigo"])
        qualis = st.text_input("Qualis", value=rec["qualis"])
        jcr = st.text_input("JCR", value=rec["jcr"])
        tipo_modelo = st.selectbox("Tipo de Modelo", ["Empírico","Regressão","ANN","GA","GEP","Outros"], index=["Empírico","Regressão","ANN","GA","GEP","Outros"].index(rec["tipo_modelo"]))
        resumo_abordagem = st.text_area("Resumo da Abordagem", value=rec["resumo_abordagem"])
        principais_resultados = st.text_area("Principais Resultados", value=rec["principais_resultados"])
        relevancia_uso = st.text_area("Relevância e Uso", value=rec["relevancia_uso"])
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
        update(edit_id, record)
        st.success("Registro atualizado!")
        st.set_query_params()
        st.experimental_rerun()
    if cancel:
        st.set_query_params()
        st.experimental_rerun()

# Fluxo de exclusão
if del_id is not None:
    rec = df.loc[df["id"] == del_id].iloc[0]
    st.error(f'Deseja excluir registro {del_id} - "{rec["titulo_artigo"]}"?')
    col1, col2 = st.columns(2)
    if col1.button("Sim, excluir"):
        delete(del_id)
        st.success("Registro excluído!")
        st.set_query_params()
        st.experimental_rerun()
    if col2.button("Cancelar"):
        st.set_query_params()
        st.experimental_rerun()
