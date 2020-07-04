from django.shortcuts import render

# Create your views here.

def horser_index(request):
    if request.method == "GET":
        html = "horser_index.html"

        return render(request,html)
