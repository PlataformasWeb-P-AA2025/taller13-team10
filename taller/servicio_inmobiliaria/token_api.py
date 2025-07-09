from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

try:
    user_empresa = User.objects.get(username='admin')
    token, created = Token.objects.get_or_create(user=user_empresa)

    if created:
        print(f"Token generado para '{user_empresa.username}': {token.key}")
    else:
        print(f"Token existente para '{user_empresa.username}': {token.key}")

except User.DoesNotExist:
    print("El usuario 'empresa_api' no existe. Créalo primero.")

# edceb491e833d5c592639370aac69a3f899edd63