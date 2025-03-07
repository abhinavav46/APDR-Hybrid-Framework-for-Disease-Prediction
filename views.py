import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# from myapp.DBConnection import Db
from myapp.predict import predictcnn
from myapp.predict_alz import predictcnn_alz
from myapp.predict_pd import predictcnn_pd
from .models import *

img_path=r"D:\softwares\Project\diabetic\myapp\static\images\\"

# Create your views here.
def logg(request):
    return render(request, "index.html")
def logg_post(request):
    uname=request.POST['t1']
    psw=request.POST['t2']
    lg=login.objects.filter(username=uname, password=psw)
    if lg.exists():
        lg=lg[0]
        request.session['lid']=lg.id
        if lg.usertype == "admin":
            return redirect("/admin_home")
        elif lg.usertype == "hospital":
            res=hospital.objects.get(LOGIN_id=lg.id)
            request.session['uname']=res.user_name
            return redirect("/hosp_home")
        elif lg.usertype == "patient":
            res=patient.objects.get(LOGIN_id=lg.id)
            request.session['uname']=res.user_name
            return redirect("/patient_home")
        else:
            return HttpResponse("<script>alert('Waiting for approval');window.location='/';</script>")

    else:
        return HttpResponse("<script>alert('Invalid details');window.location='/';</script>")



def reg(request,i):
    return render(request, "hospital_signup.html",{"i":i})
def reg_post(request,i):
    hname=request.POST['t1']
    email=request.POST['t2']
    phone=request.POST['t3']
    place=request.POST['t4']
    pin=request.POST['t5']
    post=request.POST['t6']
    psw=request.POST['t7']
    if login.objects.filter(username=email).exists():
        return HttpResponse("<script>alert('Email already exists');window.location='/';</script>")
    if i == "h":

        obj=login()
        obj.username=email
        obj.password=psw
        obj.usertype="pending"
        obj.save()

        obj2=hospital()
        obj2.user_name=hname
        obj2.email=email
        obj2.phone=phone
        obj2.place=place
        obj2.post=post
        obj2.pin=pin
        obj2.LOGIN=obj
        obj2.save()
        return HttpResponse("<script>alert('Registered.. Please wait for verification');window.location='/';</script>")
    else:
        obj = login()
        obj.username = email
        obj.password = psw
        obj.usertype = "patient"
        obj.save()

        obj2 = patient()
        obj2.user_name = hname
        obj2.email = email
        obj2.phone = phone
        obj2.place = place
        obj2.post = post
        obj2.pin = pin
        obj2.LOGIN = obj
        obj2.save()
        return HttpResponse("<script>alert('Registered..');window.location='/';</script>")


def admin_home(request):
    return render(request, "admin/index.html")

def admin_add_dis(request):
    return render(request, "admin/add_disease.html")

def admin_add_dis_post(request):
    name=request.POST['t1']
    descr=request.POST['t2']
    prec=request.POST['t3']
    obj=disease()
    obj.disease=name
    obj.description=descr
    obj.precautions=prec
    obj.save()
    return HttpResponse("<script>alert('Disease added');window.location='/admin_add_dis#content';</script>")

def admin_view_dis(request):
    res=disease.objects.all()
    return render(request, "admin/view_disease.html", {'data':res})

def admin_delete_dis(request, id):
    disease.objects.get(id=id).delete()
    return redirect("/admin_view_dis#content")

def admin_verify_hospital(request):
    res=hospital.objects.filter(LOGIN__usertype="pending")
    return render(request, "admin/verify_hospital.html", {'data':res})

def admin_approve_hospital(request, id):
    login.objects.filter(id=id).update(usertype="hospital")
    return HttpResponse("<script>alert('Approved');window.location='/admin_verify_hospital#content';</script>")

def admin_reject_hospital(request, id):
    login.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Rejected');window.location='/admin_verify_hospital#content';</script>")

def admin_view_verified_hospital(request):
    res=hospital.objects.filter(LOGIN__usertype="hospital")
    return render(request, "admin/verified_hospital.html", {'data':res})

def admin_view_patient(request):
    res=patient.objects.all()
    return render(request, "admin/view_patients.html", {'data':res})


##################          HOSPITAL

def hosp_home(request):
    return render(request, "hospital/index.html")


def hosp_view_dis(request):
    res=disease.objects.all()
    return render(request, "hospital/view_disease.html", {'data':res})

