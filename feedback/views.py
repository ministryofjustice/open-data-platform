from django.shortcuts import render
from feedback.models import Feedback
from django.utils import timezone
from django.views import generic


class ThanksView(generic.View):
    def post(self, request):
        Feedback.objects.create(email=request.POST['email'],
                                name=request.POST['name'],
                                comment=request.POST['comment'],
                                date=timezone.now())
        return render(request, 'feedback/thanks.html')

    def get(self, request):
        return redirect('feedback:index')

