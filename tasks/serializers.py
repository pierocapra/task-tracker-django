from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank.")
        return value.strip()

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)  # username column caps at 150
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email already in use.")
        return email

    def create(self, validated_data):
        email = validated_data["email"]
        return User.objects.create_user(
            username=email, email=email, password=validated_data["password"]
        )


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)
        self.fields["email"] = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(email__iexact=attrs["email"].strip()).first()
        if user is None or not user.is_active or not user.check_password(attrs["password"]):
            raise AuthenticationFailed("Invalid email or password.")
        refresh = self.get_token(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}