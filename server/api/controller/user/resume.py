__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View

from .check_request import CheckRequest
from api.models import Resume, Group, GroupAdmin
from django.forms import (Form, CharField, EmailField, IntegerField, BooleanField, Textarea)

from api.send_mail import start_mail_thread
from api.config import domain, protocol, admin_email, admin_group
from QQJob.settings import BASE_DIR
from api.response_code import errorCode, successCode

class GetForm(Form):
    groupId = IntegerField()
class DeleteForm(Form):
    groupId = IntegerField()

class PostForm(Form):
    jobTitle = CharField(max_length=20)
    email = EmailField(max_length=17)
    groupId = CharField(max_length=15) #所属群
    qq = CharField(max_length=15)
    username = CharField(max_length=50)
    sex = IntegerField()
    age = IntegerField(min_value=15, max_value=100)
    yearsOfWorking = IntegerField(min_value=0, max_value=60)
    school = CharField(max_length=40)
    education = IntegerField()
    content = CharField(widget=Textarea, required=False)
    display = BooleanField()

class PutForm(Form):
    id = IntegerField()
    jobTitle = CharField(max_length=20)
    email = EmailField(max_length=17)
    qq = CharField(max_length=15)
    username = CharField(max_length=50)
    sex = IntegerField()
    age = IntegerField(min_value=15, max_value=100)
    yearsOfWorking = IntegerField(min_value=0, max_value=60)
    school = CharField(max_length=40)
    education = IntegerField()
    content = CharField(widget=Textarea, required=False)
    display = BooleanField( required= False)



