
"""
get:
    输入:
        {
            "groupId":"xxxx"
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.Resume,modules.Rank, modules.User

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
            "data":[
                "resumeId":11111,
                "groupId":"xxx",
                "username":"xxx",
                "qq":"xxx", //优先使用modules.Resume中的qq
                "lastDate":1400000 , //unix时间戳
                "myRank":12,
                "averageRank":20,
                "content":"xxxxx",
                "status":0|1|2
                ]

        }
put:
    输入:
        {
            "resumeId":111,//必需
            "status":0|1|2,//选
            "myRank":222,//选
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.Resume,modules.Rank

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
        }
delete:
    输入:
        {
            "resumeId":111,//必需
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.Resume,modules.Rank

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
        }

"""

from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Avg
from django.forms import (Form, CharField, IntegerField, ChoiceField)

from .check_request import CheckRequest
from api.models import Resume, Rank, User


class putForm(Form):
    STATUS_CHOICES = (
        (0,u'申请中'),
        (1,u'允许的'),
        (2,u'拒绝的'),
        (3,u'拉黑的'),
    )
    resumeId = IntegerField()
    status = ChoiceField(choices=STATUS_CHOICES, required=False)
    rank = IntegerField(required=False)

class DelForm(Form):
    resumeId = IntegerField()

class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status": "error",
                                "msg": "Only admin permitted"})
        data = {"status" :  "success",
                "msg" :  '',
                "data" : []
                }
        resumes = Resume.objects.filter(groupID = check.admin.groupID)
        for item in resumes:
            print('item', item)
            user = User.objects.filter(email = item.userEmail).first()
            allRank = Rank.objects.filter(resumeId = item.id)
            rank = allRank.filter(adminName = check.admin.adminName).first()
            avgRank = allRank.aggregate(Avg('rank'))
            if not user:
                return JsonResponse({"status": "error",
                                    "msg": "Resume without valid user"})
            resume = {
                "resumeId": item.id,
                "groupId": item.groupID,
                "username": user.username,
                "qq": item.qq,
                "lastDate": item.lastDate.strftime('%Y-%m-%d'),
                "content": item.content,
                "status": item.status
            }
            if not rank: 
                resume['myRank'] = u'尚未评分'
            else:
                resume['myRank'] = rank.rank
            #不知这个是用户的averageRank还是简历的averageRank?现在是简历的averageRank
            resume['averageRank'] = avgRank['rank__avg']
            data['data'].append(resume)
        return JsonResponse(data)
        
    def post(self, request):
        return JsonResponse({"status":"success",
                             "msg":""})

    def put(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status": "error",
                                "msg": "Only admin permitted"})
        uf = DelForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status": "error",
                                "msg": "resumeId is invalid."})
        resume = Resume.objects.filter(id = uf.cleaned_data['resumeId']).first()
        if uf.cleaned_data['status']:
            resume.status = uf.cleaned_data['status']
        if uf.cleaned_data['rank']:
            resume.rank = uf.cleaned_data['rank']
        resume.save()
        return JsonResponse({"status":"success",
                             "msg":""})

    def delete(self, request):
        #删除部分是不是有二次确认比较好？
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status": "error",
                                "msg": "Only admin permitted"})
        uf = DelForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status": "error",
                                "msg": "resumeId is invalid."})
        Resume.objects.filter(id = uf.cleaned_data['resumeId']).delete()
        Rank.objects.filter(resumeId = uf.cleaned_data['resumeId']).delete()
        return JsonResponse({"status":"success",
                             "msg":""})