FROM python:3.7.3

WORKDIR /VisCOVID
COPY ./ /VisCOVID

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]