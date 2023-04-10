from django.shortcuts import render

# Create your views here.

def landing(request):
    return render(
        request,
        'single_pages/landing.html', # templates 에서 만들어줘야함. / 그냥 single_pages바로 아래에 만들면 안됌!
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html',
    )
