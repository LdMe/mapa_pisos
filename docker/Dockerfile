FROM python:3.10

#COPY . /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

#RUN pip install gunicorn

#CMD gunicorn --timeout 100 -b 0.0.0.0:80 app:app
#CMD ["gunicorn","-b","0.0.0.0:80","app:app"]
CMD ["python", "app.py"]
#ENTRYPOINT ["./gunicorn.sh"]