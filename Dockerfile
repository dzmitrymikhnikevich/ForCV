FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    default-jre \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN curl -o allure-2.24.0.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.0/allure-commandline-2.24.0.tgz \
    && tar -zxvf allure-2.24.0.tgz -C /opt/ \
    && ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure \
    && rm allure-2.24.0.tgz

WORKDIR /usr/workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "tests/", "-v", "--alluredir=report"]