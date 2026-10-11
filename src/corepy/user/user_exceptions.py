class UserNotFoundError(Exception):
    message = "User not found."

    def __str__(self):
        return self.message


class RepeatedEmailError(Exception):
    message = "Someone is already using this email, please write a different one."

    def __str__(self):
        return self.message


class InvalidCredentialsError(Exception):
    message = "Invalid email or password."

    def __str__(self):
        return self.message


class InvalidToken(Exception):
    message = "Invalid token."

    def __str__(self):
        return self.message


class ExpiredToken(Exception):
    message = "Expired token."

    def __str__(self):
        return self.message
    
class InactiveUserError(Exception):
    message = "User is inactive."

    def __str__(self):
        return self.message
    
class UserInUseError(Exception):
    message = "User has related records and cannot be deleted. Deactivate it instead."

    def __str__(self):
        return self.message

class CannotDeleteSelfError(Exception):
    message = "You cannot delete your own user."

    def __str__(self):
        return self.message