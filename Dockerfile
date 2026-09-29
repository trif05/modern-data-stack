FROM apache/airflow:2.8.1

# Copy the requirements.txt from our computer inside to the Docker container
COPY requirements.txt /tmp/requirements.txt

# Installing the packets using the requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt