from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

class CustomIsAuthenticated(BaseAuthentication):
   
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # No authentication header found

        # Extract token from header
        token = auth_header.split(' ')[1]

        try:
            # Validate the token
            AccessToken(token=token).payload
        except Exception as e:
            # Token is invalid or expired
            raise AuthenticationFailed({'detail': 'Invalid token', 'code': 'token_not_valid'})

        # Token is valid, set the authenticated user
        return (AccessToken(token=token).get_user(), None)
    # def has_permission(self, request, view):
        # print("called")
        # try:
        #     request.user or request.user.is_authenticated
        #     # Customize the response as needed
        #     response_data = {'error_message': 'Authentication required'}
        #     view.permission_denied(request, message=response_data)
        #     return True
        # except Exception as e:
                # return True