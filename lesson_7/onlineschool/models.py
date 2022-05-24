from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField

from slugify import slugify


class Teacher(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь', unique=True)
    short_bio = models.CharField('Короткая биография/специальность', max_length=64)
    bio = RichTextUploadingField('Биография')

    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        student_exists = Student.objects.filter(user=self.user)
        if student_exists:
            raise ValidationError('Уже существует студент с этим профилем')
        super().save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь', unique=True)
    courses = models.ManyToManyField(
        'Course', verbose_name='Мои курсы', related_name='student_courses', blank=True, null=True
    )
    wishlist = models.ManyToManyField(
        'Course', verbose_name='Список желаемого', related_name='student_wishlist', blank=True, null=True
    )

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        teacher_exists = Teacher.objects.filter(user=self.user)
        if teacher_exists:
            raise ValidationError('Уже существует преподаватель с этим профилем')
        super().save(*args, **kwargs)


class Review(models.Model):
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField('Оценка', validators=[MinValueValidator(0), MaxValueValidator(5)])
    text = RichTextUploadingField('Описание')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.student)


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    color = models.CharField('Цвет', max_length=7, default='#0D6EFD')
    slug = models.SlugField('URL', max_length=50, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            new_slug = slugify(self.name)
            slug_exists = Category.objects.filter(slug=new_slug).exists()
            if slug_exists:
                self.slug = f'{str(new_slug)}-{str(self.id)}'
            else:
                self.slug = new_slug
            self.save()


class Course(models.Model):
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=200)
    photo = models.ImageField('Фотография', blank=True, null=True, default='course_default.png')
    duration = models.PositiveIntegerField('Длительность (в мес.)')
    short_description = RichTextUploadingField('Краткое описание', blank=True, null=True)
    description = RichTextUploadingField('Описание')
    teachers = models.ManyToManyField('Teacher', verbose_name='Преподаватели')
    reviews = models.ManyToManyField('Review', verbose_name='Отзывы', blank=True)
    required_knowledge = RichTextUploadingField('Необходимые знания')
    after_course = RichTextUploadingField('После обучения')
    price = models.PositiveIntegerField('Стоимость (в руб.)', blank=True, null=True)
    slug = models.SlugField('URL', max_length=50, unique=True)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            new_slug = slugify(self.name)
            slug_exists = Course.objects.filter(slug=new_slug).exists()
            if slug_exists:
                self.slug = f'{str(new_slug)}-{str(self.id)}'
            else:
                self.slug = new_slug
            self.save()


class Schedule(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, verbose_name='Студенты')
    start_date = models.DateField('Дата старта курса')
    end_date = models.DateField('Дата окончания курса')
    is_announced_later = models.BooleanField('Не показывать дату начала курса?')
    slug = models.SlugField('URL', max_length=50, unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            new_slug = slugify(f'{self.course.name}-{self.start_date.month}-{self.start_date.year}')
            slug_exists = Schedule.objects.filter(slug=new_slug).exists()
            if slug_exists:
                self.slug = f'{str(new_slug)}-{str(self.id)}'
            else:
                self.slug = new_slug
            self.save()

    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'Расписание'
        ordering = ('is_announced_later', 'start_date')

    def __str__(self):
        return str(self.course)
