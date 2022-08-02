import asyncio
import json
from datetime import datetime
from xxlimited import new

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

from random import randint
from time import sleep

from .models import Notification
from .constants import *
from .exceptions import *
from .utils import *

from account.models import Account
from document.models import DocSKAI

class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        #when ws connect
        print("NotificationConsumer: connect: " + str(self.scope["user"]) )
        await self.accept()
        

    # async def websocket_receive(self,event):
    #     #when msg is received from ws
    #     print("received",event)

    #     sleep(1)

    #     await self.send({"type":"websocket.send","text":str(randint(0,100))})

    async def disconnect(self, event):
        #when ws disconnects
        print("disconnected", event)

    async def receive_json(self, content):
        """
		Called when we get a text frame. Channels will JSON-decode the payload
		for us and pass it as the first argument.
		"""

        command = content.get("command", None)
        print("NotificationConsumer: receive_json. Command: " + command)
        try:
            if command == "dummy_command":
                print("received dummy_command",event)
                sleep(1)
                await self.send({"type":"websocket.send","text":str(randint(0,100))})
            elif command == "get_general_notifications":
                payload = await get_general_notifications(self.scope["user"], content.get("page_number", None))
                if payload == None:
                    await self.general_pagination_exhausted()
                else:
                    payload = json.loads(payload)
                    await self.send_general_notifications_payload(payload['notifications'], payload['new_page_number'])
            elif command == "get_new_general_notifications":
                payload = await get_new_general_notifications(self.scope["user"], content.get("newest_timestamp", None))
                if payload != None:
                    payload = json.loads(payload)
                    await self.send_new_general_notifications_payload(payload['notifications'])
            elif command == "refresh_general_notifications":
                payload = await refresh_general_notifications(self.scope["user"], content['oldest_timestamp'], content['newest_timestamp'])
                if payload == None:
                    raise ClientError("UNKNOWN_ERROR", "Something went wrong. Try refreshing the browser.")
                else:
                    payload = json.loads(payload)
                    await self.send_general_refreshed_notifications_payload(payload['notifications'])
            elif command == "get_unread_general_notifications_count":
                payload = await get_unread_general_notification_count(self.scope["user"])
                if payload != None:
                    payload = json.loads(payload)
                    await self.send_unread_general_notification_count(payload['count'])
            elif command == "mark_notifications_read":
                await mark_notifications_read(self.scope["user"])
        except:
            pass
    
    async def general_pagination_exhausted(self):
        """
		Called by receive_json when pagination is exhausted for general notifications
		"""
		#print("General Pagination DONE... No more notifications.")
        await self.send_json(
			{
				"general_msg_type": GENERAL_MSG_TYPE_PAGINATION_EXHAUSTED,
			},
		)

    async def send_general_notifications_payload(self, notifications, new_page_number):
        """
		Called by receive_json when ready to send a json array of the notifications
		"""
		#print("NotificationConsumer: send_general_notifications_payload")
        await self.send_json(
			{
				"general_msg_type": GENERAL_MSG_TYPE_NOTIFICATIONS_PAYLOAD,
				"notifications": notifications,
				"new_page_number": new_page_number,
			},
		)
    
    async def send_new_general_notifications_payload(self, notifications):
        """
		Called by receive_json when ready to send a json array of the notifications
		"""
        await self.send_json(
			{
				"general_msg_type": GENERAL_MSG_TYPE_GET_NEW_GENERAL_NOTIFICATIONS,
				"notifications": notifications,
			},
		)

    async def send_general_refreshed_notifications_payload(self, notifications):
        """
		Called by receive_json when ready to send a json array of the notifications
		"""
		#print("NotificationConsumer: send_general_refreshed_notifications_payload: " + str(notifications))
        await self.send_json(
			{
				"general_msg_type": GENERAL_MSG_TYPE_NOTIFICATIONS_REFRESH_PAYLOAD,
				"notifications": notifications,
			},
		)
    
    async def send_unread_general_notification_count(self, count):
        """
		Send the number of unread "general" notifications to the template
		"""
        await self.send_json(
			{
				"general_msg_type": GENERAL_MSG_TYPE_GET_UNREAD_NOTIFICATIONS_COUNT,
				"count": count,
			},
		)

