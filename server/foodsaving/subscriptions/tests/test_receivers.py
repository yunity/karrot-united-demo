import json

import requests_mock
from channels.test import ChannelTestCase, WSClient
from dateutil.parser import parse
from django.utils import timezone
from pyfcm.baseapi import BaseAPI as FCMApi

from foodsaving.conversations.factories import ConversationFactory
from foodsaving.conversations.models import ConversationMessage
from foodsaving.groups.factories import GroupFactory
from foodsaving.subscriptions.models import PushSubscriptionPlatform, PushSubscription, ChannelSubscription
from foodsaving.users.factories import UserFactory
from foodsaving.utils.tests.fake import faker


class ReceiverTests(ChannelTestCase):
    def test_receives_messages(self):
        client = WSClient()
        user = UserFactory()
        author = UserFactory()

        # join a conversation
        conversation = ConversationFactory()
        conversation.join(user)
        conversation.join(author)

        # login and connect
        client.force_login(user)
        client.send_and_consume('websocket.connect', path='/')

        # add a message to the conversation
        message = ConversationMessage.objects.create(conversation=conversation, content='yay', author=author)

        # hopefully they receive it!
        response = client.receive(json=True)
        response['payload']['created_at'] = parse(response['payload']['created_at'])
        self.assertEqual(response, {
            'topic': 'conversations:message',
            'payload': {
                'id': message.id,
                'content': message.content,
                'author': message.author.id,
                'conversation': conversation.id,
                'created_at': message.created_at
            }
        })

    def tests_receive_message_on_leave(self):
        client = WSClient()
        user = UserFactory()

        # join a conversation
        conversation = ConversationFactory()
        conversation.join(user)

        # login and connect
        client.force_login(user)
        client.send_and_consume('websocket.connect', path='/')

        conversation.leave(user)

        self.assertEqual(client.receive(json=True), {
            'topic': 'conversations:leave',
            'payload': {
                'id': conversation.id
            }
        })


@requests_mock.Mocker()
class ReceiverPushTests(ChannelTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.author = UserFactory()

        self.token = faker.uuid4()
        self.content = faker.text()

        # join a conversation
        self.conversation = ConversationFactory()
        self.conversation.join(self.user)
        self.conversation.join(self.author)

        # add a push subscriber
        PushSubscription.objects.create(user=self.user, token=self.token, platform=PushSubscriptionPlatform.ANDROID)

    def test_sends_to_push_subscribers(self, m):
        def check_json_data(request):
            data = json.loads(request.body.decode('utf-8'))
            self.assertEqual(data['notification']['title'], self.author.display_name)
            self.assertEqual(data['notification']['body'], self.content)
            self.assertEqual(data['to'], self.token)
            return True

        m.post(FCMApi.FCM_END_POINT, json={}, additional_matcher=check_json_data)

        # add a message to the conversation
        ConversationMessage.objects.create(conversation=self.conversation, content=self.content, author=self.author)

    # TODO: add back in once https://github.com/yunity/karrot-frontend/issues/770 is implemented
    # def test_does_not_send_push_notification_if_active_channel_subscription(self, m):
    #     # add a channel subscription to prevent the push being sent
    #     ChannelSubscription.objects.create(user=self.user, reply_channel='foo')
    #
    #     # add a message to the conversation
    #     ConversationMessage.objects.create(conversation=self.conversation, content=self.content, author=self.author)
    #
    #     # if it sent a push message, the requests mock would complain there is no matching request...

    def test_send_push_notification_if_channel_subscription_is_away(self, m):
        def check_json_data(request):
            data = json.loads(request.body.decode('utf-8'))
            self.assertEqual(data['notification']['title'], self.author.display_name)
            self.assertEqual(data['notification']['body'], self.content)
            self.assertEqual(data['to'], self.token)
            return True

        m.post(FCMApi.FCM_END_POINT, json={}, additional_matcher=check_json_data)

        # add a channel subscription to prevent the push being sent
        ChannelSubscription.objects.create(user=self.user, reply_channel='foo', away_at=timezone.now())

        # add a message to the conversation
        ConversationMessage.objects.create(conversation=self.conversation, content=self.content, author=self.author)


@requests_mock.Mocker()
class GroupConversationReceiverPushTests(ChannelTestCase):
    def setUp(self):
        self.group = GroupFactory()
        self.user = UserFactory()
        self.author = UserFactory()
        self.group.add_member(self.user)
        self.group.add_member(self.author)

        self.token = faker.uuid4()
        self.content = faker.text()

        self.conversation = self.group.conversation

        # add a push subscriber
        PushSubscription.objects.create(user=self.user, token=self.token, platform=PushSubscriptionPlatform.ANDROID)

    def test_sends_to_push_subscribers(self, m):
        def check_json_data(request):
            data = json.loads(request.body.decode('utf-8'))
            self.assertEqual(data['notification']['title'], self.group.name + ' / ' + self.author.display_name)
            self.assertEqual(data['notification']['body'], self.content)
            self.assertEqual(data['to'], self.token)
            return True

        m.post(FCMApi.FCM_END_POINT, json={}, additional_matcher=check_json_data)

        # add a message to the conversation
        ConversationMessage.objects.create(conversation=self.conversation, content=self.content, author=self.author)
