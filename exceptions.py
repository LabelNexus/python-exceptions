"""
Common exception types
"""
class LumavateException(Exception):
  def __init__(self, message, **kwargs):
    super(LumavateException, self).__init__(message)
    self.kwargs = kwargs

class ApiException(Exception):
  """Generic API exception class - both a code and a message can be specified"""
  def __init__(self, status_code, message):
    Exception.__init__(self)
    self.status_code = status_code
    self.message = message

  def to_dict(self):
    """Returns a dictionary that fully describes the exception"""
    return {"error": self.message}

  def __str__(self):
    return self.message

class AuthorizationException(ApiException):
  """Exception for when a user should be challenged for additional auth"""
  def __init__(self, message, user=None):
    self.user_id = None if user is None else user.id
    self.company_id = None if user is None else user.company_id
    ApiException.__init__(self, 401, message)

class NotFoundException(ApiException):
  """Exception for when a resource is not found"""
  def __init__(self, message):
    ApiException.__init__(self, 404, message)

class ValidationException(ApiException):
  """Exception for when inoput does not meet given requirements"""
  def __init__(self, message, api_field=None):
    ApiException.__init__(self, 400, message)
    self.api_field = api_field

  def __str__(self):
    if self.api_field is None:
      return self.message
    else:
      return '{} ({})'.format(self.message, self.api_field)

  def to_dict(self):
    result = {"error": self.message}
    if self.api_field is not None:
      result["apiField"] = self.api_field

    return result

class InvalidOperationException(ApiException):
  """Exception for when the given user can not perform the requested action"""
  def __init__(self, message):
    ApiException.__init__(self, 403, message)

class AsyncException(Exception):
  """Exception that occures during an async operation"""
  def __init__(self, message, retry=True):
    self.retry = retry
    super().__init__(message)
