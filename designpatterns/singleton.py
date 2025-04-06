#This is where the singleton pattern functionality goes.
class Singleton:
    _instance = None  #private static instance

    def __init__(self):
        #private constructor
        if Singleton._instance is not None:
            raise Exception("Call get_instance() to get the instance.")
    
    @staticmethod
    def get_instance():
        if Singleton._instance is None:
            Singleton._instance = Singleton()  #the lazy initialization
        return Singleton._instance

    def login_user(self, request, user):
        from django.contrib.auth import login
        login(request, user)
        request.session['is_authenticated'] = True
        request.session['user_id'] = user.id
        request.session.save()
