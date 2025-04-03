#This is where the cors pattern functionality goes.

class SecurityQuestionHandler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
    
    def handle(self, user, answer, question_number):
        if self.next_handler:
            return self.next_handler.handle(user, answer, question_number)
        return False

class SecurityQuestion1Handler(SecurityQuestionHandler):
    def handle(self, user, answer, question_number):
        if question_number == 1:
            if user.security_answer_1 == answer:
                return True
        return super().handle(user, answer, question_number)

class SecurityQuestion2Handler(SecurityQuestionHandler):
    def handle(self, user, answer, question_number):
        if question_number == 2:
            if user.security_answer_2 == answer:
                return True
        return super().handle(user, answer, question_number)

class SecurityQuestion3Handler(SecurityQuestionHandler):
    def handle(self, user, answer, question_number):
        if question_number == 3:
            if user.security_answer_3 == answer:
                return True
        return super().handle(user, answer, question_number)
