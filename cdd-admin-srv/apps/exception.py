from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import set_rollback

from apps.errors import ServerError


def exception_handler(exc, context):
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'message': exc.detail}

        if isinstance(exc, ServerError):
            if hasattr(exc, 'code'):
                data.update({'code': exc.code})

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        data = {'detail': six.text_type(msg)}

        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        data = {'detail': six.text_type(msg)}

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    return None
