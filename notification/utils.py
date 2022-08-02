from django.core.serializers.python import Serializer
from django.core.serializers.json import Serializer as JSONSerializer
from django.contrib.humanize.templatetags.humanize import naturaltime

from account.models import Account


class LazyNotificationEncoder(Serializer):
	"""
	Serialize a Notification into JSON. 
	There are 3 types
		1. FriendRequest
		2. FriendList
		3. UnreadChatRoomMessage
	"""
	def get_dump_object(self, obj):
		dump_object = {}
		if obj.get_content_object_type() == "Account":
			dump_object.update({'notification_type': obj.get_content_object_type()})
			dump_object.update({'notification_id': str(obj.pk)})
			dump_object.update({'verb': obj.verb})
			dump_object.update({'is_active': str(obj.content_object.is_active)})
			dump_object.update({'is_read': str(obj.read)})
			dump_object.update({'natural_timestamp': str(naturaltime(obj.timestamp))})
			dump_object.update({'timestamp': str(obj.timestamp)})
			dump_object.update({
				'actions': {
					'redirect_url': str(obj.redirect_url),
				},
				"from": {
					"image_url": str(obj.from_user.profile_image.url)
				}
			})
		
		return dump_object

class CustomNotificationEncoder(JSONSerializer):

	def get_dump_object(self, obj):
		dump_object = {}
		try:
			if obj.get_content_object_type() == "Account":
				dump_object.update({'notification_type': obj.get_content_object_type()})
				dump_object.update({'notification_id': str(obj.pk)})
				dump_object.update({'verb': obj.verb})
				dump_object.update({'is_active': str(obj.content_object.is_active)})
				dump_object.update({'is_read': str(obj.read)})
				dump_object.update({'natural_timestamp': str(naturaltime(obj.timestamp))})
				dump_object.update({'timestamp': str(obj.timestamp)})
				dump_object.update({
					'actions': {
						'redirect_url': str(obj.redirect_url),
					},
					"from": {
						"image_url": str("https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png")
					}
				})
			elif obj.get_content_object_type() == "DocSKAI":
				dump_object.update({'notification_type': obj.get_content_object_type()})
				dump_object.update({'notification_id': str(obj.pk)})
				dump_object.update({'verb': obj.verb})
				dump_object.update({'is_active': str(obj.content_object.is_active)})
				dump_object.update({'is_read': str(obj.read)})
				dump_object.update({'natural_timestamp': str(naturaltime(obj.timestamp))})
				dump_object.update({'timestamp': str(obj.timestamp)})
				dump_object.update({
					'actions': {
						'redirect_url': str(obj.redirect_url),
					},
					"from": {
						"image_url": str("https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png")
					}
				})
			else:
				print("Not Account")
		except Exception as e: 
			print(e)
			

		return dump_object