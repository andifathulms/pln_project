from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from django.conf import settings

from notification.models import Notification

class MyAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have username')
        
        user = self.model(
            email = self.normalize_email(email),
            name = name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    name                    = models.CharField(max_length=50, unique=True)
    division                = models.CharField(max_length=100)
    role                    = models.CharField(max_length=100)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)

    # set up the reverse relation to GenericForeignKey
    notifications   		= GenericRelation(Notification)	

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = MyAccountManager()

    def __str__(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def  has_module_perms(self, app_label):
        return True
    
    def create_notif_first_login(self, account):
        content_type = ContentType.objects.get_for_model(self)
        
        self.notifications.create(
            target=self,
            from_user=account,
			redirect_url=f"{settings.BASE_URL}",
			verb="Welcome to UIP Apang !",
			content_type=content_type,
		)
        self.save()
        print("DONE")
    
    @property
    def get_cname(self):
        """
		For determining what kind of object is associated with a Notification
		"""
        return "Account"