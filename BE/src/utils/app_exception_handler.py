from uuid import UUID


class AuthService:
    def __init__(self, queries):
        self.queries = queries

    def register(self, user_data):
        row = self.queries.get_by_email(user_data.email)
        if row:
            return 409, "Email already registered"

        user_data.password = self.queries.hash_helper.hash_password(user_data.password)

        user = self.queries.create(user_data)
        if not user:
            return 400, "Creation failed"
        return 200, user

    def authenticate(self, email: str, password: str):
        user = self.queries.get_by_email(email)

        if not user or user.get("is_deleted"):
            return None

        is_valid = self.queries.hash_helper.verify_password(password, user["password"])

        if not is_valid:
            return None

        return user

    def update_profile(self, user_id: UUID, update_data):
        profile = self.queries.update(user_id, update_data)
        if not profile:
            return None
        return profile
