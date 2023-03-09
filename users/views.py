from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User
from .errors import EmailNotFound
import requests

serverDomain = "http://localhost:8000"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def getJwtResponse(serverUrl, email, password):
    return requests.post(url=serverUrl, data={'email': email, 'password': password})



# Views below.
def testConnection(request):
    return HttpResponse("Sever is live on PORT: 8000")


def signIn(request):
    print("request: ", request)

    if request.GET and (request.GET.get('email') and request.GET.get('password')):
        email = request.GET.get('email')
        user = authenticate(request, email=email,
                            password=request.GET.get('password'))

        if user is not None:
            targetUser = User.objects.get(email=email)
            serverUrl = "{serverDomain}/users/get-token".format(
                serverDomain=serverDomain)
            jwtResponse = requests.post(url=serverUrl, data={'email': email, 'password': request.GET.get('password')})

            print("jwtResponse: ", jwtResponse)

            # return HttpResponse("Testing")

            user = {"token": jwtResponse.json(), 'firstName': targetUser.first_name,
                    'lastName': targetUser.last_name}

            return JsonResponse({"msg": "Sign-in was successful.", 'user': user})
        else:
            print("Invalid username or password.")

            return HttpResponse("Invalid username or password.", status=404)

    return HttpResponse("Invalid parameters.", status=404)


@csrf_exempt
def createUser(request):
    print("request: ", request)

    if request.POST and (request.POST.get('name') == 'createUser' and request.POST.get('email')):
        print("creating user")
        email = request.POST.get('email')

        if len(User.objects.filter(email=email)) == 1:
            print("The email was taken already.")
            return HttpResponse("There is an account with that email already.", status=409)

        password = request.POST.get('password')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        birthDate = request.POST.get('birthDate')
        fromCity = request.POST.get('fromCity')
        fromCountry = request.POST.get('fromCountry')
        sex = request.POST.get('sex')
        phoneNum = request.POST.get('phoneNum')
        isAllUserInfoPresent = (email and password and firstName and lastName and birthDate and phoneNum and fromCity and fromCountry and sex)

        if isAllUserInfoPresent:
            try:
                User.objects.create_user(email=email, date_of_birth=birthDate, password=password)
                newUser = User.objects.get(email=email)
                newUser.first_name = firstName
                newUser.last_name = lastName
                newUser.phone_num = phoneNum
                newUser.from_city = fromCity
                newUser.from_country = fromCountry
                newUser.sex = sex
                newUser.save()
                serverUrl = "{serverDomain}/users/get-token".format(
                    serverDomain=serverDomain)
                jwtResponse = getJwtResponse(serverUrl, email, password)

                return JsonResponse({"msg": "User was successfully created.", "jwtToken": jwtResponse.json()})
            except Exception as error:
                print(
                    "An error occurred while saving the user into the database: ", error)
                return HttpResponse("User info may not have been saved. Have client refresh the page.", status=404)
        else:
            return HttpResponse("Did not receive an email, password, first name, or a last name.", status=404)

    return HttpResponse("Request does not have a name.")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAccountInfo(request):
    print("request, getting user account info: ", request)

    return HttpResponse("User info attained.", status=200)
