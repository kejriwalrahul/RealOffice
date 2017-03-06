from django.shortcuts import render

# Rest framework stuff
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Python Libs
from datetime import datetime

"""
	For checking presence of required keys in incoming requests
"""
def check_dict(dictionary, keys):
	for key in keys:
		if key not in dictionary:
			return False

	return True

"""
class ExampleView(APIView):
	permission_classes = (IsAuthenticated, )

	def get(self, request):
		content = {
			'user': unicode(request.user),
			'auth': unicode(request.auth)
		}
		return Response(content, status=status.HTTP_200_OK)
"""