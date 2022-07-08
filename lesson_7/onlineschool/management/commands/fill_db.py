import random
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker

from ...models import Category, Course, Schedule, Teacher, Student

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу данных случайными данными.'

    def add_arguments(self, parser):
        parser.add_argument('quantity', action='append', type=int)

    def handle(self, *args, **options):
        fake = Faker('ru-ru')

        for _ in range(options['quantity'][0]):
            name = fake.job()

            Category.objects.create(
                name=name,
                color=f'#{fake.bothify("######")}',
            )

            email = fake.ascii_free_email()
            while True:
                email_exists = User.objects.filter(email=email)
                if email_exists:
                    email = fake.ascii_free_email()
                else:
                    break

            User.objects.create(
                email=fake.ascii_free_email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.msisdn(),
                user_type=random.choice(('1', '2')),
                is_active=True,
            )

        for _ in range(options['quantity'][0]):
            random_category = random.choice(Category.objects.all())
            random_teachers = [
                random.choice(Teacher.objects.all()) for _ in range(random.randrange(0, options['quantity'][0]))
            ]
            random_students = [
                random.choice(Student.objects.all()) for _ in range(random.randrange(0, options['quantity'][0]))
            ]
            name = fake.bs()

            course = Course.objects.create(
                category=random_category,
                name=name,
                duration=random.randint(4, 12),
                short_description=fake.catch_phrase(),
                description=fake.paragraph(nb_sentences=5),
                required_knowledge=fake.paragraph(nb_sentences=3),
                after_course=fake.paragraph(nb_sentences=3),
                price=fake.bothify("#####"),
            )
            course.teachers.set(random_teachers)

            def random_date(start, end):
                delta = end - start
                int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
                random_second = random.randrange(int_delta)
                return start + timedelta(seconds=random_second)

            d1 = datetime.strptime('1/7/2022', '%m/%d/%Y')
            d2 = datetime.strptime('1/7/2023', '%m/%d/%Y')

            schedule = Schedule.objects.create(
                course=course,
                start_date=random_date(d1, d2),
                end_date=random_date(d1, d2),
                is_announced_later=False,
            )
            schedule.students.set(random_students)
