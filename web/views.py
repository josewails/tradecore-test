from django.views.generic import TemplateView


class SignupView(TemplateView):
    template_name = "posts/signup.html"


class HomeView(TemplateView):
    template_name = "posts/home.html"


class LoginView(TemplateView):
    template_name = "posts/login.html"