@database_sync_to_async
def get_general_notifications(user, page_number):
	#ADD COMENT LATER
    if user.is_authenticated:
        account_ct = ContentType.objects.get_for_model(Account)
        docSKAI_ct = ContentType.objects.get_for_model(DocSKAI)
        notifications = Notification.objects.filter(target=user, content_type__in=[account_ct, docSKAI_ct]).order_by('-timestamp')
        p = Paginator(notifications, DEFAULT_NOTIFICATION_PAGE_SIZE)
        payload = {}
        if len(notifications) > 0:
            if int(page_number) <= p.num_pages:
                s = CustomNotificationEncoder()
                serialized_notifications = s.serialize(p.page(page_number).object_list)
                payload['notifications'] = serialized_notifications
                new_page_number = int(page_number) + 1
                payload['new_page_number'] = new_page_number
        else:
            return None    
    else:
        raise ClientError("AUTH_ERROR", "User must be authenticated to get notifications.")
    
    return json.dumps(payload)

@database_sync_to_async
def get_new_general_notifications(user, newest_timestamp):
    """
    Retrieve any notifications newer than the newest_timestamp on the screen
    """
    payload = {}
    if user.is_authenticated:
        timestamp = newest_timestamp[0:newest_timestamp.find("+")] #remove tz because who cares
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')

        account_ct = ContentType.objects.get_for_model(Account)
        docSKAI_ct = ContentType.objects.get_for_model(DocSKAI)
        notifications = Notification.objects.filter(target=user, content_type__in=[account_ct, docSKAI_ct], timestamp__gt=timestamp, read=False).order_by('-timestamp')
        s = CustomNotificationEncoder()
        payload['notifications'] = s.serialize(notifications)
    else:
        raise ClientError("AUTH_ERROR", "User must be authenticated to get notifications.")

    return json.dumps(payload)
        


@database_sync_to_async
def refresh_general_notifications(user, oldest_timestamp, newest_timestamp):
	"""
	Retrieve the general notifications newer than the oldest one on the screen and younger than the newest one the screen.
	The result will be: Notifications currently visible will be updated
	"""
	payload = {}
	if user.is_authenticated:
        
		oldest_ts = oldest_timestamp[0:oldest_timestamp.find("+")] # remove timezone because who cares
		print(oldest_ts)
		oldest_ts = datetime.strptime(oldest_ts, '%Y-%m-%d %H:%M:%S.%f')
		print(oldest_ts)
		print("newest_ts")
		print(newest_timestamp)
		newest_ts = newest_timestamp[0:newest_timestamp.find("+")] # remove timezone because who cares
		#print(newest_ts)
		newest_ts = datetime.strptime(newest_ts, '%Y-%m-%d %H:%M:%S.%f')
		#print(newest_ts)
		notifications = Notification.objects.filter(target=user, content_type__in=[ContentType.objects.get_for_model(Account), ContentType.objects.get_for_model(DocSKAI)], timestamp__gte=oldest_ts, timestamp__lte=newest_ts).order_by('-timestamp')

		s = CustomNotificationEncoder()
		payload['notifications'] = s.serialize(notifications)
	else:
		raise ClientError("AUTH_ERROR", "User must be authenticated to get notifications.")
    
	return json.dumps(payload)

@database_sync_to_async
def get_unread_general_notification_count(user):
	payload = {}
	if user.is_authenticated:
		notifications = Notification.objects.filter(target=user, content_type__in=[ContentType.objects.get_for_model(Account), ContentType.objects.get_for_model(DocSKAI)])

		unread_count = 0
		if notifications:
			for notification in notifications.all():
				if not notification.read:
					unread_count = unread_count + 1
		payload['count'] = unread_count
		return json.dumps(payload)
	else:
		raise ClientError("AUTH_ERROR", "User must be authenticated to get notifications.")
	return None

@database_sync_to_async
def mark_notifications_read(user):
	"""
	marks a notification as "read"
	"""
	if user.is_authenticated:
		notifications = Notification.objects.filter(target=user)
		if notifications:
			for notification in notifications.all():
				notification.read = True
				notification.save()
	return
