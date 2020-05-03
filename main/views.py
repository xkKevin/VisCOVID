from django.shortcuts import render
from django.http import JsonResponse
from handleData.prepare import prepare
# Create your views here.
wxb_name = "./handleData/data/wang.xlsx"
world_name = "./handleData/data/owd.csv"
def index(request):
    return render(request, "index.html")


def report(request):
    if request.method == "POST":
        try:
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
            '''
    
            '''
        except Exception as e:
            return JsonResponse({"error": "Please upload those two files correctly!"})
        return render(request, "report.html")
    else:
        return render(request, "report.html")
