from django.shortcuts import render
from urllib.request import urlretrieve
import requests
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from viberbot.api.messages import TextMessage, PictureMessage, VideoMessage, KeyboardMessage, ContactMessage
from django.conf import settings
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from django.http import HttpResponse
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from .models import Userviber
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse


bot_configuration = BotConfiguration(
    name='CarDefinded',
    avatar='http://viber.com/avatar.jpg',
    auth_token='4a863d7cf8e7d212-e12f20b5630e4685-d3dd7d2b4fabe81e'
)
viber = Api(bot_configuration)


class ViberUserView(View):
    def get(self, request):
        return HttpResponse('Hi')


class ViberUserListView(ListView):
    model = Userviber

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_var'] = 'TESTJDSKJQ'
        return context


class ViberUserCreate(CreateView):
    model = Userviber
    fields = ['name', 'country']

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users_all')


@csrf_exempt
def set_webhook(request):
    event_types = ['failed',
                   'subscribed',
                   'unsubscribed',
                   'conversation_started']
    url = f'https://{settings.ALLOWED_HOSTS[0]}/viber/callback/'
    viber.set_webhook(url=url, webhook_events=event_types)
    return HttpResponse('OK')


@csrf_exempt
def unset_webhook(request):
    viber.unset_webhook()
    return HttpResponse('Off')


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        viber_request = viber.parse_request(request.body)
        if isinstance(viber_request, ViberSubscribedRequest):
            viber.send_messages(viber_request.user.id, [TextMessage(text='Thank you for subscribed')])
            user, create = Userviber.objects.update_or_create(viber_id=viber_request.user.id,
                                                              defaults={'is_active': True},
                                                              name=viber_request.user.name,
                                                              country=viber_request.user.country,
                                                              )
            if user.phone_number is None:
                SAMPLE_KEYBOARD = {
                    "Type": "keyboard",
                    "BgColor": "#FFFFFF",
                    "Buttons": [
                        {
                            "Columns": 6,
                            "Rows": 2,
                            "BgColor": "#2db9b9",
                            "BgLoop": True,
                            "ActionType": "share-phone",
                            "ActionBody": "This will be sent to your bot in a callback",
                            "ReplayType": "message",
                            "TextOpacity": 100,
                            "TextSize": "regular",
                            "Text": "<font color = '#ffff00'> Push me! </font>",
                        }
                    ]
                }
                keyboard_message = KeyboardMessage(tracking_data='tracking_data',
                                                   keyboard=SAMPLE_KEYBOARD,
                                                   min_api_version=3)
                viber.send_messages(user.viber_id, [keyboard_message])

            # print(viber_request)
        elif isinstance(viber_request, ViberMessageRequest):
            if isinstance(viber_request.message, TextMessage):
                viber.send_messages(viber_request.sender.id, [TextMessage(text='This is text')])
            elif isinstance(viber_request.message, PictureMessage):
                viber.send_messages(viber_request.sender.id, [TextMessage(text='This is picture')])
            elif isinstance(viber_request.message, VideoMessage):
                viber.send_messages(viber_request.sender.id, [TextMessage(text='This is video')])
            elif isinstance(viber_request.message, ContactMessage):
                print(viber_request)
                Userviber.objects.update_or_create(viber_id=viber_request.sender.id,
                                                   defaults={'is_active': True},
                                                   name=viber_request.sender.name,
                                                   country=viber_request.sender.country,
                                                   phone_number=viber_request.message.contact.phone_number,
                                                   )
                text_message = TextMessage(text="Number if fine")
                viber.send_messages(viber_request.sender.id, [text_message])
        return HttpResponse(status=200)
# Create your views here.
