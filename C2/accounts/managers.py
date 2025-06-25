from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, email,  full_name, password):
        if not phone_number:
            raise ValueError('Users must have phone_number')
        if not email:
            raise ValueError('Users must have email')
        if not full_name:
            raise ValueError('Users must have full_name')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email,  full_name, password):
        user = self.create_user( phone_number,  email,  full_name,password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user