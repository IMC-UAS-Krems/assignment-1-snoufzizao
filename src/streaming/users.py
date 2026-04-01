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
class User:
    def __init__(self, user_id, name, age=None):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        return sum(getattr(s, "duration_listened_seconds", 0) for s in self.sessions)

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self):
        return {s.track.track_id for s in self.sessions}


class FreeUser(User):
    def __init__(self, user_id, name, age=None):
        super().__init__(user_id, name, age)
        self.subscription_type = "Free"


class PremiumUser(User):
    def __init__(self, user_id, name, age=None, subscription_start=None):
        super().__init__(user_id, name, age)
        self.subscription_type = "Premium"
        self.subscription_start = subscription_start


class FamilyAccountUser(User):
    def __init__(self, user_id, name, age=None):
        super().__init__(user_id, name, age)
        self.subscription_type = "Family"
        self.sub_users = []

    def add_sub_user(self, member):
        # member is expected to be a FamilyMember instance
        if member not in self.sub_users:
            self.sub_users.append(member)

    def all_members(self):
        return [self] + list(self.sub_users)


class FamilyMember(User):
    def __init__(self, user_id, name, age=None, parent=None):
        super().__init__(user_id, name, age)
        self.parent = parent

