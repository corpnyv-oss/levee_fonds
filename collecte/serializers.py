from rest_framework import serializers
from .models import Cagnotte, Participation, Transaction, WebhookEvent, Actualite, Utilisateur

class CagnotteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cagnotte
        fields = '__all__'

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'
        read_only_fields = ('utilisateur', 'date_participation',)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('provider_ref', 'horodatage',)

class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = '__all__'
        read_only_fields = ('ip_source', 'horodatage',)

class ActualiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actualite
        fields = '__all__'

class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Utilisateur
        exclude = ['user_permissions', 'groups']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Utilisateur(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UtilisateurRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        # create inactive user until email confirmation
        user = Utilisateur(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()
        return user