def hosp_view_profile(request):
    res=hospital.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "hospital/hosp_profile.html", {'data':res})

def hosp_view_profile_post(request):
    name=request.POST['t1']
    email=request.POST['t2']
    phone=request.POST['t3']
    place=request.POST['t4']
    post=request.POST['t5']
    pin=request.POST['t6']
    hospital.objects.filter(LOGIN_id=request.session['lid']).update(user_name=name, email=email,
            phone=phone, place=place, post=post, pin=pin)
    return HttpResponse("<script>alert('Profile updated');window.location='/hosp_view_profile#content';</script>")


def hosp_add_doctor(request):
    return render(request, "hospital/add_doctor.html")

def hosp_add_doctor_post(request):
    name=request.POST['t1']
    email=request.POST['t2']
    phone=request.POST['t3']
    qual=request.POST['t4']
    exp=request.POST['t5']
    gender=request.POST['radio']
    img=request.FILES['f1']
    d=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fs=FileSystemStorage()
    fs.save(r"D:\softwares\Project\diabetic\myapp\static\images\\" + d + ".jpg", img)
    path="/static/images/" + d + ".jpg"
    obj=doctor()
    obj.name=name
    obj.email=email
    obj.phone=phone
    obj.image=path
    obj.gender=gender
    obj.qualification=qual
    obj.experience=exp
    obj.HOSPITAL=hospital.objects.get(LOGIN_id=request.session['lid'])
    obj.save()
    return HttpResponse("<script>alert('Doctor details added');window.location='/hosp_add_doctor#content';</script>")


def hosp_view_doctors(request):
    res=doctor.objects.filter(HOSPITAL__LOGIN_id=request.session['lid'])
    return render(request, "hospital/view_doctors.html", {'data':res})

def hosp_delete_doctors(request, id):
    doctor.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted');window.location='/hosp_view_doctors#content';</script>")

def hosp_view_patients(request):
    return render(request, "hospital/view_patients.html")

def hosp_view_patients_post(request):
    name=request.POST['t1']
    res=patient.objects.filter(user_name__contains=name)
    return render(request, "hospital/view_patients.html", {'data':res, 'nm':name})

def hosp_dr_predict(request, id):
    return render(request, "hospital/dr_predict.html", {'id':id})
def hosp_dr_predict_post(request, id):
    img=request.FILES['f1']
    d = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fs = FileSystemStorage()
    fs.save(r"D:\softwares\Project\diabetic\myapp\static\images\\" + d + ".jpg", img)
    path = "/static/images/" + d + ".jpg"

    label_list=["DR", "Healthy"]
    pred=predictcnn(r"D:\softwares\Project\diabetic\myapp\static\images\\" + d + ".jpg")
    print("Folder index : ", pred)
    idx=pred[0]
    print("Prediction : ", label_list[idx])
    if str(label_list[idx]) == "Healthy":
        msg="The patient is found to be healthy."
        res="Healthy"
        descr=""
        prec=""
    else:
        msg="Traces of diabetic retinopathy found in uploaded image."
        res="Diabetic Retinopathy"
        import random

        # Assuming disease.objects.filter(disease="Diabetic Retinopathy") returns a list
        obj = disease.objects.filter(disease="Diabetic Retinopathy")

        # Shuffle the results
        random.shuffle(obj)
        # Now the results list is shuffled
        descr=obj[0].description
        prec=obj[0].precautions

    obj=results()
    obj.date=datetime.datetime.now().date()
    obj.image=path
    obj.result=res
    obj.test_type="DR test"
    obj.PATIENT_id=id
    obj.HOSPITAL=hospital.objects.get(LOGIN_id=request.session['lid'])
    obj.save()
    return render(request, "hospital/dr_predict.html", {'id': id, 'msg':msg, "res":res, "descr":descr, "prec":prec})


def hosp_pd_predict(request, id):
    return render(request, "hospital/pd_predict.html", {'id':id})
