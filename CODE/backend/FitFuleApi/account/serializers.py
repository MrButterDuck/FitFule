from .models import CustomUser
from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'age', 'height', 'weight', 'favorites',
            'allergy', 'goal', 'activity_level'
        )
