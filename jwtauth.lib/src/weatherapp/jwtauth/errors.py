from http import HTTPStatus


class JWTError(Exception):
    status: HTTPStatus


class JWTDecodeError(JWTError):
    status = HTTPStatus.BAD_REQUEST


class JWTExpiredSignatureError(JWTError):
    status = HTTPStatus.UNAUTHORIZED


class JWTTokenRequired(JWTError):
    status = HTTPStatus.UNAUTHORIZED


class JWTInvalidType(JWTError):
    status = HTTPStatus.BAD_REQUEST


class JWTUserNotExist(JWTError):
    status = HTTPStatus.UNAUTHORIZED
