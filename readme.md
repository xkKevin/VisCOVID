# COVID19——新冠疫情可视化

## Deployment

1. use conda to create an environment with python3.7 

   `conda create --name viscovid python=3.7`

2. activate this environment

   `conda activate viscovid`

3. install those packages:

   `pip install django==3.0.2 pandas xlrd xlsxwriter python-docx`

   you can use image sources to speed up installation, like:

   `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django==3.0.2 pandas xlrd xlsxwriter python-docx`

4. then run this project:

   `python manage.py runserver 0.0.0.0:80`

   now the project is running on your [localhost](http://localhost)

#### Deploy on Windows
##### Reference
https://docs.microsoft.com/en-us/iis/get-started/getting-started-with-iis/getting-started-with-appcmdexe

https://stackoverflow.com/questions/58261464/how-to-host-python-3-7-flask-application-on-windows-server

#### Test createReport.py
`python main/createReport.py`