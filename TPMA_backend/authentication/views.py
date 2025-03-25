# authentication/views.py

import jwt
from academy.views import SupervisorEnrollmentAPIView
from administrator.models import Administrator
from administrator.serializers import AdministratorSerializer
from authentication.models import User
from authentication.permissions import IsAdministrator
from authentication.serializers import UserSerializer
from authentication.utils import TokenDecoderToGetUserId
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from email_handler.views import EmailVerificationDirectView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
# from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from staff.models import Staff
from staff.serializers import StaffSerializer
from supervisor.models import Supervisor
from supervisor.serializers import SupervisorSerializer
from trainee.models import Trainee
from trainee.serializers import TraineeSerializer


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer







class LogoutView(GenericAPIView, CreateModelMixin):
    # Sign out or Logout control
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # return Response({'message': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class UserDeleteView(DestroyModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserPartialUpdateView(UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):
        try:
            partial_update_response = self.partial_update(request, *args, **kwargs)

            # Send verification email if email was updated
            if 'email' in request.data:
                user = self.get_object()  # Get the updated user object
                email_verification_view = EmailVerificationDirectView()
                email_verification_response = email_verification_view.send(user)
                
            return partial_update_response

        except Exception as e:
            # Handle generic exceptions
            # You can log the exception or return an appropriate error response with a message and status code
            return Response({'message': 'An error occurred while updating. Please try again.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckPasswordView(APIView):
    # Check password authentication
    def post(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)

        user_auth = authenticate(
            request, username=user.username, password=password)
        if user_auth is not None:
            return Response({'message': 'Password authenticated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    # Change password without old password
    def post(self, request):
        user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class ChangePasswordUserView(APIView):
    permission_classes = [IsAuthenticated]
    # Change password
    def post(self, request):
        user_id = request.data.get('user_id')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)

        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        try:
            user = User.objects.get(username=username.strip())
        except User.DoesNotExist:
            return Response({'message': 'Invalid username'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class DeactivateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        authorization_header = request.headers.get('Authorization')
        
        # Decode the access token to retrieve the user ID
        user_id = TokenDecoderToGetUserId.decode_token(authorization_header)

        # Deactivate the user based on the retrieved user ID
        try:
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'User deactivated successfully'}, status=status.HTTP_200_OK)


class GetUserByUsernameView(APIView):
    permission_classes = [IsAdministrator]
    
    def get(self, request, *args, **kwargs):
        try:
            _username = request.GET.get('username')
            if _username is not None and isinstance(_username, str):
                _username = _username.lower()
            else:
                return Response({"success": False, "message": "Invalid username"}, status=status.HTTP_404_NOT_FOUND)

            try:
                user = User.objects.get(username=_username)
            except User.DoesNotExist:
                return Response({"success": False, "message": "User not found. Is the username correct?"}, status=status.HTTP_404_NOT_FOUND)

            user_data = {
                'user': UserSerializer(user).data
            }

            try:
                if user.role == 'administrator':
                    administrator = Administrator.objects.filter(user=user).first()
                    if administrator is not None:
                        # Add administrator data to the user_data
                        user_data['profile'] = AdministratorSerializer(administrator).data

                if user.role == 'staff':
                    staff = Staff.objects.filter(user=user).first()
                    if staff is not None:
                        # Add staff data to the user_data
                        staff_data = StaffSerializer(staff).data
                        
                        # Add permission groups data
                        permission_groups = staff.permission_groups.all()
                        group_data = [
                            {
                                'id': group.id,
                                'name': group.name,
                                'permissions': [
                                    {
                                        'id': permission.id,
                                        'codename': permission.codename,
                                        'name': permission.name
                                    }
                                    for permission in group.permissions.all()
                                ]
                            }
                            for group in permission_groups
                        ]                        
                        staff_data['permission_groups'] = group_data
                        
                        # Add permission groups data
                        permissions = staff.permissions.all()
                        permission_data = [
                            {
                                'id': permission.id,
                                'codename': permission.codename,
                                'name': permission.name
                            }
                            for permission in permissions
                        ]
                        staff_data['permissions'] = permission_data
                        
                        user_data['profile'] = staff_data

                elif user.role == 'supervisor':
                    supervisor = Supervisor.objects.filter(user=user).first()
                    if supervisor is not None:
                        # Add supervisor data to the user_data
                        user_data['profile'] = SupervisorSerializer(supervisor).data

                elif user.role == 'trainee':
                    trainee = Trainee.objects.filter(user=user).first()
                    if trainee is not None:
                        # Add trainee data to the user_data
                        user_data['profile'] = TraineeSerializer(trainee).data

            except Exception as e:
                return Response({"success": False, "message": "Cannot get the user 'profile' data", 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(user_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"success": False, "message": "Cannot get the user data", 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class LoginView(APIView):
#     # Sign in or Login control
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         user = authenticate(request, username=username.strip(), password=password.strip())
#         if user is not None:
#             # user.email_verified=True
#             # if user.email_verified:
#             login(request, user)
#             refresh = RefreshToken.for_user(user)

#             user_data = {
#                 'message': 'Login successful',
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': UserSerializer(user).data
#             }

#             if user.role == 'administrator':
#                 administrator = Administrator.objects.filter(user=user).first()
#                 if administrator is not None:
#                     # Add administrator data to the user_data
#                     user_data['profile'] = AdministratorSerializer(administrator).data

#             if user.role == 'staff':
#                 staff = Staff.objects.filter(user=user).first()
#                 if staff is not None:
#                     # Add staff data to the user_data
#                     staff_data = StaffSerializer(staff).data
                    
#                     # Add permission groups data
#                     permission_groups = staff.permission_groups.all()
#                     group_data = [
#                         {
#                             'id': group.id,
#                             'name': group.name,
#                             'permissions': [
#                                 {
#                                     'id': permission.id,
#                                     'codename': permission.codename,
#                                     'name': permission.name
#                                 }
#                                 for permission in group.permissions.all()
#                             ]
#                         }
#                         for group in permission_groups
#                     ]                        
#                     staff_data['permission_groups'] = group_data
                    
#                     # Add permissions data
#                     permissions = staff.permissions.all()
#                     permission_data = [
#                         {
#                             'id': permission.id,
#                             'codename': permission.codename,
#                             'name': permission.name
#                         }
#                         for permission in permissions
#                     ]
#                     staff_data['permissions'] = permission_data
                    
#                     user_data['profile'] = staff_data

#             elif user.role == 'supervisor':
#                 supervisor = Supervisor.objects.filter(user=user).first()
#                 if supervisor is not None:
#                     # Add supervisor data to the user_data
#                     user_data['profile'] = SupervisorSerializer(supervisor).data
#                     try:
#                         supervisor_id = int(supervisor.id)
#                         user_data['enrollment'] = SupervisorEnrollmentAPIView().enrollment(supervisor_id)
#                     except Exception as e:
#                         user_data['enrollment'] = None

#             elif user.role == 'trainee':
#                 trainee = Trainee.objects.filter(user=user).first()
#                 if trainee is not None:
#                     # Add trainee data to the user_data
#                     user_data['profile'] = TraineeSerializer(trainee).data

#             return Response(user_data, status=status.HTTP_200_OK)
#             # else:
#             #     # Add email verification information to response data
#             #     user_data = {
#             #         'message': 'Email not verified',
#             #         'email_verified': False
#             #     }
#             #     return Response(user_data, status=status.HTTP_403_FORBIDDEN)
#         else:
#             return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    # Sign in or Login control
    def post(self, request):
        email = request.data.get('email')  # Changed from username
        password = request.data.get('password')

        # Authenticate using email
        user = authenticate(request, username=email.strip(), password=password.strip())  # Django still uses 'username' param
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)

            user_data = {
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }

            if user.role == 'administrator':
                administrator = Administrator.objects.filter(user=user).first()
                if administrator is not None:
                    user_data['profile'] = AdministratorSerializer(administrator).data

            elif user.role == 'staff':
                staff = Staff.objects.filter(user=user).first()
                if staff is not None:
                    staff_data = StaffSerializer(staff).data
                    permission_groups = staff.permission_groups.all()
                    group_data = [
                        {
                            'id': group.id,
                            'name': group.name,
                            'permissions': [
                                {'id': p.id, 'codename': p.codename, 'name': p.name}
                                for p in group.permissions.all()
                            ]
                        }
                        for group in permission_groups
                    ]
                    staff_data['permission_groups'] = group_data
                    permissions = staff.permissions.all()
                    staff_data['permissions'] = [
                        {'id': p.id, 'codename': p.codename, 'name': p.name}
                        for p in permissions
                    ]
                    user_data['profile'] = staff_data

            elif user.role == 'supervisor':
                supervisor = Supervisor.objects.filter(user=user).first()
                if supervisor is not None:
                    user_data['profile'] = SupervisorSerializer(supervisor).data
                    try:
                        supervisor_id = int(supervisor.id)
                        user_data['enrollment'] = SupervisorEnrollmentAPIView().enrollment(supervisor_id)
                    except Exception as e:
                        user_data['enrollment'] = None

            elif user.role == 'trainee':
                trainee = Trainee.objects.filter(user=user).first()
                if trainee is not None:
                    user_data['profile'] = TraineeSerializer(trainee).data

            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)





























