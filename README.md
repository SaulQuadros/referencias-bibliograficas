# Matriz de Leitura – Módulo de Resiliência

Este aplicativo Streamlit implementa uma matriz de leitura para organizar referências bibliográficas relacionadas ao Módulo de Resiliência de materiais terrosos em pavimentação.

## Funcionalidades

- Adicionar novas referências com informações de base de dados, autor, ano, título, tipo de modelo, resumo e resultados.
- Filtrar a lista de referências por ano mínimo e tipo de modelo.
- Visualizar a lista completa de referências em uma tabela interativa.
- Baixar a planilha em formato CSV.

## Como usar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```
3. Acesse o link fornecido pelo Streamlit em seu navegador.

## Estrutura dos arquivos

- `app.py`: Código principal do aplicativo.
- `references.csv`: Banco de dados em CSV gerado automaticamente.
- `requirements.txt`: Dependências do projeto.
- `README.md`: Este arquivo de instruções.

## Compatibilidade

Desenvolvido e testado com Python 3.8+ e Streamlit 1.x.
