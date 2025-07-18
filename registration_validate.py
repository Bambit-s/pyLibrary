class RegistrationValidate:
    @staticmethod
    def _validate(user):
        
        errors = {}
        existing_user = user.query.filter_by(email=user.email).first()
        
        if existing_user:
            errors['email'] = 'This email is closed'
        else:
            print("Nope")
        return errors