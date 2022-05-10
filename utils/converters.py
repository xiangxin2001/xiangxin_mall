from django.urls import converters

class UsernameConverter:
    regex="[a-zA-Z0-9_-]{5,20}"

    def to_python(self,value):
        return value

class MobileConverter:
    regex='1[345789]\d{9}'

    def to_python(self,value):
        return value
    