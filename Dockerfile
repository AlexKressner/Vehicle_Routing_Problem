FROM jupyter/base-notebook

WORKDIR /vrp

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .