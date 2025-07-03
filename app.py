import streamlit as st
import pandas as pd
import os

# Arquivo de dados
CSV_FILE = 'references.csv'
COLS = [
    "Base de Dados", "Autor(es)", "Ano", "Título do Artigo",
    "Tipo de Modelo", "Resumo da Abordagem", "Principais Resultados",
    "Relevância e Uso"
]

# Função para truncar texto
def truncate(text, max_len):
    txt = str(text)
    return txt if len(txt) <= max_len else txt[:max_len-3] + '...'

# Carrega ou inicializa o CSV
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=COLS).to_csv(CSV_FILE, index=False)
df = pd.read_csv(CSV_FILE).reindex(columns=COLS).fillna('')
df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce').fillna(0).astype(int)

# Verifica parâmetros de query para edição/exclusão
params = st.experimental_get_query_params()
edit_idx = int(params.get('edit_idx', [None])[0]) if 'edit_idx' in params else None
del_idx = int(params.get('del_idx', [None])[0]) if 'del_idx' in params else None

st.title("Referências Bibliográficas")

# Filtros na sidebar
st.sidebar.header("Filtros de Visualização")
titulo_search = st.sidebar.text_input("Título")
if not df['Ano'].dropna().empty:
    min_year, max_year = int(df['Ano'].min()), int(df['Ano'].max())
else:
    min_year, max_year = 2000, 2025
if min_year > max_year:
    min_year, max_year = max_year, min_year

if min_year < max_year:
    filtro_ano = st.sidebar.slider("Ano mínimo", min_year, max_year, min_year)
else:
    filtro_ano = st.sidebar.number_input("Ano mínimo", min_year, max_year, min_year)

tipos = df['Tipo de Modelo'].unique().tolist()
filtro_tipo = st.sidebar.multiselect("Tipos de Modelo", tipos)

# Aplica filtros
filtered = df[df['Ano'] >= filtro_ano]
if filtro_tipo:
    filtered = filtered[filtered['Tipo de Modelo'].isin(filtro_tipo)]
if titulo_search:
    filtered = filtered[filtered['Título do Artigo'].str.contains(titulo_search, case=False, na=False)]

# Formulário de inclusão de nova referência
with st.expander("➕ Adicionar nova referência", expanded=True):
    cols1, cols2 = st.columns(2)
    db   = cols1.text_input("Base de Dados", key="new_db")
    auth = cols2.text_input("Autor(es)", key="new_auth")
    yr   = cols1.number_input("Ano", min_value=1900, max_value=2100, key="new_yr")
    ttl  = cols2.text_input("Título do Artigo", key="new_ttl")
    mtype= st.selectbox("Tipo de Modelo", ["Empírico","Regressão","ANN","GA","GEP","Outros"], key="new_mtype")
    summ = st.text_area("Resumo da Abordagem", key="new_summ")
    res  = st.text_area("Principais Resultados", key="new_res")
    rel  = st.text_area("Relevância e Uso", key="new_rel")
    if st.button("Salvar Referência", key="save_new"):
        entry = dict(zip(COLS, [db, auth, yr, ttl, mtype, summ, res, rel]))
        pd.concat([df, pd.DataFrame([entry])], ignore_index=True).to_csv(CSV_FILE, index=False)
        st.success("Referência adicionada!")
        st.experimental_set_query_params()
        st.experimental_rerun()

st.markdown("---")
st.subheader("Lista de Referências")

# Renderiza tabela HTML com scroll e truncamento
if filtered.empty:
    st.info("Nenhuma referência cadastrada.")
else:
    table_html = ['<div style="overflow-x:auto; overflow-y:auto; max-height:400px; border:1px solid #ddd;">']
    table_html.append('<table style="border-collapse: collapse; width:100%;">')
    # Cabeçalho
    table_html.append('<thead><tr>')
    for col in COLS:
        table_html.append(f'<th style="border:1px solid #ccc; padding:6px; min-width:120px; white-space:nowrap;">{col}</th>')
    table_html.append('<th style="border:1px solid #ccc; padding:6px;">Editar</th><th style="border:1px solid #ccc; padding:6px;">Excluir</th>')
    table_html.append('</tr></thead><tbody>')
    # Linhas
    for i, row in filtered.iterrows():
        table_html.append('<tr>')
        for col in COLS:
            val = truncate(row[col], 50)
            table_html.append(f'<td style="border:1px solid #ddd; padding:6px; max-width:200px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{val}</td>')
        table_html.append(f'<td style="border:1px solid #ddd; padding:6px; text-align:center;"><a href=\"?edit_idx={i}\">✏️</a></td>')
        table_html.append(f'<td style="border:1px solid #ddd; padding:6px; text-align:center;"><a href=\"?del_idx={i}\">🗑️</a></td>')
        table_html.append('</tr>')
    table_html.append('</tbody></table></div>')
    st.markdown(''.join(table_html), unsafe_allow_html=True)

# Fluxo de edição
if edit_idx is not None:
    rec = df.loc[edit_idx]
    st.warning(f'Editando registro {edit_idx} - "{rec["Título do Artigo"]}"')
    db_e, auth_e, yr_e, ttl_e, mtype_e, summ_e, res_e, rel_e = [rec[c] for c in COLS]
    db_e = st.text_input("Base de Dados", value=db_e)
    auth_e = st.text_input("Autor(es)", value=auth_e)
    yr_e = st.number_input("Ano", min_value=1900, max_value=2100, value=int(yr_e))
    ttl_e = st.text_input("Título do Artigo", value=ttl_e)
    mtype_e = st.selectbox("Tipo de Modelo", ["Empírico","Regressão","ANN","GA","GEP","Outros"], index=["Empírico","Regressão","ANN","GA","GEP","Outros"].index(mtype_e))
    summ_e = st.text_area("Resumo da Abordagem", value=summ_e)
    res_e = st.text_area("Principais Resultados", value=res_e)
    rel_e = st.text_area("Relevância e Uso", value=rel_e)
    col1, col2 = st.columns(2)
    if col1.button("Confirmar Alteração"):
        df.at[edit_idx, COLS] = [db_e, auth_e, yr_e, ttl_e, mtype_e, summ_e, res_e, rel_e]
        df.to_csv(CSV_FILE, index=False)
        st.success("Registro atualizado!")
        st.experimental_set_query_params()
        st.experimental_rerun()
    if col2.button("Cancelar"):
        st.experimental_set_query_params()
        st.experimental_rerun()

# Fluxo de exclusão
if del_idx is not None:
    rec = df.loc[del_idx]
    st.error(f'Deseja excluir registro {del_idx} - "{rec["Título do Artigo"]}"?')
    col1, col2 = st.columns(2)
    if col1.button("Sim, excluir"):
        df.drop(del_idx).reset_index(drop=True).to_csv(CSV_FILE, index=False)
        st.success("Registro excluído!")
        st.experimental_set_query_params()
        st.experimental_rerun()
    if col2.button("Cancelar"):
        st.experimental_set_query_params()
        st.experimental_rerun()

# Botão de download CSV
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Baixar planilha CSV", data=csv_data, file_name='references.csv', mime='text/csv')
