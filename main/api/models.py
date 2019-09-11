from django.db import models


class Name(models.Model):
    """Названия.

    Описание полей:
    ru -- русский текст
    kz -- казахский текст
    en -- английский текст
    """
    ru = models.CharField(max_length=255, 
                          blank=True, 
                          null=True,
                          verbose_name='Текст на русском')
    kz = models.CharField(max_length=255, 
                          blank=True, 
                          null=True,
                          verbose_name='Текст на казахском')
    en = models.CharField(max_length=255, 
                          blank=True, 
                          null=True,
                          verbose_name='Текст на английском')
    
    class Meta:
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'
        
    def __str__(self):
        return self.ru


class Dorm(models.Model):
    """Общежития.

    Описание полей:
    name -- ссылка на текст
    """
    name = models.ForeignKey(Name, 
                             on_delete=models.CASCADE,
                             verbose_name='Название общежития')
    
    class Meta:
        verbose_name = 'Общежитие'
        verbose_name_plural = 'Общежития'
        
    def __str__(self):
        return self.name.ru


class Floor(models.Model):
    """Этажи общежития.

    Описание полей:
    number -- номер этажа 
    dorm -- ссылка на общежитие
    """
    number = models.PositiveIntegerField(verbose_name='Номер этажа')
    dorm = models.ForeignKey(Dorm, 
                             on_delete=models.CASCADE,
                             verbose_name='Общежитие')
    
    class Meta:
        verbose_name = 'Этаж общежития'
        verbose_name_plural = 'Этажи общежитий'
        
    def __str__(self):
        return f"[{self.number} этаж] {self.dorm.name.ru}"


class Room(models.Model):
    """Комнаты этажей.

    Описание полей:
    number -- номер комнаты
    max -- максимальное количество людей в комнате
    symbol -- символ комнаты
    floor -- ссылка на этаж комнаты
    """
    number = models.PositiveIntegerField(verbose_name='Номер комнаты')
    max = models.PositiveIntegerField(verbose_name='Макс. \
                                        количество людей в комнате')
    symbol = models.CharField(max_length=255, 
                              blank=True, 
                              null=True,
                              verbose_name='Символ комнаты')
    floor = models.ForeignKey(Floor, 
                              on_delete=models.CASCADE,
                              verbose_name='Этаж комнаты')
    
    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
        
    def __str__(self):
        return f'{self.floor.number} этаж, max({self.max}), \
             {self.number}{self.symbol if self.symbol != None else ""}'


class Gender(models.Model):
    """Человеческий пол.
    
    Описание полей:
    name -- ссылка на текст
    """
    name = models.ForeignKey(Name, 
                             on_delete=models.CASCADE,
                             verbose_name='Название чел. пола')
    
    class Meta:
        verbose_name = 'Человеческий пол'
        verbose_name_plural = 'Человеческие пола'
        
    def __str__(self):
        return self.name.ru


class Status(models.Model):
    """Статусы отчётов.

    Описание полей:
    name -- ссылка на текст
    active -- слушатель на чтение отчёта
    """
    name = models.ForeignKey(Name, 
                             on_delete=models.CASCADE,
                             verbose_name='Название статуса')
    active = models.IntegerField(verbose_name='Значение статуса')
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        
    def __str__(self):
        return f"{self.name.ru} [active={self.active}]"


class Orphanage(models.Model):
    """Приюты.

    Описание полей:
    title -- название приюта
    address -- адрес
    phone -- телефонный номер
    """
    title = models.CharField(max_length=255,
                             verbose_name='Название приюта')
    address = models.CharField(max_length=140,
                               verbose_name='Адрес')
    phone = models.CharField(max_length=20,
                             verbose_name='Телефонный номер')
    
    class Meta:
        verbose_name = 'Приют'
        verbose_name_plural = 'Приюты'
        
    def __str__(self):
        return f"{self.title} - {self.address} ({self.phone})"


