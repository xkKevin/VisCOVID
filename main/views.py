from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from main.process_data import process_data
from main.createReport import createReport
import base64, json, os
import glob


def batch_delete(path,xtype):
    '''
    删除指定路径下所有指定类型的文件
    :param path: 需要操作的路径，注意不要以'\'结尾
    :param xtype: 需要删除的数据类型,eg : '*.csv' ，代表选择所有的csv文件
    '''

    for infile in glob.glob(os.path.join(path, xtype)):
        os.remove(infile)


# from handleData.prepare import prepare
# Create your views here.

wxb_name = "./main/static/data/wang.xlsx"
world_name = "./main/static/data/owd.csv"
regions_name = "./main/static/data/regions.xlsx"

export_path = "./main/static/export"
report_path = "./main/static/report"

missing_countries = []
ineffective_countries = []
error_info = ""

def index(request):
    return render(request, "index.html")


def report(request):
    global missing_countries, ineffective_countries, error_info
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
                result = process_data(wxb_file.name)

                if result[0]:
                    missing_countries = result[1][0]
                    ineffective_countries = result[1][1]
                    error_info = ""
                else:
                    error_info = result[1]
                    missing_countries = []
                    ineffective_countries = []

        except Exception as e:
            return JsonResponse({"error": repr(e)})

        return render(request, "report.html", {"export_dir": "export/", "error_info": error_info,
                                               "missing_countries": missing_countries,
                                               "ineffective_countries": ineffective_countries})
    else:
        return render(request, "report.html", {"export_dir": "export/", "error_info": error_info,
                                               "missing_countries": missing_countries,
                                               "ineffective_countries": ineffective_countries})


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


def deleteFiles(request):

    global missing_countries, ineffective_countries, error_info
    missing_countries = []
    ineffective_countries = []
    error_info = ""

    try:
        batch_delete(export_path, "*csv")
        batch_delete(report_path, "*png")
        batch_delete("./main/static/data", "*xlsx")
        if os.path.exists("./main/static/data/owd.csv"):
            os.remove("./main/static/data/owd.csv")
        if os.path.exists(report_path + "/report.docx"):
            os.remove(report_path + "/report.docx")
        if os.path.exists(report_path + "/text.txt"):
            os.remove(report_path + "/text.txt")
    except Exception as e:
        return JsonResponse({"error": "Error!\n" + repr(e)})
    return JsonResponse({"error": ""})


def charts(request):
    return render(request, "charts.html")
