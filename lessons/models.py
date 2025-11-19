from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя студента")
    email = models.EmailField(unique=True, verbose_name="Email")


class Lesson(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название урока")
    teacher = models.CharField(max_length=100, verbose_name="Преподаватель")
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    students = models.ManyToManyField(Student, through='StudentsLesson', verbose_name="Студенты")

    def get_registered_students(self):
        return self.students.all()


class StudentsLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Урок")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
