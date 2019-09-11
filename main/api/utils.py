
from django.db.models import Avg, Count, Min, Sum
from . import serializers, models
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from random import randrange


def create_account(answer, educational_f, login, password):
    mother = models.Parent.objects.create(
        name_f=answer.validated_data['parent_mother']['name_f'],
        name_l=answer.validated_data['parent_mother']['name_l'],
        patronymic=answer.validated_data['parent_mother']['patronymic'],
        phone=answer.validated_data['parent_mother']['phone']
    )
    father = models.Parent.objects.create(
        name_f=answer.validated_data['parent_father']['name_f'],
        name_l=answer.validated_data['parent_father']['name_l'],
        patronymic=answer.validated_data['parent_father']['patronymic'],
        phone=answer.validated_data['parent_father']['phone']
    )
    account = models.Account.objects.create(
        login=login,
        password=password,
        student_id=answer.validated_data['id'],
        name_f=answer.validated_data['name_f'],
        name_l=answer.validated_data['name_l'],
        patronymic=answer.validated_data['patronymic'],
        gender_id=answer.validated_data['gender_id'],
        educational_form=educational_f,
        citizenship=answer.validated_data['citizenship'],
        uin=answer.validated_data['uin'],
        address=answer.validated_data['address'],
        city=answer.validated_data['city'],
        country=answer.validated_data['country'],
        phone=answer.validated_data['phone'],
        email=answer.validated_data['email'],
        privileges=answer.validated_data['privileges'],
        group=answer.validated_data['group'],
        parent_mother=mother,
        parent_father=father,
        token=generate_token(40)
    )
    return serializers.AccountSerializer(account).data


def update_parent(answer, id, type_parent):
    try:
        parent = models.Parent.objects.get(pk=id)
        parent.name_f = answer.validated_data[type_parent]['name_f']
        parent.name_l = answer.validated_data[type_parent]['name_l']
        parent.patronymic = answer.validated_data[type_parent]['patronymic']
        parent.phone = answer.validated_data[type_parent]['phone']
        parent.save()
    except models.Parent.DoesNotExist:
        pass


def account_to_json(login, password):
    account = models.Account.objects.get(
        Q(login=login),
        Q(password=password)
    )
    return serializers.AccountSerializer(account).data


def update_account(answer, account, educational_f, login, password):
    if account.parent_mother_id:
        update_parent(answer, account.parent_mother_id, 'parent_mother')

    if account.parent_father_id:
        update_parent(answer, account.parent_father_id, 'parent_father')

    account.login = login
    account.password = password
    account.student_id = answer.validated_data['id']
    account.name_f = answer.validated_data['name_f']
    account.name_l = answer.validated_data['name_l']
    account.patronymic = answer.validated_data['patronymic']
    account.gender_id = answer.validated_data['gender_id']
    account.educational_form = educational_f
    account.citizenship = answer.validated_data['citizenship']
    account.uin = answer.validated_data['uin']
    account.address = answer.validated_data['address']
    account.city = answer.validated_data['city']
    account.country = answer.validated_data['country']
    account.phone = answer.validated_data['phone']
    account.email = answer.validated_data['email']
    account.privileges = answer.validated_data['privileges']
    account.group = answer.validated_data['group']
    account.token = generate_token(40)
    account.save()
    return account_to_json(login, password)


def handler_auth_account(request):
    body = serializers.AuthAccountSerializer(data=request.data)
    if body.is_valid():
        student = models.Account.objects.filter(
            login=body.validated_data['login'],
            password=body.validated_data['password']
        )
        
        if student.count() != 0:
            return Response(
                {
                    'id': student[0].id,
                    'name_f': student[0].name_f,
                    'name_l': student[0].name_l,
                    'patronymic': student[0].patronymic,
                    'group': student[0].group,
                }
            )
        else:
            return Response(status=status.HTTP_409_CONFLICT)


def get_sort_data(model, request):
    if request.headers.get('Educationalform') != None:
        data_list = model.filter(
            account__educational_form__id=request.headers.get('Educationalform'))
    elif request.headers.get('Gender') != None:
        data_list = model.filter(
            account__gender__id=request.headers.get('Gender'))
    elif request.headers.get('Children') != None:
        data_list = model.order_by('account__children').reverse()
    elif request.headers.get('Datecreate') != None:
        data_list = model.order_by('date_create').reverse()
    elif request.headers.get('Dateupdate') != None:
        data_list = model.order_by('date_update').reverse()
    elif request.headers.get('Active') != None:
        data_list = model.filter(active=request.headers.get('Active'))
    elif request.headers.get('All') != None:
        data_list = model.all()
    else:
        data_list = model.filter(active=0)
    return data_list


def get_db():
    dorm = serializers.DormSerializer(
        models.Dorm.objects.all(), many=True).data
    gender = serializers.GenderSerializer(
        models.Gender.objects.all(), many=True).data
    name = serializers.NameSerializer(
        models.Name.objects.all(), many=True).data
    floor = serializers.FloorSerializer(
        models.Floor.objects.all(), many=True).data
    return {
        'dorm': dorm,
        'gender': gender,
        'name': name,
        'floor': floor
    }


def get_statistic():
    accepted_requests = len(models.Request.objects.filter(active=1))
    curr_live = len(models.Report.objects.filter(status__active=1))
    return {
        'accepted_requests': accepted_requests,
        'curr_live': curr_live
    }


def get_rooms_floor(pk):
    room_list = []
    rooms = models.Room.objects.filter(floor=pk)

    for r in rooms:
        amount = len(models.Room.objects.filter(
            report__status__active=1, id=r.id))
        room_list.append({
            'id': r.id,
            'max': r.max,
            'number': r.number,
            'floor': r.floor_id,
            'symbol': r.symbol,
            'amount': amount
        })
    print(room_list)
    return room_list


def generate_token(amount):
    """Генерация нового токена."""
    token = ''
    digit = "0123456789"
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i in range(amount):
        index = randrange(3)

        if index == 0:
            token = token + digit[randrange(len(digit))]
        elif index == 1:
            token = token + lower[randrange(len(lower))]
        elif index == 2:
            token = token + upper[randrange(len(upper))]

    return token
