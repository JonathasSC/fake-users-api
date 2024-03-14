from django.db import models

# Create your models here.
from django.db.models import *
from uuid import uuid4
from django.utils.text import slugify
from users.utils.ddi import get_ddi


class Address(Model):
    id_address = UUIDField(primary_key=True, default=uuid4, editable=False)

    city = CharField(max_length=50)
    state = CharField(max_length=2)
    country = CharField(max_length=3)
    postcode = CharField(max_length=50)

    complement = CharField(blank=True, max_length=50)
    house_number = CharField(blank=True, max_length=6)

    class Meta:
        ordering = ['id_address']

        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class User(Model):
    id_user = UUIDField(primary_key=True, default=uuid4, editable=False)
    id_slug = SlugField(unique=True, editable=False, blank=True)

    username = CharField(max_length=50)

    first_name = CharField(max_length=50)
    last_name = CharField(max_length=100)

    email = EmailField(unique=True)
    password = CharField(max_length=255)

    ddi = CharField(max_length=5, choices=get_ddi, blank=True)
    phone_number = CharField(max_length=13, blank=True)
    birth_date = DateField()

    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)
    status = BooleanField(default=True)

    address = ForeignKey(
        Address,
        blank=False,
        related_name='users',
        on_delete=CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.id_slug:
            self.id_slug = slugify(str(self.id_user)[:10])
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['id_user']

        verbose_name = 'User'
        verbose_name_plural = 'Users'
