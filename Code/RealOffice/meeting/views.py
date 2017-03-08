from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

@login_required
def dashboard(request):
	context = {'username': request.user}
	return render(request, 'meeting/dash.html', context)

class LogOutView(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)

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