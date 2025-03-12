from django.db import models

class Admin(models.Model):
    """ Admin model """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    password_hash = models.TextField(null=False)
    salt = models.TextField(null=False)

    class Meta:
        db_table = "admins"

    def __str__(self):
        return self.username