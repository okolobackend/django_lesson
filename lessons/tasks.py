from celery import shared_task
from django.utils import timezone
from .models import Lesson, Student
import logging
from tools import human_local_time

logger = logging.getLogger(__name__)


@shared_task
def send_register_lesson_notification(lesson_id: int, student_id: int) -> str:
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        student = Student.objects.get(id=student_id)
        # Имитация отправки уведомления
        logger.warning(f"Привет, {student.name}. Вы записаны на урок '{lesson.name}'. Начало в {human_local_time(lesson.start_time)}")
        return f"Уведомления о записи на урок {lesson.name} отправлены"
    except Lesson.DoesNotExist:
        return "Урок не найден"


@shared_task
def send_lesson_notification(lesson_id: int) -> str:
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        students = lesson.students.all()
        for student in students:
            # Имитация отправки уведомления
            logger.warning(f"Напоминание о начале урока отправлено студенту {student.id} ({student.name}) по уроку '{lesson.name}'")
        return f"Уведомления отправлены для урока {lesson.name}"
    except Lesson.DoesNotExist:
        return "Урок не найден"


@shared_task
def check_upcoming_lessons():
    """
    Задача, которая проверяет уроки, которые начнутся в ближайшие 10 минут,
    и планирует отправку уведомлений на время начала урока.
    """
    now = timezone.now()
    time_threshold = now + timezone.timedelta(minutes=10)

    upcoming_lessons = Lesson.objects.filter(
        start_time__gte=now,
        start_time__lte=time_threshold
    )

    for lesson in upcoming_lessons:
        # Планируем задачу на точное время начала урока
        send_lesson_notification.apply_async(
            args=[lesson.id],
            eta=lesson.start_time
        )
        logger.warning(f"Запланировано уведомление для урока '{lesson.name}' на {lesson.start_time}")

    return f"Проверено уроков: {upcoming_lessons.count()}"
