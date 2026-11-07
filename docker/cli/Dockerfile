FROM python:3.12-slim

# Actualiza la lista de paquetes y luego instala los paquetes necesarios
RUN apt-get update && \
    apt-get install -y gcc unzip g++ bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# # Instala Chalice y actualiza pip
# RUN pip install --upgrade pip && \
#     pip install chalice

RUN pip install --upgrade pip

# Agrega tus recursos y establece el directorio de trabajo
ADD resources /resources/
WORKDIR /resources/
RUN pip install -r ./requirements.txt

# Argumentos para la creación de usuarios/grupos
ARG USERNAME_LOCAL
ARG UID_LOCAL
ARG GID_LOCAL

# Crea grupo y usuario
RUN groupadd -g $GID_LOCAL $USERNAME_LOCAL || echo "This group already exists!" && \
    useradd -u $UID_LOCAL -g $GID_LOCAL -m -s /bin/bash $USERNAME_LOCAL

# Establece el directorio de trabajo en /app
WORKDIR /app
