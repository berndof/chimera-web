FROM python:3.13-bullseye AS base
ENV PYTHONUNBUFFERED=1
WORKDIR /frontend
ENV PYTHONPATH=/frontend

##############################################
# Stage 2: UV Tools - Copia ferramentas do uv
##############################################
FROM base AS uv
# Copia os binários do uv da imagem oficial
COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /uvx /bin/
# Ajusta o PATH para utilizar o ambiente virtual criado pelo uv
ENV PATH="/frontend/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

##############################################
# Stage 3: Builder - Instalação das dependências
##############################################
FROM uv AS builder
# Sincroniza as dependências do projeto sem instalar o projeto em si
# Utiliza cache para acelerar builds futuros
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock,readonly \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml,readonly \
    uv sync --frozen --no-install-project

# Copia o código-fonte para dentro do container
COPY . /frontend

##############################################
# Stage 4: Final - Imagem de produção
##############################################
FROM uv AS final
WORKDIR /frontend
ENV PYTHONPATH=/frontend
# Copia os arquivos processados na etapa de build
COPY --from=builder /frontend /frontend
RUN chmod +x /frontend/scripts/start.sh
# Sincroniza o projeto para garantir que todas as dependências e módulos estejam atualizados
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Exponha a porta na qual a aplicação irá rodar
EXPOSE 9000

CMD ["/frontend/scripts/start.sh"]