from django.shortcuts import render

# Create your views here.


def main(request):
    print('main')
    return render(request, '3Dtemplate.html')
