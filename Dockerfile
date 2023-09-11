FROM apache/airflow:2.6.3-python3.9

ENV AIRFLOW_HOME=/opt/airflow
USER root
RUN apt-get update -qq
USER $AIRFLOW_UID
COPY requirement.txt .
# COPY test.py .
# RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt
