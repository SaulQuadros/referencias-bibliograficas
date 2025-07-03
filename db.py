import sqlite3
import pandas as pd

DB_FILE = "references.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)

# Criar esquema da tabela com nome não-reservado
conn.execute("""
CREATE TABLE IF NOT EXISTS referencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_de_dados TEXT,
    periodico TEXT,
    autores TEXT,
    ano INTEGER,
    titulo_artigo TEXT,
    qualis TEXT,
    jcr TEXT,
    tipo_modelo TEXT,
    resumo_abordagem TEXT,
    principais_resultados TEXT,
    relevancia_uso TEXT
)
""")
conn.commit()

def get_all():
    return pd.read_sql_query("SELECT * FROM referencias", conn)

def insert(record: dict):
    keys = ", ".join(record.keys())
    placeholders = ", ".join("?" for _ in record)
    sql = f"INSERT INTO referencias ({keys}) VALUES ({placeholders})"
    conn.execute(sql, tuple(record.values()))
    conn.commit()

def update(record_id: int, record: dict):
    assignments = ", ".join(f"{key}=?" for key in record.keys())
    sql = f"UPDATE referencias SET {assignments} WHERE id=?"
    conn.execute(sql, tuple(record.values()) + (record_id,))
    conn.commit()

def delete(record_id: int):
    conn.execute("DELETE FROM referencias WHERE id=?", (record_id,))
    conn.commit()
