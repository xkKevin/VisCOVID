import os

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from handleData.prepare import prepare
from handleData.analyze import analyze
import base64, json
from main.createReport import createReport
from pymongo import MongoClient, DESCENDING
import random
import string
import os
import traceback
from shutil import copyfile
import re
# Create your views here.
wxb_name = "./handleData/data/wang.xlsx"
world_name = "./handleData/data/owd.csv"
export_path = "./main/static/export"
report_path = "./main/static/report"


def extract_excel_time(name):
    pattern = "全球及重点国家疫情主要指数数据-(\d*)-(\d*)-(\d*)-(\d*)H(\d*)(.*).xlsx"
    matched = re.match(pattern, name)
    if not matched:
        return None
    year = matched.group(1)
    month = matched.group(2)
    day = matched.group(3)
    hour = matched.group(4)
    minute = matched.group(5)
    return {
        "hour": hour,
        "minute": minute
    }


def random_string(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def index(request):
    return render(request, "index.html")


def report(request):
    client = MongoClient()
    db = client['coronavirus_analysis']
    if request.method == "POST":
        try:
            # -----------------------------------------------
            # Generate a random dir name
            dir_name = random_string()
            export_dir = os.path.join(export_path, dir_name)
            os.mkdir(export_dir)
            # -----------------------------------------------
            folder = request.FILES.getlist("folder")
            method = None
            if folder:
                
                if db.csv.count() == 0:
                    db.due.remove({})
                else:
                    last_version = list(db.csv.find().sort([("_id", DESCENDING)]).limit(1))[0]
                    last_export_dir = os.path.join(export_path, last_version['name'])
                    dir_name = last_version['name']
                    export_dir = os.path.join(export_path, dir_name)

                method = "folder"
                
                for fi in folder:
                    with open("%s/%s" % (export_dir,fi.name), "wb") as f:
                        for i in fi.chunks():
                            f.write(i)
            else:
                method = "excel"
                wxb_file = request.FILES.get("wxb_file")
                due = extract_excel_time(wxb_file.name)
                if not due:
                    db.due.remove({})
                    pass
                else:
                    db.due.remove({})
                    db.due.insert_one(due)
                ourworldindata = request.FILES.get("ourworldindata")
                with open(wxb_name, "wb") as f1, open(world_name, "wb") as f2:
                    for i in wxb_file.chunks():
                        f1.write(i)
                    for i in ourworldindata.chunks():
                        f2.write(i)
                prepare()
                analyze(export_dir=export_dir)
            db.csv.insert({
                "name": dir_name,
                "method": method,
            })
        except Exception as e:
            return JsonResponse({"error": "Error!\n"+traceback.format_exc()})
        # return render(request, "report.html")
    else:
        pass
    print(db.csv.count())
    if db.csv.count() == 0:
        return render(request, "report.html", {"export_dir": ""})
    last_version = list(db.csv.find().sort([("_id", DESCENDING)]).limit(1))[0]
    
    context = {
        "export_dir": "export/" + last_version['name'] + "/"
    }
    return render(request, "report.html", context)


def csvFile(request, file_name):
    file_data = None
    client = MongoClient()
    db = client['coronavirus_analysis']
    last_version = list(db.csv.find().sort([("_id", DESCENDING)]).limit(1))[0]
    try:    
        file_location = "./main/static/export/" + last_version['name'] + "/" + file_name
        with open(file_location, 'r') as f:
           file_data = f.read()

        # sending response 
        response = HttpResponse(file_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + '"' + file_name + '"'

    except IOError:
        # handle file not exist case here
        response = HttpResponseNotFound('<h1>File not exist</h1>')
    
    return response


def saveImage(request):
    if request.method == "POST":
        try:
            baseimg = json.loads(request.POST.get("baseimg"))
            text = request.POST.get("text","")

            for key, value in baseimg.items():
                with open("%s/%s.png" % (report_path, key),'wb') as f:
                    f.write(base64.b64decode(value[21:]))

            if text:
                path = "%s/text.txt" % (report_path)
                if (os.path.exists(path)):
                    os.remove(path)
                for line in text.split('\n'):
                    line = line.strip()
                    if len(line) > 3:
                        with open(path, 'a', encoding='utf-8') as f:
                            f.write(line+"\n")
            createReport()
        except Exception as e:
            return JsonResponse({"error": "Error!\n"+repr(e)})

        return JsonResponse({"result": True})

    return JsonResponse({"result": "404"})



def dataprocess_index(request):
    return render( request, "dataprocess.html")