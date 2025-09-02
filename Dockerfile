FROM python:3.13

WORKDIR /app

COPY . .
RUN pip install gunicorn && pip install -r requirements.txt

ENV BACKGROUND_URL = "https://www.loliapi.com/acg/"
ENV DEFAULT_ICON = "mcstatus_img/minecraft-creeper-face.png"
ENV FONT_PATH = "mcstatus_img/MiSans-Bold.ttf"
ENV IMAGE_WIDTH = 0
ENV IMAGE_HEIGHT = 0

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
