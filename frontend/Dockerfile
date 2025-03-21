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
#ENV PATH="/frontend/.venv/bin:$PATH"
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

# Stage 4: Final - Imagem de produção
##############################################

FROM uv AS final

# Instala dependências do frontend
RUN apt-get update && apt-get install -y curl \
&& curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
&& apt-get install -y nodejs

ADD . /frontend
WORKDIR /frontend
ENV PYTHONPATH=/frontend

RUN npm install -g npm@11.2.0

RUN npm install

EXPOSE 9000




