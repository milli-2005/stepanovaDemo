from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField('ФИО', max_length=120)
    phone = models.CharField('Телефон', max_length=16)

    def __str__(self):
        return self.full_name


class CourseApplication(models.Model):
    COURSE_CHOICES = [
        ('qualification', 'Курс повышения квалификации'),
        ('retraining', 'Курс переподготовки'),
        ('safety', 'Курс по охране труда'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('phone', 'Переводом по номеру телефона'),
    ]
    STATUS_NEW = 'new'
    STATUS_STUDYING = 'studying'
    STATUS_FINISHED = 'finished'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_STUDYING, 'Идет обучение'),
        (STATUS_FINISHED, 'Обучение завершено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    course = models.CharField('Курс', max_length=32, choices=COURSE_CHOICES)
    start_date = models.DateField('Дата начала')
    payment_method = models.CharField('Способ оплаты', max_length=16, choices=PAYMENT_CHOICES)
    status = models.CharField('Статус', max_length=16, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.get_course_display()}'


class Review(models.Model):
    application = models.OneToOneField(CourseApplication, on_delete=models.CASCADE, related_name='review')
    text = models.TextField('Отзыв', max_length=700)
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    def __str__(self):
        return f'Отзыв к заявке #{self.application_id}'
