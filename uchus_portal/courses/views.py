from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdminApplicationForm, ApplicationForm, LoginForm, RegisterForm, ReviewForm
from .models import CourseApplication


def admin_required(request):
    return bool(request.session.get('portal_admin'))


def index(request):
    return render(request, 'courses/index.html')


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Регистрация завершена. Добро пожаловать!')
        return redirect('dashboard')
    return render(request, 'courses/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')


        if username == 'Admin26' and password == 'demo20':
            request.session['portal_admin'] = True
            messages.success(request, 'Панель администратора открыта.')
            return redirect('admin_panel')


        if form.is_valid():
            login(request, form.user)
            messages.success(request, 'Вы вошли в систему.')

            # Проверка, является ли пользователь суперпользователем Django
            if form.user.is_superuser:
                request.session['portal_admin'] = True
                return redirect('admin_panel')

            return redirect('dashboard')

    return render(request, 'courses/login.html', {'form': form})


def logout_view(request):
    logout(request)
    request.session.pop('portal_admin', None)
    return redirect('login')


@login_required
def dashboard(request):
    applications = request.user.applications.select_related('review')
    return render(request, 'courses/dashboard.html', {'applications': applications})


@login_required
def create_application(request):
    form = ApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.user = request.user
        application.save()
        messages.success(request, 'Заявка отправлена администратору.')
        return redirect('dashboard')
    return render(request, 'courses/application_form.html', {'form': form})


@login_required
def add_review(request, application_id):
    application = get_object_or_404(
        CourseApplication,
        id=application_id,
        user=request.user,
        status=CourseApplication.STATUS_FINISHED,
    )
    if hasattr(application, 'review'):
        messages.info(request, 'Отзыв по этой заявке уже оставлен.')
        return redirect('dashboard')
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.application = application
        review.save()
        messages.success(request, 'Спасибо за отзыв!')
        return redirect('dashboard')
    return render(request, 'courses/review_form.html', {'form': form, 'application': application})


def admin_login(request):
    return redirect('login')


def admin_logout(request):
    request.session.pop('portal_admin', None)

    return redirect('login')


def admin_panel(request):
    if not admin_required(request):
        return redirect('login')

    if request.method == 'POST':
        application = get_object_or_404(CourseApplication, id=request.POST.get('application_id'))
        application.status = request.POST.get('status', application.status)
        application.save()
        messages.success(request, f'Статус заявки #{application.id} обновлен.')
        query_string = request.GET.urlencode()
        return redirect(f'{request.path}?{query_string}' if query_string else request.path)

    applications = CourseApplication.objects.select_related('user', 'user__profile', 'review')
    status = request.GET.get('status', '')
    query = request.GET.get('q', '')
    ordering = request.GET.get('sort', '-created_at')
    if status:
        applications = applications.filter(status=status)
    if query:
        course_values = [
            value
            for value, label in CourseApplication.COURSE_CHOICES
            if query.lower() in label.lower()
        ]
        applications = applications.filter(
            Q(user__username__icontains=query)
            | Q(user__profile__full_name__icontains=query)
            | Q(course__icontains=query)
            | Q(course__in=course_values)
        )
    if ordering not in ['created_at', '-created_at', 'status', 'course']:
        ordering = '-created_at'
    paginator = Paginator(applications.order_by(ordering), 6)
    page = paginator.get_page(request.GET.get('page'))
    query_params = request.GET.copy()
    query_params.pop('page', None)
    page_prefix = f'?{query_params.urlencode()}&' if query_params else '?'
    return render(
        request,
        'courses/admin_panel.html',
        {
            'page': page,
            'page_prefix': page_prefix,
            'status_choices': CourseApplication.STATUS_CHOICES,
        },
    )


def admin_application_create(request):
    if not admin_required(request):
        return redirect('login')

    form = AdminApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save()
        messages.success(request, f'Заявка #{application.id} создана.')
        return redirect('admin_panel')

    return render(
        request,
        'courses/admin_application_form.html',
        {'form': form, 'title': 'Создать заявку', 'button_text': 'Создать'},
    )


def admin_application_edit(request, application_id):
    if not admin_required(request):
        return redirect('login')

    application = get_object_or_404(CourseApplication, id=application_id)
    form = AdminApplicationForm(request.POST or None, instance=application)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Заявка #{application.id} обновлена.')
        return redirect('admin_panel')
    return render(
        request,
        'courses/admin_application_form.html',
        {'form': form, 'title': f'Редактировать заявку #{application.id}', 'button_text': 'Сохранить'},
    )


def admin_application_delete(request, application_id):
    if not admin_required(request):
        return redirect('login')

    application = get_object_or_404(CourseApplication.objects.select_related('user'), id=application_id)
    if request.method == 'POST':
        application.delete()
        messages.success(request, f'Заявка #{application_id} удалена.')
        return redirect('admin_panel')
    return render(request, 'courses/admin_application_confirm_delete.html', {'application': application})
