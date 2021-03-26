from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives

from django.utils.translation import ugettext_lazy as _
import binascii
import os
from django.template.loader import render_to_string
# Create your models here.

# Make part of the model eventually, so it can be edited
EXPIRY_PERIOD = 1   # days


def _generate_code():
    return binascii.hexlify(os.urandom(20)).decode('utf-8')


class CustomUser(AbstractUser):

    username = models.CharField(blank=True, null=True, max_length=150)
    fullname = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(auto_now=False, auto_now_add=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', "username", "phone", "birthday"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SignupCodeManager(models.Manager):
    def create_signup_code(self, user, ipaddr):
        code = _generate_code()
        signup_code = self.create(user=user, code=code, ipaddr=ipaddr)

        return signup_code

    def set_user_is_verified(self, code):
        try:
            signup_code = SignupCode.objects.get(code=code)
            signup_code.user.is_active = True
            signup_code.user.save()
            return True
        except SignupCode.DoesNotExist:
            pass

        return False


def send_multi_format_email(template_prefix, template_ctxt, target_email):

    subject_file = '%s_subject.txt' % template_prefix
    txt_file = '%s.txt' % template_prefix
    html_file = '%s.html' % template_prefix

    from_email = settings.EMAIL_HOST_USER
    subject = render_to_string(subject_file).strip()
    to = target_email
    text_content = render_to_string(txt_file, template_ctxt)
    html_content = render_to_string(html_file, template_ctxt)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


class AbstractBaseCode(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    code = models.CharField(_('code'), max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def send_email(self, prefix):
        
        ctxt = {
            'email': self.user.email,
            'fullname': self.user.fullname,
            'code': self.code,
            'base_url': settings.URL
        }
        send_multi_format_email(prefix, ctxt, target_email=self.user.email)

    def __str__(self):
        return self.code


class SignupCode(AbstractBaseCode):
    ipaddr = models.GenericIPAddressField(_('ip address'))

    objects = SignupCodeManager()

    def send_signup_email(self):
        prefix = 'signup_email'
        self.send_email(prefix)


class PasswordResetCodeManager(models.Manager):
    def create_password_reset_code(self, user):
        code = _generate_code()
        password_reset_code = self.create(user=user, code=code)

        return password_reset_code

    def get_expiry_period(self):
        return EXPIRY_PERIOD


class PasswordResetCode(AbstractBaseCode):
    objects = PasswordResetCodeManager()

    def send_password_reset_email(self):
        prefix = 'password_reset_email'
        self.send_email(prefix)
