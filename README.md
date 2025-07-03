# Referências Bibliográficas

Este aplicativo Streamlit organiza referências bibliográficas de forma interativa e intuitiva.

## Funcionalidades

- **Incluir novas referências**, com os campos:
  - Base de Dados  
  - Autor(es)  
  - Ano  
  - Título do Artigo  
  - Tipo de Modelo  
  - Resumo da Abordagem  
  - Principais Resultados  
  - Relevância e Uso  
- **Filtros integrados acima da lista**:
  - **Busca por Título** (campo de texto livre)  
  - **Filtro por Ano** (slider ou campo numérico)  
  - **Filtro por Tipo de Modelo** (multi-select)  
- **Visualização em tabela HTML** scrollable, com truncamento automático e botões ✏️/🗑️ para editar ou excluir cada registro.  
- **Fluxo de edição/exclusão** com confirmação antes de aplicar mudanças definitivas.  
- **Download** da planilha completa em CSV.

## Como usar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```
3. No browser:
   - Use o formulário no topo para **incluir** referências.  
   - Abaixo, ajuste os **filtros** (Título, Ano, Tipo) para reduzir a lista.  
   - Clique nos ícones ✏️ ou 🗑️ na tabela para **editar** ou **excluir** registros.  
   - Baixe a planilha completa clicando em **Baixar planilha CSV**.

## Estrutura dos arquivos

- `app.py` – Código principal do Streamlit.  
- `references.csv` – Banco de dados CSV gerado automaticamente.  
- `requirements.txt` – Lista de dependências (`streamlit`, `pandas`).  
- `README.md` – Este guia de uso.
