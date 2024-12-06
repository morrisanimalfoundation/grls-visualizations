FROM python:3.11
COPY requirements.txt .
ENV PYTHONPATH=\/workspace
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir
WORKDIR /workspace