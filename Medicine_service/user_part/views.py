from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'user_part/home.html')


# def register(request):
#     return render(request, 'user_part/register_auth')