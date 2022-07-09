from django.views.generic import ListView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from ..models import RegistrationRequest, Course, Student, Schedule, CourseRequest
from ..mixins import CheckUserIsTeacher
from ..tasks import send_mail_task

User = get_user_model()


class RegistrationRequestListView(CheckUserIsTeacher, ListView):
    model = RegistrationRequest
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('course', 'student', 'student__user') \
            .only(
            'email', 'student', 'student__user__first_name', 'student__user__last_name', 'date_created',
            'course', 'course__name', 'course__slug'
        )


class RegistrationRequestDeleteView(DeleteView):
    model = RegistrationRequest
    success_url = reverse_lazy('onlineschool:registration_requests')

    def form_valid(self, form):
        messages.success(self.request, 'Заявка удалена.')
        return redirect(self.get_success_url())


def add_student_to_group(request, course_slug, user_id):
    if not request.user.is_authenticated or request.user.user_type == '2':
        raise PermissionDenied

    course = get_object_or_404(Course, slug=course_slug)
    groups = course.schedule_set.all()
    user = User.objects.filter(id=user_id).only('first_name', 'last_name', 'email').first()
    student = Student.objects.filter(user__id=user_id).first()

    if request.method == 'POST':
        group_id = request.POST.get('group')
        group_to_add_user = Schedule.objects.filter(id=group_id).first()
        group_to_add_user.students.add(student)
        group_to_add_user.save()

        registration_request = RegistrationRequest.objects.filter(student=student, course=course).first()
        registration_request.delete()

        messages.success(request, 'Пользователь добавлен в группу!')
        return redirect('onlineschool:registration_requests')

    return render(request, 'onlineschool/add_user_to_group.html', context={'groups': groups, 'user': user})


def register_registration_request(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    current_user = request.user

    if current_user.is_authenticated:
        if current_user.user_type == '1':
            messages.error(
                request, 'Для регистрации вы должны быть студентом :) Зарегистрируйте аккаунт студента для записи.'
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))

        student = Student.objects.filter(user=current_user).first()
        request_exists = RegistrationRequest.objects.filter(student=student, course=course).exists()
        if request_exists:
            messages.error(request, 'Вы уже подавали заявку на этот курс!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        email = current_user.email
    else:
        student = None
        email = request.POST.get('email')
        account_exists = User.objects.filter(email=email).first()
        if account_exists:
            messages.error(
                request,
                f'У Вас имеется аккаунт, зарегистрированный на почту {email}! Войдите и подайте заявку с аккаунта.'
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))

    data = RegistrationRequest.objects.create(
        student=student,
        email=email,
        course=course
    )
    data.save()

    send_mail_task.delay(
        'Заявка на запись подана!',
        f'Заявка на запись на курс {course.name} успешно подана. Мы Вам сообщим, когда начнётся курс.',
        email,
    )
    send_mail_task.delay(
        'Новая заявка',
        f'Подана новая заявка на курс {course.name} от {student if student else email}\n'
        f'Посмотреть все заявки: {request.get_host() + reverse("onlineschool:registration_requests")}'
    )

    messages.success(request, 'Заявка на запись подана!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def register_course_request(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    current_user = request.user

    if current_user.is_authenticated:
        if current_user.user_type == '1':
            messages.error(
                request, 'Для подачи заявки вы должны быть студентом :)'
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))

        student = Student.objects.filter(user=current_user).first()
        request_exists = CourseRequest.objects.filter(student=student, course=course).exists()
        if request_exists:
            messages.error(request, 'Вы уже подавали заявку на этот курс!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        email = current_user.email
    else:
        student = None
        email = request.POST.get('email')
        account_exists = User.objects.filter(email=email).first()
        if account_exists:
            messages.error(
                request,
                f'У Вас имеется аккаунт, зарегистрированный на почту {email}! Войдите и подайте заявку с аккаунта.'
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))

    data = CourseRequest.objects.create(
        student=student,
        email=email,
        course=course
    )
    data.save()

    send_mail_task.delay(
        'Заявка на старт курса подана!',
        f'Заявка на старт курса {course.name} успешно подана. Мы Вам сообщим, когда начнётся набор в группу.',
        email,
    )
    send_mail_task.delay(
        'Новая заявка',
        f'Подана новая заявка на курс {course.name} от {student if student else email}\n'
        f'Группы на курс ещё нет, начать набор? '
        f'{request.get_host() + reverse("onlineschool:create_group") + "?create=" + str(course.id)}'
    )

    messages.success(request, 'Заявка подана! Мы вам сообщим о старте курса.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def send_registration_link(request, email, course_slug):
    course = Course.objects.filter(slug=course_slug).first()
    send_mail_task.delay(
        'Online School. Регистрация.',
        f'Вы недавно подавали заявку на запись на курс {course.name}\n'
        f'Чтобы записать Вас в группу, потребуется создать аккаунт в нашем сайте.\n'
        f'Перейдите по ссылке ниже, чтобы создать новый аккаунт:\n'
        f'{request.get_host() + reverse("accounts:signup")}',
        email,
    )

    messages.success(request, 'Ссылка на регистрацию отправлена.')
    return redirect(request.META.get('HTTP_REFERER', '/'))
