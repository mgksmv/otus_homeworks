from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from .validators import only_int


class Teacher(models.Model):
    first_name = models.CharField('Имя', max_length=32)
    last_name = models.CharField('Фамилия', max_length=32)
    short_bio = models.CharField('Короткая биография/специальность', max_length=64)
    bio = RichTextUploadingField('Биография')
    photo = models.ImageField('Фотография', blank=True, null=True, default='default_profile_pic.jpg')

    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    first_name = models.CharField('Имя', max_length=32)
    last_name = models.CharField('Фамилия', max_length=32)
    birthday = models.DateField('День рождения', blank=True, null=True)
    photo = models.ImageField('Фотография', blank=True, null=True, default='default_profile_pic.jpg')
    email = models.EmailField('Почта', max_length=32)
    phone = models.CharField('Телефон', max_length=15, validators=[only_int])

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Review(models.Model):
    stars = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE)
    rating = models.CharField('Оценка', choices=stars, max_length=1)
    text = RichTextUploadingField('Описание')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.student)


class Course(models.Model):
    name = models.CharField('Специализация', max_length=200)
    duration = models.PositiveIntegerField('Длительность (в мес.)')
    description = RichTextUploadingField('Описание')
    teachers = models.ManyToManyField(Teacher, verbose_name='Преподаватели')
    reviews = models.ManyToManyField(Review, verbose_name='Отзывы', blank=True)
    required_knowledge = RichTextUploadingField('Необходимые знания')
    after_course = RichTextUploadingField('После обучения')
    price = models.PositiveIntegerField('Стоимость (в руб.)', blank=True, null=True)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Schedule(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, verbose_name='Студенты')
    start_date = models.DateField('Дата старта курса')
    end_date = models.DateField('Дата окончания курса')

    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return str(self.course)
