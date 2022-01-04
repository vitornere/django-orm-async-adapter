#!/bin/bash
echo "Criando atalho e inserindo no bashrc"
echo alias shell="'python manage.py shell'" >> ~/.bashrc

echo "Esperando o banco de dados conectar"
postgres_ready() {
python3 << END
import sys
import psycopg2
import os
try:
    conn = psycopg2.connect(
      dbname=os.environ.get('POSTGRES_NAME'),
      user=os.environ.get('POSTGRES_USER'),
      password=os.environ.get('POSTGRES_PASSWORD'),
      host=os.environ.get('POSTGRES_HOST')
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "PostgreSQL não está disponível ainda - Espere..."
  sleep 1
done

echo "Rodando as migrações"
python manage.py migrate

echo "Rodando o servidor"
uvicorn app:app --reload --host 0.0.0.0 --port 5000 --log-level debug
