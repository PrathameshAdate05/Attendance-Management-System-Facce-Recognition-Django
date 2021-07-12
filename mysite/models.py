from django.db import models
import datetime

# Create your models here.

class facultyReg(models.Model):

    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)



class studentreg(models.Model):
    rollno=models.CharField(max_length=100)
    enrollmentno=models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    dob=models.DateField()
    studentimage=models.ImageField(upload_to='studentImages/',blank=True)
    dept=models.CharField(max_length=100)

    def __str__(self):
        return self.rollno


class mon_reports(models.Model):
    sroll = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    present_date = models.DateField()
    present_time = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    curmonth = models.CharField(max_length=100)

    def __str__(self):
        return self.sroll


# class s_reports(models.Model):
#     sroll = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     period = models.CharField(max_length=100)
#     present_date = models.DateField()
#     present_time = models.CharField(max_length=100)
#     status = models.CharField(max_length=100)
#     curmonth = models.CharField(max_length=100)



