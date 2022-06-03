from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField

from slugify import slugify

User = get_user_model()


class Teacher(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, unique=True)
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', unique=True)
    wishlist = models.ManyToManyField(
        'Course', verbose_name='Список желаемого', related_name='student_wishlist', blank=True
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


# Auto create Teacher or Student (one to one) after User was created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == '1':
            Teacher.objects.create(user=instance)
        else:
            Student.objects.create(user=instance)


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
    students = models.ManyToManyField(Student, verbose_name='Студенты', blank=True)
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
        return f'{self.course} - {self.start_date}'


class RegistrationBase(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField('Почта', max_length=32)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    date_created = models.DateField('Дата создания', auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.email)


class RegistrationRequest(RegistrationBase):
    course = models.ForeignKey(Schedule, verbose_name='Курс (ближайший)', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'заявка на запись'
        verbose_name_plural = 'Заявки на запись'


class CourseRequest(RegistrationBase):
    class Meta:
        verbose_name = 'заявка о старте набора'
        verbose_name_plural = 'Заявки о старте набора'
