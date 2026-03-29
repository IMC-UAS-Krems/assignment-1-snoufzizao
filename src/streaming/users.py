"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
class User():
    def __init__(self, username, email, age=None):
        self.username = username
        self.email = email
        self.age = age

    def __str__(self):
        return f"User: {self.username} ({self.email})"
    
class FreeUser(User):
    def __init__(self, username, email, age=None):
        super().__init__(username, email, age)
        self.subscription_type = "Free"
    
    def __str__(self):
        return f"Free User: {self.username} ({self.email})"
  

class PremiumUser(User):
    def __init__(self, username, email, age=None, subscription_start=None):
        super().__init__(username, email, age)
        self.subscription_type = "Premium"
        self.subscription_start = subscription_start

    def __str__(self):
        return f"Premium User: {self.username} ({self.email})"

class FamilyAccountUser(User):
    def __init__(self, username, email, age=None):
        super().__init__(username, email, age)
        self.subscription_type = "Family"
        self.members = []

    def NewMembers(self, username, email, age=None):
        self.members.append(FamilyMember(username, email, age))

    def __str__(self):
        return f"Family Account User: {self.username} ({self.email})"
    
class FamilyMember(User):
    def __init__(self, username, email, age=None, parent=None):
        super().__init__(username, email, age)
        self.subscription_type = "Family User"
        self.parent = parent

    def __str__(self):
        return f" Family Member: {self.username} ({self.email})"
