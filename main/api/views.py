from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status, generics
from . import serializers, models, utils, constructor_docx, permissions, email
from django.db.models import Q
from django.http import FileResponse
import os


@api_view(['POST'])
@permission_classes((AllowAny,))
def auth_account(request):
    return utils.handler_auth_account(request)


class GuardianAPIView(generics.ListCreateAPIView):
    """ Добавление и прочтение времени """
    queryset = models.Guardian.objects.all()
    serializer_class = serializers.GuardianSerializer
    permission_classes = (permissions.IsAuthenticatedOrAuthAccountWrite,)


class OrphanageAPIView(generics.ListCreateAPIView):
    """ Добавление и прочтение времени """
    queryset = models.Orphanage.objects.all()
    serializer_class = serializers.OrphanageSerializer
    permission_classes = (permissions.IsAuthenticatedOrAuthAccountWrite,)

class ReportsViewAPI(generics.ListCreateAPIView):
    """Класс позволяет создавать и получать экземпляры отчёты."""
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        self.serializer_class = serializers.ReportSerializer.Read
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = serializers.ReportSerializer.All
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return models.Report.objects.filter(active=0)


class RequestsViewAPI(generics.ListCreateAPIView):
    """Класс позволяет создавать и получать экземпляры заявления."""
    permission_classes = (permissions.IsAuthenticatedOrAuthAccountWrite,)

    def get(self, request, *args, **kwargs):
        self.serializer_class = serializers.RequestSerializer.Read
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = serializers.RequestSerializer.All
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return models.Request.objects.filter(active=0)


class AccountStudentViewAPI(generics.RetrieveUpdateAPIView):
    """Класс позволяет создавать и получать экземпляры заявления."""
    queryset = models.Account.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrAuthAccountUpdate,)

    def get(self, request, *args, **kwargs):
        self.serializer_class = serializers.StudentSerializer.Read
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.serializer_class = serializers.StudentSerializer.All
        
        instance = self.get_object()
        instance.orphanage = request.data.get("orphanage") if request.data.get("orphanage") != None else instance.orphanage
        instance.guardian = request.data.get("guardian") if request.data.get("guardian") != None else instance.guardian
        instance.children = request.data.get("children") if request.data.get("children") != None else instance.children
        instance.save()

        return Response(serializers.AccountSerializer(instance).data)


class ReportViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """Класс позволяет удалять, изменять и получать экземпляр отчёта."""
    queryset = models.Report.objects.all()
    serializer_class = serializers.ReportSerializer.All
    permission_classes = (IsAdminUser,)


class RequestViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """Класс позволяет удалять, изменять и получать экземпляр заявления."""
    queryset = models.Request.objects.all()
    serializer_class = serializers.RequestSerializer.All
    permission_classes = (IsAdminUser,)

    def perform_update(self, serializer):
        instance = serializer.save()

        if self.request.data['active'] == 1:
            email.send_request_success(instance.email)


class ReportsSortViewAPI(generics.ListAPIView):
    """Класс сортирует отчёты."""
    serializer_class = serializers.ReportSerializer.Read
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        self.queryset = utils.get_sort_data(models.Report.objects, request)
        return self.list(request, *args, **kwargs)


class RequestsSortViewAPI(generics.ListAPIView):
    """Класс сортирует заявления."""
    serializer_class = serializers.RequestSerializer.Read
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        self.queryset = utils.get_sort_data(models.Request.objects, request)
        return self.list(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes((AllowAny,))
def db_base(request):
    return Response(utils.get_db())


@api_view(['GET'])
@permission_classes((AllowAny,))
def statistic(request):
    return Response(utils.get_statistic())


@api_view(['GET'])
@permission_classes((AllowAny,))
def rooms_floor(request, pk):
    return Response(utils.get_rooms_floor(pk))


def send_direction_file(response, pk):
    """Отправить файл направление."""
    try:
        direction = models.Report.objects.get(pk=pk)
        name_file = constructor_docx.direction(
            name_f=direction.account.name_f, 
            name_l=direction.account.name_l, 
            dorm=direction.room.floor.dorm.id, 
            address=direction.account.address, 
            phone=direction.account.phone, 
            patronymic=direction.account.patronymic
        )

        response = FileResponse(open(name_file, 'rb'))
        os.remove(name_file)

        return response
    except models.Report.DoesNotExist:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_request_file(response, pk):
    """Отправить файл заявление."""
    try:
        request = models.Request.objects.get(pk=pk)
        name_file = constructor_docx.request(
            dorm=request.room.floor.dorm.id, 
            date=request.date_update, 
            number_request=request.id, 
            gender=request.account.gender.id, 
            address=request.account.address, 
            name_f=request.account.name_f, 
            name_l=request.account.name_l, 
            phone=request.account.phone, 
            group=request.account.group, 
            children=request.account.children, 
            patronymic=request.account.patronymic
        )

        response = FileResponse(open(name_file, 'rb'))
        os.remove(name_file)

        return response
    except models.Request.DoesNotExist:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)