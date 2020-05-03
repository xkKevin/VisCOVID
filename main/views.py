from django.shortcuts import render
from django.http import JsonResponse
from handleData.prepare import prepare
from handleData.analyze import analyze
# Create your views here.
wxb_name = "./handleData/data/wang.xlsx"
world_name = "./handleData/data/owd.csv"
export_path = "./main/static/export"
def index(request):
    return render(request, "index.html")


def report(request):
    if request.method == "POST":
        try:
<<<<<<< HEAD
            wxb_file = request.FILES.get("wxb_file")
            ourworldindata = request.FILES.get("ourworldindata")

            # file_name = wxb_file.name
            # f1 = open(file_name, "wb")
            # for i in wxb_file.chunks():
            #     f1.write(i)
            # f1.close()

            with open(wxb_name, "wb") as f1, open(world_name, "wb") as f2:
                for i in wxb_file.chunks():
                    f1.write(i)
                for i in ourworldindata.chunks():
                    f2.write(i)
            
            prepare()
            analyze()
=======
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
                '''
                your code
                '''
>>>>>>> 25d43f9671b460d7354ba28b517b051e644b5d06
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Please upload those two files correctly!"})
        return render(request, "report.html")
    else:
        return render(request, "report.html")