class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.user:
            return JsonResponse({
                "status": "error",
                "code":10000,
                "msg": errorCode[10000]
            })
        uf = GetForm(check.jsonForm)
        if uf.is_valid():
            item = Resume.objects.filter(groupId__exact = uf.cleaned_data['groupId'], qq__exact = check.user.qq).first()
            if item:
                group = Group.objects.filter(groupId__exact = item.groupId).first()
                groupName = ""
                if group:
                    groupName = group.groupName
                return JsonResponse({
                    "status": 'success',
                    'msg': '',
                    'count': 1,
                    'data':{
                        'id': item.id,
                        'jobTitle': item.jobTitle,
                        'email': item.userEmail,
                        "groupId": item.groupId,
                        "groupName": groupName,
                        "username": item.username,
                        "qq": item.qq,
                        'sex': item.sex,
                        'age': item.age,
                        'yearsOfWorking': item.yearsOfWorking,
                        'school': item.school,
                        'education': item.education,
                        "lastDate": item.lastDate.strftime('%Y-%m-%d'),
                        "content": item.content,
                        'display': item.display,
                        "status": item.status
                    }
                })
            else:
                group = Group.objects.filter(groupId__exact = uf.cleaned_data['groupId']).first()
                if not group:
                    return JsonResponse({
                        "status": 'success',
                        "code":30002,
                        "msg": successCode[30002]
                    })

                groupName = group.groupName
                return JsonResponse({"status": 'success',
                                 'msg': "Resume not found",
                                 'count': 0,
                                 'data':{
                                     "groupId": uf.cleaned_data['groupId'],
                                     "groupName": groupName,
                                     "username": check.user.username,
                                     'email': check.user.qq + "@qq.com",
                                     "qq": check.user.qq,
                                     'sex': check.user.sex,
                                     'age': check.user.age,
                                     'yearsOfWorking': check.user.yearsOfWorking,
                                     'school': check.user.school,
                                     'display': True,
                                     "content": '',
                                     'education': check.user.education
                                 }
                            })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "Form is error"
                                 })
    def post(self, request):
        check = CheckRequest(request)
        if not check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User not logined"
            })
        uf = PostForm(check.jsonForm)
        if uf.is_valid():
            group = Group.objects.filter(groupId__exact = uf.cleaned_data['groupId']).first()
            groupName = ""
            if group:
                groupName = group.groupName
            checkResume = Resume.objects.filter(groupId__exact = uf.cleaned_data['groupId'], qq__exact=uf.cleaned_data['qq']).first()
            if checkResume:
                return JsonResponse({
                    "status": "success",
                    "code":30003,
                    "msg": successCode[30003],
                    'count': 1,
                    'data':{
                        'id': checkResume.id,
                        'jobTitle': checkResume.jobTitle,
                        'email': checkResume.userEmail,
                        "groupId": checkResume.groupId,
                        "groupName": groupName,
                        "username": checkResume.username,
                        "qq": checkResume.qq,
                        'sex': checkResume.sex,
                        'age': checkResume.age,
                        'yearsOfWorking': checkResume.yearsOfWorking,
                        'school': checkResume.school,
                        'education': checkResume.education,
                        "lastDate": checkResume.lastDate,
                        "content": checkResume.content,
                        'display': checkResume.display,
                        "status": checkResume.status
                    }
                })
            resume = Resume(
                jobTitle= uf.cleaned_data['jobTitle'],
                userEmail = uf.cleaned_data['email'],
                groupId = uf.cleaned_data['groupId'],
                qq = uf.cleaned_data['qq'],
                username = uf.cleaned_data['username'],
                sex = uf.cleaned_data['sex'],
                age = uf.cleaned_data['age'],
                yearsOfWorking = uf.cleaned_data['yearsOfWorking'],
                school = uf.cleaned_data['school'],
                education = uf.cleaned_data['education'],
                content = uf.cleaned_data['content'],
                display = uf.cleaned_data['display']
            )
            resume.save()
            if resume.id:
                responseCode = 30000
                try:
                    with open(BASE_DIR + "/api/mail_template/remind.html", 'rt', encoding='utf-8') as mail_template:
                        template = mail_template.read()
                    admins = GroupAdmin.objects.filter(groupId = resume.groupId,
                                                        status= 1).all()
                    link = "%s://%s/#/group/resume/%s" % (protocol, domain, str(resume.id))
                    email_content = template % (groupName, resume.username, resume.qq, link, admin_email, admin_group)
                    start_mail_thread(
                        'Qjob新用户入群',
                        email_content,
                        ['%s@qq.com' % admin.qq for admin in admins]
                        )
                except:
                    responseCode = 30001
                return JsonResponse({
                    "status": 'success',
                    'msg': successCode[responseCode],
                    'code': responseCode,
                    'count': 1,
                    'data':{
                        'id': resume.id,
                        'jobTitle': resume.jobTitle,
                        'email': resume.userEmail,
                        "groupId": resume.groupId,
                        "groupName": groupName,
                        "username": resume.username,
                        "qq": resume.qq,
                        'sex': resume.sex,
                        'age': resume.age,
                        'yearsOfWorking': resume.yearsOfWorking,
                        'school': resume.school,
                        'education': resume.education,
                        "lastDate": resume.lastDate,
                        "content": resume.content,
                        'display': resume.display,
                        "status": resume.status
                    }
                })
            else:
                return JsonResponse({
                    "status" : 'error',
                    'msg' : "Save error"
                    })
        else:
            return JsonResponse({
                "status": "error",
                "msg": "From error: %s" % uf.errors
            })
    def put(self, request):
        check = CheckRequest(request)
        if not check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User not logined"
            })
        uf = PutForm(check.jsonForm)
        if uf.is_valid():
            item = Resume.objects.filter(id__exact = uf.cleaned_data['id'], qq__exact = check.user.qq).first()
            if item:
                item.jobTitle = uf.cleaned_data['jobTitle']
                item.userEmail = uf.cleaned_data['email']
                item.qq = uf.cleaned_data['qq']
                item.username = uf.cleaned_data['username']
                item.sex = uf.cleaned_data['sex']
                item.age = uf.cleaned_data['age']
                item.yearsOfWorking = uf.cleaned_data['yearsOfWorking']
                item.school = uf.cleaned_data['school']
                item.education = uf.cleaned_data['education']
                item.content = uf.cleaned_data['content']
                item.display = uf.cleaned_data['display']
                item.save()
                print(uf.cleaned_data['jobTitle'])
                return JsonResponse({"status": 'success',
                                 'msg': ""
                                 })
            else:
                return JsonResponse({"status": 'error',
                                 'msg': "id not found:%s" % uf.cleaned_data['id']
                                 })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "Form is error:%s" % uf.errors
                                 })

    def delete(self, request):
        check = CheckRequest(request)
        if not check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User not logined"
            })
        uf = DeleteForm(check.jsonForm)
        if uf.is_valid():
            item = Resume.objects.filter(groupId__exact = uf.cleaned_data['groupId'], qq__exact = check.user.qq).first()
            if item:
                item.delete()
                return JsonResponse({"status": 'success',
                                 'msg': ""
                                 })
            else:
                return JsonResponse({"status": 'error',
                                 'msg': "groupId not found:%s" % uf.cleaned_data['groupId']
                                 })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "Form is error:%s" % uf.errors
                                 })



