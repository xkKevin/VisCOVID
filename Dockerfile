FROM python:3.7.3

WORKDIR /VisCOVID
COPY ./ /VisCOVID

EXPOSE 80
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django==3.0.2
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]