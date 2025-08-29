from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging
import traceback

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    DRF custom exception handler that:
    - Delegates to DRF's default handler first
    - Formats errors consistently for clients (Postman/Frontend)
    - Avoids leaking internal details while logging enough on the server
    """
    response = drf_exception_handler(exc, context)

    view = context.get('view')
    request = context.get('request')
    endpoint = getattr(view, '__class__', type(view)).__name__ if view else 'unknown'
    path = getattr(request, 'path', 'unknown')

    if response is not None:
        # Known DRF exceptions: normalize structure
        data = {
            'error': True,
            'message': _extract_message(response.data),
            'details': response.data,
            'status_code': response.status_code,
            'endpoint': endpoint,
            'path': path,
        }
        # In DEBUG, attach extra info to help during development
        if settings.DEBUG:
            data['exc_type'] = type(exc).__name__
            data['trace'] = traceback.format_exc()
        response.data = data
        return response

    # Unknown/unhandled exceptions -> return 500 without internal details
    logger.exception('Unhandled exception at %s (%s)', path, endpoint, exc_info=exc)
    payload = {
        'error': True,
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'endpoint': endpoint,
        'path': path,
    }
    if settings.DEBUG:
        # Reveal details only in development
        payload.update({
            'message': str(exc) or 'Unhandled error',
            'exc_type': type(exc).__name__,
            'trace': traceback.format_exc(),
        })
    else:
        payload['message'] = "Une erreur de serveur s'est produite. Veuillez contacter l'administrateur."
    return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _extract_message(data):
    """Try to extract a human-friendly message from DRF error payloads."""
    if isinstance(data, dict):
        # Prefer 'detail' or 'message' keys if present
        for key in ('detail', 'message', 'error'):
            if key in data:
                val = data[key]
                if isinstance(val, (list, tuple)) and val:
                    return str(val[0])
                return str(val)
        # Fallback: join first errors
        if data:
            key, val = next(iter(data.items()))
            if isinstance(val, (list, tuple)) and val:
                return f"{key}: {val[0]}"
            return f"{key}: {val}"
    elif isinstance(data, (list, tuple)) and data:
        return str(data[0])
    return 'Requête invalide'
