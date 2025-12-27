from typing import Any, List

from django.db import models
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail


def get_response_serializer(
    model: models.Model, fields: List[str] = [], exclude_fields: List[str] = []
):
    if not any([fields, exclude_fields]):
        raise ValueError("Please provide either of fields : fields or exclude fields")

    # if  all(fields and exclude_fields):
    if fields and exclude_fields:
        raise ValueError(
            "Please only provide either of fields : fields or exclude fields"
        )

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            pass

    ResponseSerializer.Meta.model = model
    if fields:
        ResponseSerializer.Meta.fields = fields
    else:
        ResponseSerializer.Meta.exclude = exclude_fields

    return ResponseSerializer


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(BaseModelSerializer, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages = get_error_messages_code(field_name)


def get_crud_serializer(model: models.Model, fields: list = [], update=True):

    if not fields:
        raise ValueError("Please provide fields to edit.")
    if not model:
        raise ValueError("Please provide model for the serializer")

    class BaseCrudSerializer(BaseModelSerializer):
        def __init__(self, *args, **kwargs):
            if update:
                pk_field = self.Meta.model._meta.pk.name
                self.fields[pk_field] = serializers.PrimaryKeyRelatedField(
                    queryset=self.Meta.model.objects.dfilter(),
                    required=True,
                )
            super(BaseCrudSerializer, self).__init__(*args, **kwargs)

            for field_name, field in self.fields.items():
                field.required = True

        class Meta:
            pass

    BaseCrudSerializer.Meta.model = model

    BaseCrudSerializer.Meta.fields = fields

    return BaseCrudSerializer


class BaseSerializerSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super(BaseSerializerSerializer, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages = get_error_messages_code(field_name)


def get_error_messages_code(field_name: str = None, extra_kwargs_fields: list = None):
    if field_name:
        return {
            "required": f"{field_name}_required",
            "blank": f"{field_name}_blank",
            "invalid": f"{field_name}_invalid",
            "does_not_exist": f"{field_name}_does_not_exist",
            "incorrect_type": f"{field_name}_invalid",
            "min_value": f"{field_name}_min_value",
            "max_value": f"{field_name}_max_value",
            "max_length": f"{field_name}_max_length",
            "null": f"{field_name}_null",
        }
    elif extra_kwargs_fields:
        return {
            field_name: {
                "error_messages": get_error_messages_code(field_name=field_name)
            }
            for field_name in extra_kwargs_fields
        }


def get_full_error_messages(field_name, field_error,error_messages_dict):
    # print("101 field_name", field_name)
    # print("101 field_error", field_error)
    _base_messages_dict = {
        f"{field_name}_null": f"{field_name} should not be null.",
        f"{field_name}_required": f"Key : {field_name} is missing.",
        f"{field_name}_blank": f"Please enter value for {field_name}.",
        f"{field_name}_invalid": f"Please enter a valid value for Field : {field_name}.",
        f"{field_name}_does_not_exist": "No record found.",
        f"{field_name}_incorrect_type": f"Please enter a valid value for Field : {field_name}.",
        f"{field_name}_min_value": "Please enter a value greater than min value.",
        f"{field_name}_max_value": f"You have exceeded the maximum value for {field_name}",
        f"{field_name}_max_length": f"You have exceeded the maximum length for {field_name}",
    }
    _base_messages_dict = _base_messages_dict | error_messages_dict
    # _base_messages_dict = _base_messages_dict | {
    #     "non_field_errors": "Please check the fields and try again."
    # }
    
    # Extract error code from ErrorDetail object or use the string directly
    if isinstance(field_error, ErrorDetail):
        error_code = field_error.code
        error_message = str(field_error)
    else:
        error_code = str(field_error)
        error_message = str(field_error)
    
    # For ErrorDetail objects, check if message is a custom message (not a generic one)
    # Custom messages usually don't contain generic patterns like "Please enter a valid value"
    if isinstance(field_error, ErrorDetail):
        # Generic message patterns that we should replace with dictionary messages
        generic_patterns = [
            "Please enter a valid value for Field",
            "This field is required",
            "This field may not be blank",
            "This field may not be null"
        ]
        
        is_generic = any(pattern in error_message for pattern in generic_patterns)
        
        # If message is not generic, it's likely a custom message - use it directly
        if not is_generic:
            # If the custom message is actually the code itself, try dictionary lookup
            if error_message == error_code:
                # If error_code already starts with field_name (e.g., "email_blank")
                if error_code in _base_messages_dict:
                    return _base_messages_dict[error_code]
                field_specific_code = f"{field_name}_{error_code}"
                if field_specific_code in _base_messages_dict:
                    return _base_messages_dict[field_specific_code]
            return error_message
        
        # For generic messages, try dictionary lookup
        # Check if error_code already starts with field_name (e.g., "password2_required")
        # This happens when BaseModelSerializer has set custom error codes
        if error_code.startswith(f"{field_name}_"):
            # Error code is already field-specific, use it directly
            if error_code in _base_messages_dict:
                return _base_messages_dict[error_code]
        
        # Try constructing field-specific error code (e.g., "password2_required" from "required")
        field_specific_code = f"{field_name}_{error_code}"
        if field_specific_code in _base_messages_dict:
            return _base_messages_dict[field_specific_code]
        
        # Try exact error code as fallback
        if error_code in _base_messages_dict:
            return _base_messages_dict[error_code]
        
        # If not found in dict but message is generic, return the generic message
        return error_message
    
    # For non-ErrorDetail errors, try dictionary lookup
    # First try the exact error code
    if error_code in _base_messages_dict:
        return _base_messages_dict[error_code]
    
    # If not found, try constructing field-specific error code (e.g., "password2_required")
    field_specific_code = f"{field_name}_{error_code}"
    if field_specific_code in _base_messages_dict:
        return _base_messages_dict[field_specific_code]
    
    # Final fallback to a generic message
    return f"Validation error for {field_name}: {error_message}"


def get_error_message(serializer_errors, error_messages_dict) -> tuple:
    """
    Get the first error message from serializer errors.
    Returns only one error at a time (first field, first error).
    
    Args:
        serializer_errors: Dictionary of serializer errors
        error_messages_dict: Dictionary of custom error messages
        
    Returns:
        tuple: (error_detail, error_message) - Returns only the first error
    """
    # Get the first field that has an error
    if not serializer_errors:
        return None, "Unknown validation error."
    
    error_field = list(serializer_errors.keys())[0]
    field_errors = serializer_errors[error_field]
    
    # Get only the first error from this field (even if multiple exist)
    if not field_errors:
        return None, f"Validation error for {error_field}."
    
    # Take only the first error from the list
    first_error = field_errors[0] if isinstance(field_errors, list) else field_errors
    
    # Handle non_field_errors
    if error_field == "non_field_errors":
        error_detail = first_error
        # Extract error code from ErrorDetail or use the string directly
        if isinstance(error_detail, ErrorDetail):
            error_code = error_detail.code
            error_message = error_messages_dict.get(error_code, str(error_detail))
        else:
            error_code = str(error_detail)
            error_message = error_messages_dict.get(error_code, str(error_detail))
        return error_detail, error_message
    
    # Handle field-specific errors
    return (
        first_error,
        get_full_error_messages(
            field_name=error_field,
            field_error=first_error,
            error_messages_dict=error_messages_dict,
        ),
    )
