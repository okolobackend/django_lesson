from django.shortcuts import render, redirect

from lessons.models import Lesson


def index(request):
    return render(request, 'index.html')


def create_lesson_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher = request.POST.get('teacher')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        Lesson.objects.create(
            name=name,
            teacher=teacher,
            start_time=start_time,
            end_time=end_time
        )
        return redirect('index')

    return render(request, 'index.html')
