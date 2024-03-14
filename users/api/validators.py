import re


class UserValidator():

    def validate_first_name(first_name):
        return first_name.isalpha()

    def validate_last_name(last_name):
        return last_name.isascii()

    def validate_phone_number(phone_number):
        phone_number_model = '[0-9]{2} [0-9]{5}-[0-9]{4}'
        answer = re.findall(phone_number_model, phone_number)
        return answer


# class AddressValidator():
