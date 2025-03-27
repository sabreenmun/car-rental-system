class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def login_user(self, request, user):
        from django.contrib.auth import login  # Import here to prevent circular imports
        login(request, user)
        request.session['is_authenticated'] = True
        request.session['user_id'] = user.id
        request.session.save()
