"""
URL configuration for diabetic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.logg),
    path('logg_post', views.logg_post),
    path('reg/<i>', views.reg),
    path('reg_post/<i>', views.reg_post),
    path('admin_home', views.admin_home),
    path('admin_add_dis', views.admin_add_dis),
    path('admin_add_dis_post', views.admin_add_dis_post),
    path('admin_view_dis', views.admin_view_dis),
    path('admin_delete_dis/<id>', views.admin_delete_dis),
    path('admin_verify_hospital', views.admin_verify_hospital),
    path('admin_approve_hospital/<id>', views.admin_approve_hospital),
    path('admin_reject_hospital/<id>', views.admin_reject_hospital),
    path('admin_view_verified_hospital', views.admin_view_verified_hospital),
    path('admin_view_patient', views.admin_view_patient),


    path('hosp_home', views.hosp_home),
    path('hosp_view_dis', views.hosp_view_dis),
    path('hosp_view_profile', views.hosp_view_profile),
    path('hosp_view_profile_post', views.hosp_view_profile_post),
    path('hosp_add_doctor', views.hosp_add_doctor),
    path('hosp_add_doctor_post', views.hosp_add_doctor_post),
    path('hosp_view_doctors', views.hosp_view_doctors),
    path('hosp_delete_doctors/<id>', views.hosp_delete_doctors),
    path('hosp_view_patients', views.hosp_view_patients),
    path('hosp_view_patients_post', views.hosp_view_patients_post),
    path('hosp_dr_predict/<id>', views.hosp_dr_predict),
    path('hosp_dr_predict_post/<id>', views.hosp_dr_predict_post),
    path('hosp_alz_predict/<id>', views.hosp_alz_predict),
    path('hosp_alz_predict_post/<id>', views.hosp_alz_predict_post),
    path('hosp_pd_predict/<id>', views.hosp_pd_predict),
    path('hosp_pd_predict_post/<id>', views.hosp_pd_predict_post),
    path('hosp_view_uploads', views.hosp_view_uploads),
    path('logout', views.logout),


    path('patient_home', views.patient_home),
    path('patient_disease', views.patient_disease),
    path('patient_profile', views.patient_profile),
    path('patient_profile_post', views.patient_profile_post),
    path('patient_view_result', views.patient_view_result),
    path('patient_view_verified_hospital', views.patient_view_verified_hospital),
    path('patient_view_doctors/<id>', views.patient_view_doctors),


]
