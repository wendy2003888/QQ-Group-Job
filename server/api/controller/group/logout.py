__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View


class Index(View):
    def get(self, request):

        response = JsonResponse({"status":"success",
                                 "msg":""
                                 })
        response.delete_cookie("admin_token")
        response.delete_cookie("admin_logined")
        return  response