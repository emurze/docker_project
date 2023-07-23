from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from apps.base.forms import ShareForm
from apps.base.models import Post


class Share(View):
    template_name = 'pages/share/share.html'

    def get(self, request: WSGIRequest, pk: int) -> HttpResponse:
        post = get_object_or_404(Post, pk=pk)
        context = {
            'post': post,
            'share_form': ShareForm()
        }
        return render(request, self.template_name, context)

    def post(self, request: WSGIRequest, pk: int) -> HttpResponse:
        post = get_object_or_404(Post, pk=pk)

        sent = False
        if (form := ShareForm(request.POST, request.FILES)).is_valid():
            cd = form.cleaned_data
            send_mail(
                subject=cd['name'] + request.build_absolute_uri(
                    post.get_absolute_url()
                ),
                message=cd['content'],
                from_email=cd['email'],
                recipient_list=(cd['email_to'],),
                fail_silently=False,
            )
            sent = True

        context = {
            'post': post,
            'share_form': form,
            'sent': sent,
        }
        return render(request, self.template_name, context)
