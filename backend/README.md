# Desenvolvimento

Para usar o workflow que sincroniza as branches de desenvolvimento basta adicionar "[sync-dev]" na mensagem de commit

Ou utilizar o alias 
```bash
git config --local alias.syncdev '!f() { read -p "Mensagem do commit: " msg; git commit -m "[sync-dev] $msg" && git push; }; f'
```

# Comandos

# `make dev`

Roda a aplicação no docker em modo de desenvolvimento, as portas do banco de dados são encaminhadas para o host

# `make migration`

Depois de rodar o make dev, usa para criar automaticamente as migrações do alembic

# `make migrate`

Serve para subir as migrações do alembic para o banco de dados 

# `make down`

# ENVIRONMENT

gerando secret key 

```bash
openssl rand -hex 32
```

```bash
cp example.env .env
nano .env
```

por padrão o host do postgress é configurado como o nome do serviço no docker-compose, se quiser alterar basta definir no `.env` a váriavel `POSTGRES_HOST="nome_do_host_ou_ip"` o mesmo vale para `POSTGRES_PORT`


se quiser rodar a parte do python localmente configure as variaveis acima e suba os serviços separadamente 

docker compose up -d pgadmin
uv run --env-file .env fastapi run --port 9090 --host 0.0.0.0 --reload

# Migrações manuais 

Precisa ter o banco de dados rodando para fazer as migrações
uv run --env-file .env alembic revision --autogenerate -m "nome da migration"

para subir uma migração 
uv run --env-file .env alembic upgrade head