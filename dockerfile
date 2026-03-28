FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/root/.cache/huggingface

RUN . /etc/os-release \
    && printf 'deb http://deb.debian.org/debian %s main contrib non-free non-free-firmware\n' "$VERSION_CODENAME" > /etc/apt/sources.list.d/nonfree.list \
    && printf 'deb http://deb.debian.org/debian %s-updates main contrib non-free non-free-firmware\n' "$VERSION_CODENAME" >> /etc/apt/sources.list.d/nonfree.list \
    && printf 'deb http://security.debian.org/debian-security %s-security main contrib non-free non-free-firmware\n' "$VERSION_CODENAME" >> /etc/apt/sources.list.d/nonfree.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        antiword \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
        libmagic1 \
        libsm6 \
        libxext6 \
        libxrender1 \
        poppler-utils \
        p7zip-full \
        unrar \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY app.py config.py processors.py utils.py index.html ./

EXPOSE 3333

CMD ["python", "app.py"]
