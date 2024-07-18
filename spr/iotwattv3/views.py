import boto3
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .utils import get_secret_hash

import os
from dotenv import load_dotenv
load_dotenv("../spr/.env")


AWS_REGION = os.getenv('AWS_REGION')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
client = boto3.client('cognito-idp', region_name=AWS_REGION,aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

#class SignInView(View): 
@csrf_exempt
def SignInView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            secret_hash = get_secret_hash(username, COGNITO_CLIENT_ID,COGNITO_CLIENT_SECRET)
            response = client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                    'SECRET_HASH': secret_hash
                }
            )
            return JsonResponse({'message': 'Success'}, status=200)
        except:
            return JsonResponse({'message': 'Failed'}, status=401)


        
    else:
        return JsonResponse({'message': 'Failed'}, status=405)
   