from django.contrib import admin
from .models import User, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'password',
        'phone_number',
        'birth_date',
        'created_at',
        'updated_at',
        'status',
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'city',
        'state',
        'country',
        'postcode',
        'complement',
        'house_number'
    )
