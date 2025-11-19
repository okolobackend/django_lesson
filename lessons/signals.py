from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from .models import Lesson, Student, StudentsLesson
from .tasks import send_register_lesson_notification

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Lesson)
def lesson_created(sender, instance, created, **kwargs):
    if created:
        logger.warning(f"Создан новый урок: '{instance.name}' с учителем {instance.teacher}")
        students = Student.objects.all()
        for student in students:
            # Регистрируем студента на урок
            StudentsLesson.objects.create(lesson=instance, student=student)


@receiver(post_save, sender=StudentsLesson)
def student_registered(sender, instance, created, **kwargs):
    if created:
        logger.warning(f"Студент {instance.student.name} зарегистрирован на урок '{instance.lesson.name}'")
        send_register_lesson_notification.apply_async(kwargs={'lesson_id': instance.lesson.id,
                                                              'student_id': instance.student.id,},
                                                      countdown=1)