from django.contrib.auth.mixins import UserPassesTestMixin
"""import  ghasedak_sms

def sms_otp_code(phone_number, code):
    pass
    sms_api = ghasedak_sms.Ghasedak(api_key='2ec629b813eb0acc6203f217fdc1300a3e79fe74921cdfb5dcc1700611318fa8PYEwpifNEaoFKshL')
    response = sms_api.send_single_sms(
        ghasedak_sms.SendSingleSmsInput(
            message=f'your code is{code}',
            receptor='09380060729',
            line_number='09380060729',
            send_date='',
            client_reference_id=''
        )
    )

    print(response)"""

class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin






