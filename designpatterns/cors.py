#This is where the cors pattern functionality goes.
from abc import ABC, abstractmethod

#handler defines an interface for handling requests
class Handler(ABC):
    def __init__(self):
        self.successor = None
    
    def set_successor(self, successor):
        self.successor = successor  #set successor handler
    
    @abstractmethod
    def handle_request(self, user, answer, question_number):
        pass

#concrete handler 1
class SecurityQuestion1Handler(Handler):
    def handle_request(self, user, answer, question_number):
        if question_number == 1:
            if user.security_answer_1 == answer:
                return True
        #pass the request to the successor if it can't handle it
        if self.successor:
            return self.successor.handle_request(user, answer, question_number)
        return False
#concrete handler 2
class SecurityQuestion2Handler(Handler):
    def handle_request(self, user, answer, question_number):
        if question_number == 2:
            if user.security_answer_2 == answer:
                return True
        #passs the request to the successor if it can't handle it
        if self.successor:
            return self.successor.handle_request(user, answer, question_number)
        return False
#concrete handler 3
class SecurityQuestion3Handler(Handler):
    def handle_request(self, user, answer, question_number):
        if question_number == 3:
            if user.security_answer_3 == answer:
                return True
        #pass the request to the successor if it can't handle it
        return super().handle_request(user, answer, question_number)

#client is within the views and inititates the request to a concretehandler object on the chian.