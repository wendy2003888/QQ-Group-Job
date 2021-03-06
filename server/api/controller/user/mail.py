from django.http import JsonResponse
from django.views.generic import View
from api.send_mail import start_mail_thread
from api.models import User
from api.token import new_token
from api.config import domain, protocol, user_email, user_group
from QQJob.settings import BASE_DIR
from django.forms import (Form, CharField)

class qqForm(Form):
    qq = CharField(max_length=15)

class Activate(View):
    def get(self, request):
        uf = qqForm(request.GET)
        if not uf.is_valid():
            return JsonResponse({
                "status": "error",
                "msg": "激活邮件发送失败:%s" % uf.errors
            })

        qq = uf.cleaned_data["qq"]
        user = User.objects.filter(qq__exact = qq).first()
        if user is None:
            msg = {
                "status" : 'error',
                "msg" : '用户不存在'
            }
        else:
            if user.status == 1:
                msg = {
                    "status" : 'error',
                    "msg" : '用户已激活'
                }
            else:

                with open(BASE_DIR + "/api/mail_template/activate.html", 'rt', encoding='utf-8') as mail_template:
                    template = mail_template.read()
                token = new_token(user, 'activate').get_token()
                link = "%s://%s/api/activate/?token=%s" % (protocol, domain, token)
                email_content = template % (user.qq, link, user_email, user_group)


                start_mail_thread(
                    'Qjob账户激活',
                    email_content,
                    ['%s@qq.com' % user.qq]
                )

                msg = {
                    "status" : 'success',
                    "msg" : '邮件已发送,请注意查收'
                }
        return JsonResponse(msg)

class Recover(View):
    def get(self, request):
        uf = qqForm(request.GET)
        if not uf.is_valid():
            return JsonResponse({
                "status": "error",
                "msg": "邮件发送失败"
            })

        qq = uf.cleaned_data["qq"]
        user = User.objects.filter(qq__exact= qq).first()
        if user is None:
            msg = {
                "status" : 'error',
                "msg" : 'user not exist'
            }
        else:
            with open(BASE_DIR + "/api/mail_template/recover.html", 'rt', encoding='utf-8') as mail_template:
                template = mail_template.read()
            token = new_token(user, 'recover').get_token()
            link = "%s://%s/#/new_pwd/%s" %(protocol, domain, token)
            email_content = template % (user.qq, link, user_email, user_group)

            start_mail_thread(
                'Qjob账户密码重置',
                email_content,
                ['%s@qq.com' % user.qq]
            )

            msg = {
                "status" : 'success',
                "msg" : '邮件已发送,请注意查收'
            }
        return JsonResponse(msg)

