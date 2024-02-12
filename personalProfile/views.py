import random

from django.contrib.auth import get_user_model
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from personalProfile import logic

from requests import Response

from personalProfile.models import EmailCodeModel

# from personalProfile.models import EmailCode


UserModel = get_user_model()


class Avavtar(LoginRequiredMixin, TemplateView):
    template_name = "personalProfile/eprsonal-profile.html"

    def post(self, request, *args, **kwargs):
        user = UserModel.objects.get(username=request.user)

        if request.POST.get("Name", None):
            user.first_name = request.POST["Name"]

        if request.POST.get("Surname", None):
            user.middle_name = request.POST["Surname"]

        if request.POST.get("Second-surname", None):
            user.last_name = request.POST["Second-surname"]

        if request.POST.get("description", None):
            user.description = request.POST["description"]

        if request.POST.get("email", None):
            user.email = request.POST["email"]

        if request.POST.get("phone_number", None):
            user.phone_number = request.POST["phone_number"]

        user.save()

        return redirect("avatar")


class EmailCode(LoginRequiredMixin, TemplateView):
    template_name = "personalProfile/email-code.html"

    def post(self, request, *args, **kwargs):
        mail_address = request.POST['email-address']

        email_code = random.randint(1000000000, 9999999999)

        send_mail(
            "Subject here",
            f"{email_code}",
            "na2aroffnikita@yandex.ru",
            [f"{mail_address}"],
            fail_silently=False,
        )

        EmailCodeModel.objects.create(user=request.user,
                                      code=email_code)

        response = render(request, template_name="personalProfile/input-email-code.html")
        response.set_cookie("email_address", f"{mail_address}", 3600)

        return response


def set_email(request):
    email_address = request.COOKIES["email_address"]
    code = request.POST.get('code', None)
    email_code_obj = EmailCodeModel.objects.get(user=request.user,
                                                code=code)

    user = UserModel.objects.get(id=request.user.id)

    if email_code_obj.code == int(code):
        user.email = email_address
        user.save()
        return redirect("avatar")

    return HttpResponse("чет пошло не так")
