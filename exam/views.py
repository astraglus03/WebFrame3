from django.shortcuts import render
from .models import Student
from django.views.generic import ListView,DetailView
# Create your views here.

def index(request):
    return render(
        request,
        'exam/index.html',
    )

# student_list.html
class St_List(ListView):
    model=Student
    template_name = 'exam/st_list.html'

class St_Detail(DetailView):
    model=Student
    template_name = 'exam/st_card.html'