class Guardian(models.Model):
    """Опекуны.

    Описание полей:
    name_f -- имя
    name_l -- фамилия
    patronymic -- отчество
    phone -- телефонный номер
    """
    name_f = models.CharField(max_length=100,
                              verbose_name='Имя')
    name_l = models.CharField(max_length=100,
                              verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, 
                                  blank=True, 
                                  null=True,
                                  verbose_name='Отчество')
    phone = models.CharField(max_length=20,
                             verbose_name='Телефонный номер')
    
    class Meta:
        verbose_name = 'Опекун'
        verbose_name_plural = 'Опекуны'
        
    def __str__(self):
        return f"{self.name_l} {str(self.name_f)[0]}.\
            {str(self.patronymic)[0]+'.' if self.patronymic != None else ''} \
                ({self.phone})"


class Parent(models.Model):
    """Родители (мама или папа).

    Описание полей:
    name_f -- имя
    name_l -- фамилия
    patronymic -- отчество
    phone -- телефонный номер
    """
    name_f = models.CharField(max_length=100,
                              verbose_name='Имя')
    name_l = models.CharField(max_length=100,
                              verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, 
                                  blank=True, 
                                  null=True,
                                  verbose_name='Отчество')
    phone = models.CharField(max_length=20,
                             blank=True,
                             null=True,
                             verbose_name='Телефонный номер')
    
    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'
        
    def __str__(self):
        return f"{self.name_l} {str(self.name_f)[0]}.\
            {str(self.patronymic)[0]+'.' if self.patronymic != None else ''} \
                ({self.phone})"


class EducationalForm(models.Model):
    """Формы обучения.

    Описание полей:
    name -- ссылка на текст
    """
    name = models.CharField(max_length=100,
                            verbose_name='Название формы обучения')
    
    class Meta:
        verbose_name = 'Форма обучения'
        verbose_name_plural = 'Формы обучения'
        
    def __str__(self):
        return self.name


class Account(models.Model):
    """Аккаунты.

    Описание полей:
    name_f -- имя
    name_l -- фамилия
    patronymic -- отчество
    group -- группа
    gender -- ссылка на человеческий пол
    educational_form -- ссылка на форму обучения
    parent_mother -- ссылка на родителя (мама)
    parent_father -- ссылка на родителя (папа)
    orphanage -- ссылка на приют
    guardian -- ссылка на опекуна
    children -- количество детей в семье
    student_id -- ID студента в основной базе КЭУК
    citizenship -- гражданство
    uin -- ИИН или номер паспорта
    address -- адрес проживания
    city -- город
    country -- страна
    phone -- телефонный номер
    email -- электронная почта
    privileges -- льготы
    token -- ключ безопасности
    """
    login = models.CharField(max_length=255,
                              verbose_name='Логин')
    password = models.CharField(max_length=255,
                              verbose_name='Пароль')
    name_f = models.CharField(max_length=100,
                              verbose_name='Имя')
    name_l = models.CharField(max_length=100,
                              verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, 
                                  blank=True, 
                                  null=True,
                                  verbose_name='Отчество')
    group = models.CharField(max_length=10, 
                             blank=True, 
                             null=True,
                             verbose_name='Группа')
    gender = models.ForeignKey(Gender, 
                               on_delete=models.CASCADE, 
                               blank=True, 
                               null=True,
                               verbose_name='Человеческий пол')
    educational_form = models.ForeignKey(EducationalForm, 
                                         on_delete=models.CASCADE, 
                                         blank=True, 
                                         null=True,
                                         verbose_name='Форма обучения')
    parent_mother = models.ForeignKey(Parent, 
                                      on_delete=models.CASCADE, 
                                      blank=True, 
                                      null=True, 
                                      related_name='parent_mother',
                                      verbose_name='Мама')
    parent_father = models.ForeignKey(Parent, 
                                      on_delete=models.CASCADE, 
                                      blank=True, 
                                      null=True, 
                                      related_name='parent_father',
                                      verbose_name='Папа')
    orphanage = models.ForeignKey(Orphanage, 
                                  on_delete=models.CASCADE, 
                                  blank=True, 
                                  null=True,
                                  verbose_name='Приют')
    guardian = models.ForeignKey(Guardian, 
                                 on_delete=models.CASCADE, 
                                 blank=True, 
                                 null=True,
                                 verbose_name='Опекун')
    children = models.PositiveSmallIntegerField(blank=True, 
                                                null=True,
                                                verbose_name='Количество детей \
                                                     в семье')
    student_id = models.IntegerField(verbose_name='ID студента')
    citizenship = models.CharField(max_length=100, 
                                   blank=True, 
                                   null=True,
                                   verbose_name='Гражданство')
    uin = models.CharField(max_length=100,
                           verbose_name='ИИН или номер паспорта')
    address = models.CharField(max_length=100, 
                               blank=True, 
                               null=True,
                               verbose_name='Адрес')
    city = models.CharField(max_length=100, 
                            blank=True, 
                            null=True,
                            verbose_name='Город')
    country = models.CharField(max_length=100, 
                               blank=True, 
                               null=True,
                               verbose_name='Страна')
    phone = models.CharField(max_length=20, 
                             blank=True, 
                             null=True,
                             verbose_name='Телефонный номер')
    email = models.EmailField(blank=True, 
                              null=True,
                              verbose_name='Электронная почта')
    privileges = models.CharField(max_length=255, 
                                  blank=True, 
                                  null=True,
                                  verbose_name='Льготы')
    token = models.CharField(max_length=40,
                             verbose_name='Ключ')
    
    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'аккаунты'
        
    def __str__(self):
        return f"{self.name_l} {str(self.name_f)[0]}. \
            {str(self.patronymic)[0]+'.' if self.patronymic != None else ''} \
                ({self.phone})"


