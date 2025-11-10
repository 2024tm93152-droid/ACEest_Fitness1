FROM python:3.11-slim

WORKDIR /app

COPY app/aceest_fitness1/requirements.txt /app/app/aceest_fitness1/requirements.txt

RUN pip install --no-cache-dir -r /app/app/aceest_fitness1/requirements.txt

COPY app /app/app

ENV PYTHONPATH=/app
ENV FLASK_APP=app.aceest_fitness1.app:create_app
ENV VERSION=v1.0
ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.aceest_fitness1.app:create_app()"]
