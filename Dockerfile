FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements.txt /app/requirements.txt

#WORKDIR /app

RUN pip install -r requirements.txt

#CMD ["python", "app.py"]
#ENTRYPOINT ["./gunicorn.sh"]