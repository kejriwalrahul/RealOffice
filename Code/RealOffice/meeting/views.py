# Django Stuff
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Rest framework stuff
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Python Libs
from datetime import datetime

# Import Models
from . import models

"""
	For checking presence of required keys in incoming requests
"""
def check_dict(dictionary, keys):
	for key in keys:
		if key not in dictionary:
			return False

	return True


def loginpage(request):
	context = {}
	return render(request, 'meeting/login.html', context)


def dashboard(request):
	context = {'username': request.user}
	return render(request, 'meeting/dash.html', context)


class LogOutView(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)

class UserInfo(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		res_data = {
			'user': unicode(request.user),
			'auth': unicode(request.auth)
		}

		return Response(res_data, status=status.HTTP_200_OK)

class ChangePassword(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):

		if not check_dict(request.data, ['old_pass', 'new_pass']):
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

		if not request.user.check_password(request.data['old_pass']):
			return Response({}, status=status.HTTP_403_FORBIDDEN)

		request.user.set_password(request.data['new_pass'])
		request.user.save()

		return Response({}, status=status.HTTP_200_OK)