FROM python:3.7.3

WORKDIR /VisCOVID
COPY ./ /VisCOVID

EXPOSE 80
# ADD /VisCOVID /home/jnzs1836/zhejiang-lab/mongodb-org-server_4.2.6_amd64.deb 
RUN pwd
RUN wget https://mirrors.tuna.tsinghua.edu.cn/mongodb/apt/debian/dists/stretch/mongodb-org/4.2/main/binary-amd64/mongodb-org-server_4.2.6_amd64.deb
RUN dpkg -i ./mongodb-org-server_4.2.6_amd64.deb 
RUN wget https://mirrors.tuna.tsinghua.edu.cn/mongodb/apt/debian/dists/stretch/mongodb-org/4.2/main/binary-amd64/mongodb-org-tools_4.2.1_amd64.deb
RUN dpkg -i ./mongodb-org-tools_4.2.1_amd64.deb
RUN mkdir /data
RUN mkdir /data/db
# RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
# RUN wget https://mi/rrors.tuna.tsinghua.edu.cn/mongodb/apt/debian/dists/stretch/mongodb-org/4.2/main/binary-amd64/mongodb-org-server_4.2.2_amd64.deb

# RUN echo 'deb http://mirrors.tuna.tsinghua.edu.cn/mongodb/apt/debian stretch/mongodb-org/stable main' >> /etc/apt/sources.list.d/mongodb.list
# RUN apt-get update
# RUN apt-get install -y mongodb-org

# RUN chmod 777 /etc/systemd/system/mongo.service

RUN echo "/usr/bin/mongod &" >> /start.sh
RUN echo 'python ./manage.py runserver 0.0.0.0:80' >> /start.sh
RUN chmod 777 /start.sh
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django==3.0.2 pandas numpy pymongo xlrd python-docx

CMD ["bash", "/start.sh"]
# CMD [ "/usr/bin/mongod", "&", "&&","python", "./manage.py", "runserver", "0.0.0.0:80"]