def hosp_pd_predict_post(request, id):
    img=request.FILES['f1']
    d = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fs = FileSystemStorage()
    fs.save(r"D:\softwares\Project\diabetic\myapp\static\images\\" + d + ".jpg", img)
    path = "/static/images/" + d + ".jpg"

    label_list=["No", "Yes"]
    pred=predictcnn_pd(r"D:\softwares\Project\diabetic\myapp\static\images\\" + d + ".jpg")
    print("Folder index : ", pred)
    idx=pred[0]
    print("Prediction : ", label_list[idx])
    if str(label_list[idx]) == "No":
        msg="The patient is found to be healthy."
        res="Healthy"
        descr=""
        prec=""
    else:
        msg="Traces of parkinsons disease found in uploaded image."
        res="Parkinsons Disease"
        import random
        # Assuming disease.objects.filter(disease="Diabetic Retinopathy") returns a list
        obj = disease.objects.filter(disease="Parkinsons Disease")

        # Shuffle the results
        random.shuffle(obj)
        # Now the results list is shuffled
        descr = obj[0].description
        prec = obj[0].precautions

    obj=results()
    obj.date=datetime.datetime.now().date()
    obj.image=path
    obj.result=res
    obj.test_type="PD test"
    obj.PATIENT_id=id
    obj.HOSPITAL=hospital.objects.get(LOGIN_id=request.session['lid'])
    obj.save()
    return render(request, "hospital/pd_predict.html", {'id': id, 'msg':msg, 'res':res, 'descr':descr, 'prec':prec})



def hosp_alz_predict(request, id):
    return render(request, "hospital/alz_predict.html", {'id':id})
def hosp_alz_predict_post(request, id):
    img=request.FILES['f1']
    d = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fs = FileSystemStorage()
    fs.save(r"D:\softwares\Project\diabetic\myapp\static\images\\" + d + ".jpg", img)
    path = "/static/images/" + d + ".jpg"

    label_list=["Alzheimers", "Healthy"]
    pred=predictcnn_alz(r"D:\softwares\Project\diabetic\myapp\static\images\\" + d + ".jpg")
    print("Folder index : ", pred)
    idx=pred[0]
    print("Prediction : ", label_list[idx])

    if str(label_list[idx]) == "Healthy":
        msg="The patient is found to be healthy."
        res="Healthy"
        descr=""
        prec=""
    else:
        msg="Traces of Alzheimers found in uploaded image."
        res="Alzheimers"
        import random
        # Assuming disease.objects.filter(disease="Diabetic Retinopathy") returns a list
        obj = disease.objects.filter(disease="Alzheimers")

        # Shuffle the results
        random.shuffle(obj)
        # Now the results list is shuffled
        descr = obj[0].description
        prec = obj[0].precautions
    obj=results()
    obj.date=datetime.datetime.now().date()
    obj.image=path
    obj.result=res
    obj.test_type="Alzheimers test"
    obj.PATIENT_id=id
    obj.HOSPITAL=hospital.objects.get(LOGIN_id=request.session['lid'])
    obj.save()
    return render(request, "hospital/alz_predict.html", {'id': id, 'msg':msg, "res":res, "prec":prec, "descr":descr})

def hosp_view_uploads(request):
    res=results.objects.filter(HOSPITAL__LOGIN_id=request.session['lid']).order_by("-id")
    return render(request, "hospital/view_previous uploads.html", {'data':res})

def logout(request):
    return redirect("/")



##################      PATIENT
def patient_home(request):
    return render(request, "user/index.html")

def patient_profile(request):
    res=patient.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "user/view_profile.html", {'data':res})

def patient_profile_post(request):
    name=request.POST['t1']
    email=request.POST['t2']
    phone=request.POST['t3']
    place=request.POST['t4']
    post=request.POST['t5']
    pin=request.POST['t6']
    patient.objects.filter(LOGIN_id=request.session['lid']).update(user_name=name, email=email, phone=phone, place=place, post=post, pin=pin)
    return HttpResponse("<script>alert('Profile updated');window.location='/patient_profile#content';</script>")


def patient_view_result(request):
    res=results.objects.filter(PATIENT__LOGIN_id=request.session['lid']).order_by("-id")
    return render(request, "user/view_results.html", {'data':res})

def patient_view_verified_hospital(request):
    res=hospital.objects.filter(LOGIN__usertype="hospital")
    return render(request, "user/verified_hospital.html", {'data':res})


def patient_view_doctors(request, id):
    res=doctor.objects.filter(HOSPITAL_id=id)
    return render(request, "user/view_doctors.html", {'data':res})




def patient_disease(request):
    res=disease.objects.filter()
    return render(request, "user/view_disease.html", {'data':res})