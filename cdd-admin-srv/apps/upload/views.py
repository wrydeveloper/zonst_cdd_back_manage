import uuid
import imghdr

from django.conf import settings

from rest_framework.views import APIView, status
from rest_framework.response import Response

from apps.permissions import AdminPermission


class UploadView(APIView):
    permission_classes = (AdminPermission,)

    def post(self, request):
        file_obj = request.FILES['file']
        type = request.data.get('type')

        if type == 'image':
            extension = imghdr.what(request.FILES['file'])
            if extension is None:
                return Response({'message': '非法文件！'}, status=status.HTTP_400_BAD_REQUEST)
            
            filename = '{filename}.{extension}'.format(filename=uuid.uuid1(), extension=extension)
            path = ''.join([settings.IMG_PATH, filename])
        else:
            filename = request.FILES['file'].name
            path = ''.join([settings.APK_PATH, filename])

        with open(path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        if type == 'banner':
            url = ''.join([settings.IMG_URL, filename])
        else:
            url = ''.join([settings.APK_URL, filename])

        data = {
            'url': url
        }

        return Response({'data': data})
