from django.utils import timezone
from datetime import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from django.contrib.auth.models import User, Group

class ViloyatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viloyat
        fields = '__all__'

class TumanSerializer(serializers.ModelSerializer):
    viloyat = ViloyatSerializer()  # Nested Viloyat
    class Meta:
        model = Tuman
        fields = '__all__'

class NhtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noqonuniy_holat_turi
        fields = '__all__'

class StansiyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stansiya
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class DalolatnomaRasmSerializer(serializers.ModelSerializer):
    class Meta:
        model = DalolatnomaRasm
        fields = ['rasm']  # Only the file field for upload

class DalolatnomaSerializer(serializers.ModelSerializer):
    tuman_detail = TumanSerializer(source='tuman', read_only=True)
    stansiya_detail = StansiyaSerializer(source='stansiya', read_only=True)
    noqonuniy_holat_turi_detail = NhtSerializer(source='noqonuniy_holat_turi', read_only=True)
    inspektor_detail = UserSerializer(source='inspektor', read_only=True)

    inspektor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False) 
    rasmlar = serializers.ListField(child=serializers.ImageField(), required=False)
    
    korsatma_raqam = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Dalolatnoma.objects.all())]
    )
    korsatma_sana = serializers.DateTimeField(default_timezone=None)

    boshqa_rasmlar = DalolatnomaRasmSerializer(source='dalolatnomarasm_set', many=True, read_only=True)

    class Meta:
        model = Dalolatnoma
        fields = '__all__'
    
    def to_internal_value(self, data):
        stansiya_prefix = self.context.get('stansiya_prefix', '')
        data = data.copy()
        
        if 'korsatma_raqam' in data and not data['korsatma_raqam'].startswith(stansiya_prefix):
            data['korsatma_raqam'] = f"{stansiya_prefix}-{data['korsatma_raqam']}"
        
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        print(validated_data)
        rasmlar_data = validated_data.pop('rasmlar', [])
        dalolatnoma = Dalolatnoma.objects.create(**validated_data)
        print("=======================================")
        print(rasmlar_data)
        print("=======================================")
        for rasm in rasmlar_data:
            DalolatnomaRasm.objects.create(dalolatnoma=dalolatnoma, rasm=rasm)
        
        return dalolatnoma

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop('tuman')
    #     representation.pop('stansiya')
    #     representation.pop('noqonuniy_holat_turi')
    #     representation.pop('inspektor')

    #     # representation['korsatma_sana'] = instance.korsatma_sana.isoformat()

    #     # if isinstance(instance.korsatma_sana, datetime):
    #     #     instance.korsatma_sana = instance.korsatma_sana.date()  # Extract the date part

    #     return representation