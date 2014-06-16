from django.shortcuts import render, redirect
from download.models import Downloader
from django.utils import timezone
from django.views import generic


class GoView(generic.View):
    def post(self, request):
        Downloader.objects.create(email=request.POST['email'],
                                  name=request.POST['name'],
                                  comment=request.POST['comment'],
                                  registration_date=timezone.now())
        return render(request, 'download/go.html')

    def get(self, request):
        return redirect('download:index')
