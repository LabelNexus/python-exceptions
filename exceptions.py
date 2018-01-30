class ApiException(Exception):
  def __init__(self, status_code, message):
    Exception.__init__(self)
    self.status_code = status_code
    self.message = message

  def to_dict(self):
    return {"error": self.message}

  def __str__(self):
    return self.message

class AuthorizationException(ApiException):
  def __init__(self, message, user=None):
    self.user_id = None if user is None else user.id
    self.company_id = None if user is None else user.company_id
    ApiException.__init__(self, 401, message)

class NotFoundException(ApiException):
  def __init__(self, message):
    ApiException.__init__(self, 404, message)

class ValidationException(ApiException):
  def __init__(self, message, api_field=None):
    ApiException.__init__(self, 400, message)
    self.api_field = api_field

  def to_dict(self):
    result = {"error": self.message}
    if self.api_field is not None:
      result["apiField"] = self.api_field

    return result

class InvalidOperationException(ApiException):
  def __init__(self, message):
    ApiException.__init__(self, 403, message)
