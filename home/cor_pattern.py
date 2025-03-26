class SecurityQuestionHandler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, car_owner, answers):
        pass


class FirstSecurityQuestionHandler(SecurityQuestionHandler):
    def handle(self, car_owner, answers):
        if answers.get('security_answer_1') == car_owner.security_answer_1:
            if self.next_handler:
                return self.next_handler.handle(car_owner, answers)
            return True
        return False


class SecondSecurityQuestionHandler(SecurityQuestionHandler):
    def handle(self, car_owner, answers):
        if answers.get('security_answer_2') == car_owner.security_answer_2:
            if self.next_handler:
                return self.next_handler.handle(car_owner, answers)
            return True
        return False


class ThirdSecurityQuestionHandler(SecurityQuestionHandler):
    def handle(self, car_owner, answers):
        if answers.get('security_answer_3') == car_owner.security_answer_3:
            if self.next_handler:
                return self.next_handler.handle(car_owner, answers)
            return True
        return False
