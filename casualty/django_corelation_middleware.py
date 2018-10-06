import uuid

import structlog

from casualty.constants import HTTP_REQUEST_HEADER


class DjangoCorelationMiddleware(object):
    """
    If request_id header is present bind it to logger
    else create an ew request_id and bind it to logger
    It uses
    """

    def __init__(self, get_response):
        self.get_response = get_response
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="ISO"),
                structlog.processors.JSONRenderer(),
            ],
            context_class=structlog.threadlocal.wrap_dict(dict),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    def __call__(self, request):

        logger = structlog.getLogger()
        if request.META.get(HTTP_REQUEST_HEADER):
            current_request_id = request.META.get(HTTP_REQUEST_HEADER)

        else:
            current_request_id = str(uuid.uuid4())
        logger = logger.bind(request_id=current_request_id)

        response = self.get_response(request)

        return response