class UserNotFoundError(Exception):
    def __init__(self):
        super().__init__("User not found")

class RepeatedEmailError(Exception):
    def __init__(self):
        super().__init__("Someone is already using this email, please write a different one")

class InvalidCredentialsError(Exception):
    def __init__(self):
        super().__init__("Invalid email or password")

class InvalidToken(Exception):
    def __init__(self):
        super().__init__("Invalid token")

class ExpiredToken(Exception):
    def __init__(self):
        super().__init__("Expired token")
    
class InactiveUserError(Exception):
    def __init__(self):
        super().__init__("User is inactive")
    
class UserInUseError(Exception):
    def __init__(self):
        super().__init__("User has related records and cannot be deleted. Deactivate it instead")

class CannotDeleteSelfError(Exception):
    def __init__(self):
        super().__init__("You cannot delete your own user")