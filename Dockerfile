FROM python:3.10

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "flask_app.py"]
#ENTRYPOINT ["./gunicorn.sh"]