import logging
from auto_nornir.core.helpers import configure_logging

logger = logging.getLogger(__name__)


class AutoNornirException(Exception):

    configure_logging(logger)

    REASONS = (
        "fail-config",  # config provided is not valid
        "fail-connect",  # device is unreachable at IP:PORT
        "fail-execute",  # unable to execute device/API command
        "fail-login",  # bad username/password
        "fail-general",  # other error
    )

    def __init__(self, reason, message, **kwargs):
        """Exception Init."""
        super(AutoNornirException, self).__init__(kwargs)
        self.reason = reason
        self.message = message
        logger.error(message)

    def __str__(self):
        """Exception __str__."""
        return f"{self.__class__.__name__}: {self.reason}: {self.message}"


class ValidationException(AutoNornirException):
    pass

class RuntimeErrorException(AutoNornirException):
    pass