class Report(models.Model):
    """Отчёты.

    Описание полей:
    account -- ссылка на аккаунт
    room -- ссылка на комнату общежития
    status -- ссылка на статус отчёта
    active -- состояние где: 1-завершен, 0-активен
    date_create -- дата и время создания отчёта
    date_update -- дата и время обновления отчёта
    date_residence -- дата заселения
    """
    account = models.ForeignKey(Account, 
                                on_delete=models.CASCADE,
                                verbose_name='Аккаунт')
    room = models.ForeignKey(Room, 
                             on_delete=models.CASCADE,
                             verbose_name='Комната')
    status = models.ForeignKey(Status, 
                               on_delete=models.CASCADE,
                               verbose_name='Статус отчёта')
    active = models.PositiveIntegerField(verbose_name='Слушатель активности')
    date_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата изменения')
    date_residence = models.DateField(verbose_name='Дата заселения')
    
    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
        
    def __str__(self):
        return f"{self.account.name_l} {str(self.account.name_f)[0]}. \
            {str(self.account.patronymic)[0]+'.' if self.account.patronymic != None else ''} \
                [Комната {self.room.number}{self.room.symbol if self.room.symbol != None else ''}]"


class Request(models.Model):
    """Заявления.

    Описание полей:
    account -- ссылка на аккаунт
    room -- ссылка на комнату общежития
    active -- слушатель на чтение заявления
    date_create -- дата и время создания отчёта
    date_update -- дата и время обновления отчёта
    date_residence -- дата заселения
    """
    account = models.ForeignKey(Account, 
                                on_delete=models.CASCADE,
                                verbose_name='аккаунт')
    room = models.ForeignKey(Room, 
                             on_delete=models.CASCADE,
                             verbose_name='Комната')
    active = models.IntegerField(verbose_name='Слушатель активности')
    date_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата изменения')
    date_residence = models.DateField(verbose_name='Дата заселения')
    
    class Meta:
        verbose_name = 'Заявление'
        verbose_name_plural = 'Заявления'
        
    def __str__(self):
        return f"{self.account.name_l} {str(self.account.name_f)[0]}. \
        {str(self.account.patronymic)[0]+'.' if self.account.patronymic != None else ''} \
            {self.room.number}{self.room.symbol}"