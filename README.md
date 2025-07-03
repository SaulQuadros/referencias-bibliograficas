# Matriz de Leitura – Módulo de Resiliência

Este aplicativo Streamlit organiza referências bibliográficas relacionadas ao Módulo de Resiliência de materiais terrosos em pavimentação.

## Funcionalidades

- Adicionar novas referências com campos de base de dados, autor, ano, título, tipo de modelo, resumo e resultados.
- Filtrar referências por ano mínimo e tipo de modelo.
- Visualizar e baixar a planilha CSV atualizada.

## Como usar

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
2. Execute o aplicativo:
   ```
   streamlit run app.py
   ```
3. Acesse o link fornecido pelo Streamlit no navegador.

## Arquivos

- `app.py`: Código principal do Streamlit.
- `references.csv`: Banco de dados CSV (gerado automaticamente).
- `requirements.txt`: Dependências do projeto.
- `README.md`: Este guia de instruções.
