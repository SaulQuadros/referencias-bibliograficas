# Referências Bibliográficas

Este aplicativo Streamlit organiza referências bibliográficas com backend SQLite.

## Funcionalidades

- **Incluir** novas referências.
- **Listar** todas as referências cadastradas.
- **Editar** e **Excluir** registros existentes.

## Arquivos principais

- `app.py` – Código principal do Streamlit.
- `db.py` – Módulo de conexão e funções CRUD para SQLite.
- `.gitignore` – Ignora o arquivo de banco de dados local.
- `requirements.txt` – Lista de dependências (`streamlit`, `pandas`).

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
   - Use o formulário "Adicionar nova referência" para incluir registros.
   - Abaixo, utilize os botões nos registros para **Editar** ou **Excluir**.
