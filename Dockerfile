FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements2.txt /app/requirements2.txt

#WORKDIR /app

RUN pip install -r requirements2.txt

#CMD ["python", "app.py"]
#ENTRYPOINT ["./gunicorn.sh"]