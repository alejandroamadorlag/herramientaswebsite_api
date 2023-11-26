from rest_framework import serializers
from rest_framework.authtoken.models import Token
from herramientaswebsite_api.models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class ProfilesSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Profiles
        fields = "__all__"
class ProfilesAllSerializer(serializers.ModelSerializer):
    #user=UserSerializer(read_only=True)
    class Meta:
        model = Profiles
        fields = '__all__'
        depth = 1


#MATERIAS
class MateriaSerializer(serializers.ModelSerializer):
    nrc = serializers.IntegerField(read_only=True)
    materia = serializers.CharField(required=True)
    seccion = serializers.CharField(required=True)

    class Meta:
        model = Materias
        fields = ('nrc','materia','seccion')

class MateriasSerializer(serializers.ModelSerializer):
    user=MateriaSerializer(read_only=True)
    class Meta:
        model = Materias
        fields = "__all__"
class MateriasAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materias
        fields = '__all__'
        depth = 1