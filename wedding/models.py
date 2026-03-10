from django.db import models
import uuid
from django.utils import timezone
created_at = models.DateTimeField(default=timezone.now)
# =========================
# CONVIDADOS
# =========================

class Guest(models.Model):

    GUEST_TYPE_CHOICES = [
        ('amigo', 'Amigo'),
        ('familia', 'Família'),
        ('crianca', 'Criança'),
        ('agregado', 'Agregado'),
    ]

    SIDE_CHOICES = [
        ('noivo', 'Noivo'),
        ('noiva', 'Noiva'),
    ]

    name = models.CharField(max_length=100)
    guest_type = models.CharField(max_length=10, choices=GUEST_TYPE_CHOICES, default='amigo')
    invited_by = models.CharField(max_length=10, choices=SIDE_CHOICES, default='noivo')
    confirmed = models.BooleanField(default=False)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    rsvp_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # relacionamento de agregado
    main_guest = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='companions'
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(models.Model):

    PAYMENT_STATUS = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
    ]

    name = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default='pendente'
    )

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - R$ {self.value}"


# =========================
# CATEGORIAS FINANCEIRAS
# =========================

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# DESPESAS
# =========================

class Expense(models.Model):

    PAYMENT_STATUS = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
    ]

    name = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default='pendente'
    )

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - R$ {self.value}"