from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail
from utils.base_serializer import get_error_message

class APIResponse:
    """
    Custom API Response class to standardize all API responses.
    """

    @staticmethod
    def success(return_code, message, data=None, status_code=status.HTTP_200_OK):
        """
        Create a success response with the standard structure.

        Args:
            return_code (str): A unique code identifying the response type (e.g., 'login_success')
            message (str): A human-readable message
            data (dict, optional): The response data. Defaults to None.
            status_code (int, optional): HTTP status code. Defaults to 200.

        Returns:
            Response: A standardized success response
        """
        response_data = {
            "return_code": return_code,
            "status": True,
            "message": message,
            "data": data or {},
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def error(return_code, message, data=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Create an error response with the standard structure.

        Args:
            return_code (str): A unique code identifying the error type (e.g., 'invalid_credentials')
            message (str): A human-readable error message
            data (dict, optional): Additional error details. Defaults to None.
            status_code (int, optional): HTTP status code. Defaults to 400.

        Returns:
            Response: A standardized error response
        """
        response_data = {
            "return_code": return_code,
            "status": False,
            "message": message,
            "data": data or {},
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def get_success_response(return_code, data=None, status_code=status.HTTP_200_OK):
        """
        Create a success response with automatic message lookup.
        
        Args:
            return_code (str): A unique code identifying the response type
            data (dict, optional): The response data. Defaults to None.
            status_code (int, optional): HTTP status code. Defaults to 200.
        
        Returns:
            Response: A standardized success response
        """
        message = APIResponse.Codes._success_messages.get(return_code, "Success")
        response_data = {
            "return_code": return_code,
            "status": True,
            "message": message,
            "data": data or {},
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def get_serializer_error_response(return_code, serializer_errors: dict):
        field_error, field_error_message = get_error_message(
            serializer_errors=serializer_errors,
            error_messages_dict=APIResponse.Codes._error_messages,
        )
        response_data = {
            "return_code": return_code,
            "status": False,
            "message": field_error_message,
            "data": {},
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def get_error_response(return_code, message, status_code=status.HTTP_400_BAD_REQUEST, data=None):
        return Response({
            "return_code": return_code,
            "status": False,
            "message": message,
            "data": data or {},
        }, status=status_code)

    
    # Common response codes
    class Codes:
        # Authentication codes
        LOGIN_SUCCESS = "login_success"
        LOGOUT_SUCCESS = "logout_success"
        REGISTRATION_SUCCESS = "registration_success"
        TOKEN_INVALID = "token_invalid"
        
        # Validation codes
        VALIDATION_ERROR = "validation_error"
        
        # Account related codes
        PROFILE_RETRIEVED = "profile_retrieved"
        PROFILE_UPDATED = "profile_updated"
        PASSWORD_RESET_EMAIL_SENT = "password_reset_email_sent"
        PASSWORD_CHANGE_SUCCESS = "password_change_success"
        OTP_VERIFIED = "otp_verified"
        OTP_VERIFICATION_FAILED = "otp_verification_failed"
        OTP_EXPIRED = "otp_expired"
        OTP_RESENT = "otp_resent"
        OTP_REQUIRED = "otp_required"
        OTP_INVALID = "otp_invalid"
        OTP_DO_NOT_MATCH = "otp_do_not_match"
        EMAIL_OTP_REQUIRED = "email_otp_required"
        USER_DELETED_SUCCESS = "user_deleted_success"
        USERS_LIST_RETRIEVED = "users_list_retrieved"
        INVALID_LINK = "invalid_link"
        
        # User related codes
        USER_NOT_FOUND = "user_not_found"
        USER_EXISTS = "username_exists"
        
        # Success messages dictionary
        _success_messages = {
            LOGIN_SUCCESS: "Login successful.",
            LOGOUT_SUCCESS: "Logout successful.",
            REGISTRATION_SUCCESS: "Registration successful. Please verify your email with the OTP sent.",
            PROFILE_RETRIEVED: "Profile retrieved successfully.",
            PROFILE_UPDATED: "Profile updated successfully.",
            PASSWORD_RESET_EMAIL_SENT: "Password reset email sent successfully.",
            PASSWORD_CHANGE_SUCCESS: "Password changed successfully.",
            OTP_VERIFIED: "OTP verified successfully.",
            OTP_RESENT: "OTP resent successfully.",
            USER_DELETED_SUCCESS: "User deleted successfully.",
            USERS_LIST_RETRIEVED: "Users list retrieved successfully.",
        }
        
        # Login api serializer error codes
        LOGIN_CREDENTIAL_REQUIRED = "login_credential_required"
        LOGIN_CREDENTIAL_INVALID = "login_credential_invalid"
        LOGIN_USER_NOT_ACTIVE = "login_user_not_active"
        LOGIN_USER_NOT_VERIFY = "login_user_not_verify"
        
        # Register user api serializer error codes
        EMAIL_REQUIRED = "email_required"
        EMAIL_ALREADY_EXISTS = "email_already_exists"
        PASSWORD_LENGTH_INVALID = "password_length_invalid"
        PASSWORD_VALIDATION_FAILED = "password_validation_failed"
        PASSWORDS_DO_NOT_MATCH = "passwords_do_not_match"
        PASSWORD_REQUIRED = "password_required"
        CONFIRM_PASSWORD_INVALID = "confirm_password_invalid"
        OLD_PASSWORD_INVALID = "old_password_invalid"
        SAME_PASSWORD= "same_password"
        PHONE_INVALID= "phone_invalid"
        PHONE_ALREADY_EXISTS = "phone_already_exists"
        PHONE_ONLY_DIGIT= "only_digit_required"
        
        # Account status codes
        ACCOUNT_NOT_VERIFIED = "account_not_verified"
        ACCOUNT_INACTIVE = "account_inactive"
        EMAIL_NOT_FOUND = "email_not_found"
        
        # Error messages dictionary
        _error_messages = {
            # login api serializer error
            LOGIN_CREDENTIAL_REQUIRED: "Email and password are required to log in.",
            LOGIN_CREDENTIAL_INVALID: "Invalid email or password. Please try again.",
            LOGIN_USER_NOT_ACTIVE: "Your account is disabled or inactive.",
            LOGIN_USER_NOT_VERIFY: "Please confirm your email address to log in.",
            
            # register user api serializer error 
            EMAIL_REQUIRED: "Email is required.",
            EMAIL_ALREADY_EXISTS: "A user with this email already exists.",
            PASSWORD_LENGTH_INVALID: "Password must contains atleast 8 or 16 characters.",
            PASSWORD_VALIDATION_FAILED: "Password validation failed.",
            PASSWORDS_DO_NOT_MATCH: "Passwords do not match.",
            PASSWORD_REQUIRED: "Password is required.",
            OLD_PASSWORD_INVALID: "Old Password is invalid.",
            SAME_PASSWORD: "New password is same as old password",
            CONFIRM_PASSWORD_INVALID: "Confirm password must be the same",
            PHONE_INVALID:"Phone number is not valid",
            PHONE_ONLY_DIGIT: "Phonenumber must contain digit only.",
            PHONE_ALREADY_EXISTS: "A user with this phone already exists.",
            
            # Account status errors
            ACCOUNT_INACTIVE: "This account is inactive.",
            ACCOUNT_NOT_VERIFIED: "Account is not verified. Please verify your email.",
            EMAIL_NOT_FOUND: "No user found with this email.",
            
            # OTP related errors
            OTP_INVALID: "OTP must contain only digits.",
            OTP_VERIFICATION_FAILED: "OTP verification failed.",
            OTP_EXPIRED: "OTP has expired.",
            OTP_REQUIRED: "OTP is required.",
            OTP_DO_NOT_MATCH: "OTP is invalid please enter from email!",
            EMAIL_OTP_REQUIRED: "Email and OTP are required.",
            
            # Password reset errors
            INVALID_LINK: "Invalid or expired link.",
            TOKEN_INVALID: "Token is invalid or expired.",
            
            # Validation error
            VALIDATION_ERROR: "Validation error.",
            USER_EXISTS: "Username already exists.",
        }

def get_first_error(errors, error_message=""):
    if isinstance(errors, dict):
        for key, value in errors.items():
            print(key)
            error_message += f"{key}."
            return get_first_error(value, error_message)
    elif isinstance(errors, list):
        if errors and isinstance(errors[0], (str, ErrorDetail)):
            message = f"{error_message.rstrip('.')}: {str(errors[0])}"
            return message
        elif errors and isinstance(errors[0], dict):
            return get_first_error(errors[0], error_message)
    return "An unknown error occurred"
