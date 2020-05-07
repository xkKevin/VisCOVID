from django.shortcuts import render
from django.http import JsonResponse
from handleData.prepare import prepare
from handleData.analyze import analyze
import base64, json
# Create your views here.
wxb_name = "./handleData/data/wang.xlsx"
world_name = "./handleData/data/owd.csv"
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
                ourworldindata = request.FILES.get("ourworldindata")
                with open(wxb_name, "wb") as f1, open(world_name, "wb") as f2:
                    for i in wxb_file.chunks():
                        f1.write(i)
                    for i in ourworldindata.chunks():
                        f2.write(i)
                prepare()
                analyze()

        except Exception as e:
            return JsonResponse({"error": "Error!\n"+repr(e)})
        return render(request, "report.html")
    else:
        return render(request, "report.html")


def saveImage(request):
    if request.method == "POST":
        try:
            # baseimg = json.loads(request.POST.get("baseimg"))
            baseimg = request.POST.get("baseimg")
            print(baseimg)
            with open("%s/%s.png" % (report_path, '2'), 'wb') as f:
                f.write(base64.b64decode(baseimg[21:]))
            # for key, value in baseimg.items():
            #     with open("%s/%s.png" % (report_path, key),'wb') as f:
            #         f.write(base64.b64decode(value[21:]))
        except Exception as e:
            return JsonResponse({"error": "Error!\n"+repr(e)})
        return JsonResponse({"result": True})

    return JsonResponse({"result": "404"})
