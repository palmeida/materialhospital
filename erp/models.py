from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField


class Process(models.Model):
    code = models.IntegerField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)


class Request(models.Model):
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL)
    health_unit = models.ForeignKey('HealthUnit', null=True, blank=True,
                                    on_delete=models.SET_NULL)
    health_professional = models.ForeignKey('HealthProfessional', null=True,
                                            blank=True,
                                            on_delete=models.SET_NULL)
    equipment = models.ForeignKey('Equipment', on_delete=models.PROTECT)
    quantity = models.IntegerField(null=True, blank=True)
    maximum_available = models.BooleanField()

    def __str__(self):
        return '{} / {}'.format(self.process, self.equipment.name)


class HealthUnit(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HealthProfessional(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=200)

    PRODUCT_TYPE_CHOICES = (
        ('E', 'Equipamento Protecao Individual'),
        ('V', 'Ventilador'),
        ('T', 'Kit Teste'),
        ('O', 'Outro'),
    )

    product_type = models.CharField(max_length=1, choices=PRODUCT_TYPE_CHOICES)
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True,
                                     on_delete=models.PROTECT)
    model = models.CharField(max_length=100)
    manufacturer_reference = models.CharField(max_length=100)

    def __str__(self):
        return '{} / {}'.format(self.name, self.get_product_type_display())


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Procurement(models.Model):
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    PROCUREMENT_TYPE_CHOICES = (
        ('D', 'Donation'),
        ('C', 'Commercial'),
    )
    procurement_type = models.CharField(max_length=1,
                                        choices=PROCUREMENT_TYPE_CHOICES)
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL)
    equipment = models.ForeignKey('Equipment', on_delete=models.PROTECT)
    supplier = models.ForeignKey('Supplier', null=True, blank=True,
                                 on_delete=models.PROTECT)
    availability = models.CharField(max_length=100, null=True, blank=True)
    min_order_quantity = models.IntegerField(null=True, blank=True)
    picture = models.ImageField(upload_to='images')
    price_per_unit = models.IntegerField(null=True, blank=True)
    price_total = models.IntegerField(null=True, blank=True)

    CURRENCY_CHOICES = (
        ('D', 'dollar'),
        ('E', 'euro'),
    )
    currency = models.CharField(max_length=1, choices=CURRENCY_CHOICES,
                                null=True, blank=True)
    payment_terms = models.CharField(max_length=200, null=True, blank=True)
    delivery_time = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    ce_certified = models.NullBooleanField()
    fda_certified = models.NullBooleanField()

    def __str__(self):
        return '{} / {} / {}'.format(self.process, self.equipment.name,
                                     self.supplier)


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    lead = models.CharField(max_length=32, blank=True, null=True)
    origin = CountryField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProcurementDocument(models.Model):
    procurement = models.ForeignKey('Procurement', on_delete=models.CASCADE)
    file_type = models.ForeignKey('DocumentType', null=True, blank=True,
                                  on_delete=models.PROTECT)
    file = models.FileField(upload_to='files')

    def __str__(self):
        return '{} / {}'.format(self.procurement, self.file_type)


class DocumentType(models.Model):
    file_type = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.file_type


class PurchaseValidation(models.Model):
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL)
    health_professional = models.ForeignKey('HealthProfessional', null=True,
                                            blank=True,
                                            on_delete=models.SET_NULL)


class PurchaseOrder(models.Model):
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL)
    code = models.CharField(max_length=30, null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=30, blank=True, null=True)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} / {}'.format(self.process, self.code)


class Stock(models.Model):
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL)
    loading_point = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    warehouse = models.ForeignKey('Warehouse', null=True, blank=True,
                                  on_delete=models.PROTECT)

    def __str__(self):
        return str(self.process)


class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Distribution(models.Model):
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    distributor = models.ForeignKey('Distributor', null=True, blank=True,
                                    on_delete=models.PROTECT)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.process)


class Distributor(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=300)

    def __str__(self):
        return self.name
