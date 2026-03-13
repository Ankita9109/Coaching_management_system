from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Sum
from reportlab.pdfgen import canvas
import random

from .models import Student, Fee, Attendance, Course
from .forms import StudentForm


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_fees = Fee.objects.aggregate(total=Sum("amount"))["total"] or 0

    return render(request, "layout/dashboard.html", {
        "students": total_students,
        "fees": total_fees
    })


@login_required
def add_student(request):
    form = StudentForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("student_list")

    return render(request, "students/add_student.html", {"form": form})


@login_required
def student_list(request):
    query = request.GET.get("q")

    if query:
        students = Student.objects.filter(name__icontains=query)
    else:
        students = Student.objects.all()

    return render(request, "students/student_list.html", {"students": students})


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    courses = Course.objects.all()

    if request.method == "POST":
        student.name = request.POST["name"]
        student.phone = request.POST["phone"]

        course_id = request.POST["course"]
        student.course = Course.objects.get(id=course_id)

        student.save()

        return redirect("student_list")

    return render(request, "students/edit_student.html", {
        "student": student,
        "courses": courses
    })


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("student_list")


@login_required
def add_fee(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        amount = request.POST.get("amount")

        if amount:
            Fee.objects.create(student=student, amount=amount)

        return redirect("fee_history", student_id=student.id)

    return render(request, "fees/add_fee.html", {"student": student})


@login_required
def fee_history(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    fees = Fee.objects.filter(student=student)

    return render(request, "fees/fee_history.html", {
        "student": student,
        "fees": fees
    })


@login_required
def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    total_fees = Fee.objects.filter(student=student).aggregate(
        total=Sum("amount")
    )["total"] or 0

    remaining = student.course.fee - total_fees

    total_classes = Attendance.objects.filter(student=student).count()
    present_classes = Attendance.objects.filter(
        student=student,
        present=True
    ).count()

    percent = int((present_classes / total_classes) * 100) if total_classes else 0

    return render(request, "students/profile.html", {
        "student": student,
        "fees": total_fees,
        "attendance": percent,
        "remaining": remaining
    })


@login_required
def mark_attendance(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        status = request.POST.get("status")

        Attendance.objects.create(
            student=student,
            present=status == "Present"
        )

        return redirect("student_list")

    return render(request, "attendance/mark_attendance.html", {"student": student})


@login_required
def attendance_history(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    records = Attendance.objects.filter(student=student)

    return render(request, "attendance/attendance_history.html", {
        "student": student,
        "records": records
    })


@login_required
def daily_attendance(request):
    students = Student.objects.all()

    if request.method == "POST":

        for student in students:
            status = request.POST.get(str(student.id))

            if status:
                Attendance.objects.create(
                    student=student,
                    present=status == "Present"
                )

        return redirect("student_list")

    return render(request, "attendance/daily_attendance.html", {
        "students": students
    })

@login_required
def fee_receipt(request, fee_id):

    fee = get_object_or_404(Fee, id=fee_id)
    student = fee.student

    total_paid = Fee.objects.filter(student=student).aggregate(
        total=Sum("amount")
    )["total"] or 0

    remaining = student.course.fee - total_paid

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="receipt.pdf"'

    p = canvas.Canvas(response)

    p.drawString(200, 800, "Fee Receipt")

    p.drawString(100, 750, f"Student: {student.name}")
    p.drawString(100, 730, f"Phone: {student.phone}")
    p.drawString(100, 710, f"Course: {student.course.name}")

    p.drawString(100, 680, f"Total Fee: ₹{student.course.fee}")
    p.drawString(100, 660, f"Paid Now: ₹{fee.amount}")
    p.drawString(100, 640, f"Total Paid: ₹{total_paid}")
    p.drawString(100, 620, f"Remaining: ₹{remaining}")

    p.drawString(100, 590, f"Date: {fee.date}")

    p.save()

    return response


def otp_reset(request):

    if request.method == "POST":

        # STEP 1 : Username
        if request.POST.get("username"):
            try:
                user = User.objects.get(username=request.POST["username"])
                otp = str(random.randint(100000, 999999))

                request.session["otp"] = otp
                request.session["uid"] = user.id

                return render(request, "otp.html", {"stage": "verify", "otp": otp})

            except User.DoesNotExist:
                return render(request, "otp.html", {"error": "User not found"})


        # STEP 2 : OTP verify
        if request.POST.get("otp") == request.session.get("otp"):

            user = User.objects.get(id=request.session["uid"])
            user.set_password(request.POST["password"])
            user.save()

            return redirect("/login/")

        return render(request, "otp.html", {"stage": "verify", "error": "Wrong OTP"})

    return render(request, "otp.html")


# @login_required
# def dashboard(request):
#     total_students = Student.objects.count()
#     total_fees = sum(f.amount for f in Fee.objects.all())
#     # f object type ka vairiable kyu ki vo fee class ke object ko hold kar rha h

#     context = {
#         "students": total_students,
#         "fees": total_fees
#     }
#     return render(request, "layout/dashboard.html", context)



    # if request.method == "POST":
    #     # backend variable name = frontend variable name
    #     name = request.POST['name'] #frontend ke se ane vale name ko b.e.ke name variable store kar rhi hu
    #     phone = request.POST['phone']
    #     course = request.POST['course']

    #     if not name or not phone or not course:
    #         messages.error(request, "All fields are required!")
    #         return redirect("add_student")
        
    #     #name=name mens DB ke feild var me= yaha pe jo var.banaya h uska data insert kar rhi hu
    #     Student.objects.create(name=name, phone=phone, course=course)

    #     messages.success(request, "Student added successfully!")
    #     return redirect("student_list")

    # return render(request, "students/add_student.html")

