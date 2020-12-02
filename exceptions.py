"""
Common exception types
"""
class LumavateException(Exception):
  def __init__(self, message, **kwargs):
    self.message = message
    self.kwargs = kwargs
    super(LumavateException, self).__init__(message, kwargs)

class ApiException(Exception):
  """Generic API exception class - both a code and a message can be specified"""
  def __init__(self, status_code, message):
    # In order for celery pickling to work, you have to pass all arguments to the super
    super(ApiException, self).__init__(status_code, message)
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

class AsyncException(LumavateException):
  """Exception that occures during an async operation"""
  def __init__(self, message, retry=True, **kwargs):
    self.retry = retry
    # Pass all properties as specific kwargs to base
    # Passing retry as a kwarg to super so it'll be included when the exception is logged.
    super(AsyncException, self).__init__(message, retry=retry, **kwargs)

  def __setstate__(self, state):
    self.kwargs = state

  def __reduce__(self):
    # Helper for celery pickling. The 3rd part of the tuple is state which we'll use to put into the self.kwargs property
    # Since we pass "retry" as a kwarg to the super init, when unpickling we have to tell the pickler to pass message & retry as args
    return (self.__class__, (self.message, self.retry), self.kwargs)

class MaxAppException(ApiException):
  """Exception for free user when they reach max app limit"""
  def __init__(self):
    ApiException.__init__(
        self,
        402,
        "You've reached the limit of allowed apps for this account. "
        "Please upgrade your subscription to add more apps to your account.")
