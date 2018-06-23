from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def registration(self, postData):
        errors = {}
#names
        if (len(postData["first_name"]) < 3) or (len(postData["last_name"]) < 3):
            errors["name_length"] = "First and last name must be at least 3 characters."
#password
        if (len(postData["password"]) < 8):
            errors["password_length"] = "Password must be at least 8 characters."
        if postData["password"] != postData["confirm_password"]:
            errors["password_mismatch"] = "Password must match password confirmation."
#email regex
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email_regex"] = "Must use a valid email."
#registered
        if User.objects.filter(email=postData["email"]).count() > 0:
            errors["email_exists"] = "Email already registered."
        return errors

    def login(self, postData):
        errors = {}
        user_list = User.objects.filter(email=postData["email"])
        if len(user_list) > 0:
            if bcrypt.checkpw(postData["password"].encode(), user_list[0].password.encode()):
                return errors
        errors["login_failed"] = "Login failed."
        return errors

    def edit(self, postData):
        errors = {}
        if (len(postData["first_name"]) < 3) or (len(postData["last_name"]) < 3):
            errors["name_length"] = "First and last name must be at least 3 characters."
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email_regex"] = "Must use a valid email."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()



class QuoteManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData["author"]) < 3:
            errors["author_name_length"] = "Author name must be at least 3 characters."
        if len(postData["content"]) < 10:
            errors["content_length"] = "Quote must be at least 10 characters."
        return errors

class Quote(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quotes_posted")
    author = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name="liked_quotes")
    objects = QuoteManager()
