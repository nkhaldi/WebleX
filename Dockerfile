FROM python:3.10-slim

WORKDIR /usr/app

# Copy and install requirements
COPY ./ci/requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000
