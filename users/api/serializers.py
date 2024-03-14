from rest_framework.serializers import ModelSerializer, ValidationError
from users.models import User, Address
from users.api.validators import *


class AddressSerializer(ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'city',
            'state',
            'country',
            'postcode',
            'complement',
            'house_number'
        )

    def to_representation(self, instance):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return super().to_representation(instance)
        else:
            data = super().to_representation(instance)
            data.pop('id_address', None)
            return data

    def get_or_create_address(self, validated_data):
        similar_addresses = Address.objects.filter(**validated_data)
        if similar_addresses.exists():
            return similar_addresses.first()
        else:
            return Address.objects.create(**validated_data)


class UserSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = (
            'id_slug',
            'username',
            'first_name',
            'last_name',
            'email',
            'ddi',
            'phone_number',
            'birth_date',
            'created_at',
            'updated_at',
            'status',
            'address',
        )

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address_serializer = AddressSerializer(data=address_data)

        if address_serializer.is_valid():
            address = address_serializer.get_or_create_address(address_data)
            user = User.objects.create(address=address, **validated_data)
            return user
        else:
            raise ValidationError(address_serializer.errors)

    def validate(self, data):

        if not UserValidator.validate_first_name(data['first_name']):
            raise ValidationError({'first_name': 'Invalid first name format'})

        if not UserValidator.validate_last_name(data['last_name']):
            raise ValidationError(
                {'last_name': 'Invalid last name format'})

        if not UserValidator.validate_phone_number(data['phone_number']):
            raise ValidationError(
                {'phone_number': 'Invalid phone number format'})

        return data

    def update(self, instance, validated_data):

        instance.username = validated_data.get(
            'username', instance.username
        )
        instance.first_name = validated_data.get(
            'first_name', instance.first_name
        )
        instance.email = validated_data.get(
            'email', instance.email
        )
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number
        )
        instance.birth_date = validated_data.get(
            'birth_date', instance.birth_date
        )
        instance.ddi = validated_data.get(
            'ddi', instance.ddi
        )

        address_data = validated_data.pop('address', None)

        if address_data:
            address_serializer = AddressSerializer(
                instance.address, data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()

        return instance
