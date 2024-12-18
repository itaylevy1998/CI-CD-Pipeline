FROM python:3.10 AS base

WORKDIR /app

COPY . .
COPY ./templates/ /templates/
RUN pip install   --no-cache-dir -r requirements.txt 

FROM python:3.10-slim
WORKDIR /app
COPY --from=base /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=base /usr/local/bin /usr/local/bin  
COPY --from=base /app/ /app
COPY --from=base /app/templates/ /app/templates
EXPOSE 5000
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]



