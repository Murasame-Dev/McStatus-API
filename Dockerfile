FROM python:3.13

WORKDIR /app

COPY . .
RUN pip install gunicorn && pip install -r requirements.txt
EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
