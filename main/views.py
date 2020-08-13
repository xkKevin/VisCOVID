from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from main.process_data import process_data
from main.createReport import createReport
import base64, json, os

# from handleData.prepare import prepare
# Create your views here.

wxb_name = "./main/static/data/wang.xlsx"
world_name = "./main/static/data/owd.csv"
regions_name = "./main/static/data/regions.xlsx"

export_path = "./main/static/export"
report_path = "./main/static/report"


def index(request):
    return render(request, "index.html")


def report(request):
    if request.method == "POST":
        try:
            folder = request.FILES.getlist("folder")
            if folder:
                for fi in folder:
                    with open("%s/%s" % (export_path,fi.name), "wb") as f:
                        for i in fi.chunks():
                            f.write(i)
            else:
                wxb_file = request.FILES.get("wxb_file")
                # print(wxb_file)
                ourworldindata = request.FILES.get("ourworldindata")
                regionsdata = request.FILES.get("regionsdata")
                with open(wxb_name, "wb") as f1, open(world_name, "wb") as f2, open(regions_name, "wb") as f3:
                    for i in wxb_file.chunks():
                        f1.write(i)
                    for i in ourworldindata.chunks():
                        f2.write(i)
                    for i in regionsdata.chunks():
                        f3.write(i)
                process_data(wxb_file.name)
        except Exception as e:
            return JsonResponse({"error": repr(e)})
        return render(request, "report.html", {"export_dir": "export/"})
    else:
        return render(request, "report.html", {"export_dir": "export/"})


def csvFile(request, file_name):
    try:
        file_location = export_path + "/" + file_name
        with open(file_location, 'r', encoding='utf-8') as f:
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
            text = request.POST.get("text", "")
            num = int(request.POST.get("num", "50"))

            for key, value in baseimg.items():
                with open("%s/%s.png" % (report_path, key), 'wb') as f:
                    f.write(base64.b64decode(value[21:]))

            if text:
                path = "%s/text.txt" % (report_path)
                if (os.path.exists(path)):
                    os.remove(path)
                for line in text.split('\n'):
                    line = line.strip()
                    if len(line) > 3:
                        with open(path, 'a', encoding='utf-8') as f:
                            f.write(line + "\n")
            createReport(num)
        except Exception as e:
            return JsonResponse({"error": "Error!\n" + repr(e)})

        return JsonResponse({"result": True})

    return JsonResponse({"result": "404"})

