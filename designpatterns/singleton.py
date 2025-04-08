#This is where the Singleton pattern functionality goes.
class Singleton:
    _instance = None  #private static instance

    def __init__(self):
        #private constructor 
        if Singleton._instance is not None:
            raise Exception("Call get_instance() to get the instance.")
    
    @staticmethod
    def get_instance():
         #method to get the single instance (lazy initialization)
        if Singleton._instance is None:
            Singleton._instance = Singleton() #creates the instance if it doesn't exist
        return Singleton._instance

    def login_user(self, request, user):
        #method to log the user in and set the session variables
        from django.contrib.auth import login
        login(request, user)  # logs the user in
        request.session['is_authenticated'] = True  #sets session to authenticated
        request.session['user_id'] = user.id  #stores the user's ID in session
        request.session.save()  #saves the session data
