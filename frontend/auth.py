from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt_token')
        if not token:
            return None
        try:
            validated_token = AccessToken(token)
            user_id = validated_token.payload.get('user_id')
            user = User.objects.get(id=user_id)
            return (user, validated_token)
        except Exception as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')