from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from requests import Response
from six import BytesIO

from userapp.models import UserModel

from PIL import Image


class Avavtar(TemplateView):
    template_name = "personalProfile/eprsonal-profile.html"

    def post(self, request, *args, **kwargs):
        user = UserModel.objects.get(username=request.user)

        # print(request)
        # print(request.POST)
        # print(request.headers['User-Agent'])

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
