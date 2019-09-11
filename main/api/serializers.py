from rest_framework import serializers
from . import models


class AuthAccountSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class ParseParentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name_f = serializers.CharField(max_length=100)
    name_l = serializers.CharField(max_length=100)
    patronymic = serializers.CharField(max_length=100, required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)


class ParseAccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name_f = serializers.CharField(max_length=100)
    name_l = serializers.CharField(max_length=100)
    patronymic = serializers.CharField(max_length=100, required=False, allow_null=True)
    group = serializers.CharField(max_length=10, required=False, allow_null=True)
    gender_id = serializers.IntegerField(required=False, allow_null=True)
    uin = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100, required=False, allow_null=True)
    city = serializers.CharField(max_length=100, required=False, allow_null=True)
    country = serializers.CharField(max_length=100, required=False, allow_null=True)
    citizenship = serializers.CharField(max_length=100, required=False, allow_null=True)
    parent_mother = ParseParentSerializer(required=False, allow_null=True)
    parent_father = ParseParentSerializer(required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    educational_form = serializers.IntegerField(required=False, allow_null=True)
    privileges = serializers.CharField(max_length=255, required=False, allow_null=True)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'
        depth = 2


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guardian
        fields = '__all__'


class OrphanageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Orphanage
        fields = '__all__'


class StudentSerializer:
    class Read(serializers.ModelSerializer):
        class Meta:
            model = models.Account
            fields = '__all__'
            depth = 2

    class All(serializers.ModelSerializer):
        class Meta:
            model = models.Account
            fields = '__all__'


class RequestSerializer:
    class Read(serializers.ModelSerializer):
        class Meta:
            model = models.Request
            fields = '__all__'
            depth = 3

    class All(serializers.ModelSerializer):
        class Meta:
            model = models.Request
            fields = '__all__'


class ReportSerializer:
    class Read(serializers.ModelSerializer):
        class Meta:
            model = models.Report
            fields = '__all__'
            depth = 3

    class All(serializers.ModelSerializer):
        class Meta:
            model = models.Report
            fields = '__all__'


class DormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dorm
        fields = '__all__'


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gender
        fields = '__all__'


class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Name
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = '__all__'


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Floor
        fields = '__all__'