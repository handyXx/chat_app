from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View

from chat.models import Chat
from account.models import Friends

User = get_user_model()


def index(request):
    return render(request, "index.html", {})


def room(request, room_name):
    return render(request, "chatroom.html", {"room_name": room_name})


def chatroom(request):
    return render(request, "chat_room.html")


class ThreadView(LoginRequiredMixin, View):
    template_name = "one_room_chat.html"

    def dispatch(self, request, *args, **kwargs):
        user_check = self.kwargs["username"]

        print(Friends.objects.filter(user=self.request.user))

        if not User.objects.filter(username=user_check).exists():
            return render(self.request, "user_not_found.html")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Chat.objects.by_user(self.request.user)

    def get_object(self):
        other_username = self.kwargs.get("username")
        self.other_user = User.objects.get(username=other_username)
        obj = Chat.objects.get_or_create_personal_thread(
            self.request.user, self.other_user
        )
        if obj == None:
            raise Http404

        return obj

    def get_context_data(self, **kwargs):
        context = {}
        context["friends"] = Friends.objects.filter(user=self.request.user)[0].friends.all()
        context["me"] = self.request.user
        context["reciever"] = self.kwargs["username"]
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)
