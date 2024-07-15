from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

class Books(models.Model):
    title = models.CharField(db_column="titre",max_length=200)
    genre = models.CharField(db_column="genre",max_length=200)
    auteur = models.CharField(db_column="auteur",max_length=200)
    isbn = models.CharField(db_column="isbn",max_length=13)
    nombre_de_copiess = models.IntegerField(db_column="number_of_copies")
    language = models.CharField(db_column="langue",max_length=50)
    resume= models.CharField(max_length=500)
    image = models.ImageField(upload_to='book_image', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class Loans(models.Model):
    book = models.ForeignKey(Books,db_column="book", on_delete=models.CASCADE)
    member = models.ForeignKey(User,db_column="member",on_delete=models.CASCADE)
    return_date = models.DateField(db_column="return_date",null=True,blank=True)
    due_date = models.DateField() 
    returned = models.BooleanField(default=False,db_column="returned")
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return f" Membre({self.member}), book( {self.book}) "
    
    

class Penalty(models.Model):
    loan = models.ForeignKey(Loans,db_column="loan", on_delete=models.CASCADE)
    reason = models.CharField(db_column="reason",max_length=200)

    def __str__(self):
        return f" L({self.loan})"
    
