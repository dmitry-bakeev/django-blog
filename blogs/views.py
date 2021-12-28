from django.contrib.auth.views import LoginView


class BlogLoginView(LoginView):
    template_name = 'blogs/login-form.html'
