from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    total_fee = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Fee(models.Model):
    # agr me student record se kisi student ko delete karungi to 
    # fk ke thougth us name se relete sari row ,data delete ho jayega
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)

# class Attendance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)
#     status = models.CharField(max_length=10)  # Present / Absent


class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=True)

    def __str__(self):
        return self.student.name
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    fee = models.IntegerField()

    def __str__(self):
        return self.name