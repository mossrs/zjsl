from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class LoginRequiredJSONMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        return JsonResponse({'code': 4003, 'errormsg': '用户未登陆'})
