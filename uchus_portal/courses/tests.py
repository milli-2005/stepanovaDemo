# from django.contrib.auth.models import User
# from django.test import TestCase
# from django.urls import reverse
#
# from .forms import ApplicationForm, RegisterForm
# from .models import CourseApplication, Profile, Review
#
#
# class PortalScenarioTests(TestCase):
#     def test_registration_validation_matches_task(self):
#         form = RegisterForm(
#             data={
#                 'username': 'ivan12',
#                 'password': 'password123',
#                 'full_name': 'Иван Иванов',
#                 'phone': '8(999)123-45-67',
#                 'email': 'ivan@example.com',
#             }
#         )
#         self.assertTrue(form.is_valid())
#
#         bad_form = RegisterForm(
#             data={
#                 'username': 'иван123',
#                 'password': 'short',
#                 'full_name': 'Ivan Ivanov',
#                 'phone': '+7 999 123',
#                 'email': 'bad-email',
#             }
#         )
#         self.assertFalse(bad_form.is_valid())
#         self.assertIn('username', bad_form.errors)
#         self.assertIn('password', bad_form.errors)
#         self.assertIn('full_name', bad_form.errors)
#         self.assertIn('phone', bad_form.errors)
#         self.assertIn('email', bad_form.errors)
#
#     def test_application_rejects_past_start_date(self):
#         form = ApplicationForm(
#             data={
#                 'course': 'qualification',
#                 'start_date': '01.01.2020',
#                 'payment_method': 'cash',
#             }
#         )
#         self.assertFalse(form.is_valid())
#         self.assertIn('start_date', form.errors)
#
#     def test_user_can_register_login_and_create_application(self):
#         response = self.client.post(
#             reverse('register'),
#             {
#                 'username': 'user1',
#                 'password': 'password123',
#                 'full_name': 'Петр Петров',
#                 'phone': '8(900)111-22-33',
#                 'email': 'petr@example.com',
#             },
#         )
#         self.assertRedirects(response, reverse('dashboard'))
#
#         response = self.client.post(
#             reverse('apply'),
#             {
#                 'course': 'qualification',
#                 'start_date': '25.05.2026',
#                 'payment_method': 'cash',
#             },
#         )
#         self.assertRedirects(response, reverse('dashboard'))
#
#         application = CourseApplication.objects.get()
#         self.assertEqual(application.status, CourseApplication.STATUS_NEW)
#         self.assertEqual(application.get_course_display(), 'Курс повышения квалификации')
#
#     def test_admin_can_filter_and_change_status(self):
#         user = User.objects.create_user('admusr', password='password123', email='admusr@example.com')
#         Profile.objects.create(user=user, full_name='Анна Смирнова', phone='8(901)222-33-44')
#         application = CourseApplication.objects.create(
#             user=user,
#             course='safety',
#             start_date='2026-05-25',
#             payment_method='phone',
#         )
#
#         response = self.client.post(
#             reverse('login'),
#             {'username': 'Admin26', 'password': 'demo20'},
#         )
#         self.assertRedirects(response, reverse('admin_panel'))
#
#         response = self.client.get(reverse('admin_panel'), {'q': 'охране'})
#         self.assertContains(response, 'Курс по охране труда')
#
#         response = self.client.post(
#             reverse('admin_panel'),
#             {'application_id': application.id, 'status': CourseApplication.STATUS_FINISHED},
#         )
#         self.assertRedirects(response, reverse('admin_panel'))
#         application.refresh_from_db()
#         self.assertEqual(application.status, CourseApplication.STATUS_FINISHED)
#
#     def test_admin_can_create_edit_and_delete_application(self):
#         user = User.objects.create_user('crud1', password='password123', email='crud1@example.com')
#         Profile.objects.create(user=user, full_name='Мария Крылова', phone='8(903)444-55-66')
#         self.client.post(reverse('login'), {'username': 'Admin26', 'password': 'demo20'})
#
#         response = self.client.post(
#             reverse('admin_application_create'),
#             {
#                 'user': user.id,
#                 'course': 'qualification',
#                 'start_date': '26.05.2026',
#                 'payment_method': 'cash',
#                 'status': CourseApplication.STATUS_NEW,
#             },
#         )
#         self.assertRedirects(response, reverse('admin_panel'))
#         application = CourseApplication.objects.get(user=user)
#         self.assertEqual(application.course, 'qualification')
#
#         response = self.client.post(
#             reverse('admin_application_edit', args=[application.id]),
#             {
#                 'user': user.id,
#                 'course': 'safety',
#                 'start_date': '27.05.2026',
#                 'payment_method': 'phone',
#                 'status': CourseApplication.STATUS_STUDYING,
#             },
#         )
#         self.assertRedirects(response, reverse('admin_panel'))
#         application.refresh_from_db()
#         self.assertEqual(application.course, 'safety')
#         self.assertEqual(application.status, CourseApplication.STATUS_STUDYING)
#
#         response = self.client.post(reverse('admin_application_delete', args=[application.id]))
#         self.assertRedirects(response, reverse('admin_panel'))
#         self.assertFalse(CourseApplication.objects.filter(id=application.id).exists())
#
#     def test_review_available_only_after_finished_status(self):
#         user = User.objects.create_user('revusr', password='password123', email='revusr@example.com')
#         Profile.objects.create(user=user, full_name='Олег Орлов', phone='8(902)333-44-55')
#         application = CourseApplication.objects.create(
#             user=user,
#             course='retraining',
#             start_date='2026-05-25',
#             payment_method='cash',
#         )
#         self.client.login(username='revusr', password='password123')
#
#         response = self.client.get(reverse('add_review', args=[application.id]))
#         self.assertEqual(response.status_code, 404)
#
#         application.status = CourseApplication.STATUS_FINISHED
#         application.save()
#         response = self.client.post(reverse('add_review', args=[application.id]), {'text': 'Курс понравился'})
#         self.assertRedirects(response, reverse('dashboard'))
#         self.assertTrue(Review.objects.filter(application=application).exists())
