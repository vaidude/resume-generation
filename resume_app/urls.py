
from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),  
    path('home/',views.home,name='home'),
    path('reg/',views.reg,name='reg'),
    
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('pprofile/',views.pprofile,name='pprofile'),
    path('update/',views.update,name='update'),
    path('delete_user/<int:uid>/',views.delete_user,name='delete_user'),
    path('logout/',views.logout,name='logout'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('userlist/',views.userlist,name='userlist'),
    path('deleteusr_admin/<int:uid>/',views.deleteusr_admin,name='deleteusr_admin'),
    path('addjob/',views.addjob,name='addjob'),
    path('job_list/', views.job_list, name='job_list'),
    path('view_job/',views.view_job,name='view_job'),
    path('edit_job/<int:job_id>/',views.edit_job,name='edit_job'),
    path('delete_job/<int:job_id>/',views.delete_job,name='delete_job'),
    path('userfeedback/',views.userfeedback,name='userfeedback'),
    path('feedbacklist/',views.feedbacklist,name='feedbacklist'),
    path('delete_feedback/<int:feedback_id>/',views.delete_feedback,name='delete_feedback'),
    path('reg_job/',views.reg_job,name='reg_job'),
    path('jobprovider_login/',views.jobprovider_login,name='jobprovider_login'),
    path('job_provider/',views.job_provider1,name='job_provider'),
    path('jobprovider_list/',views.jobprovider_list,name='jobprovider_list'),
    path('delete_jobprovider/<int:id>/',views.delete_jobprovider,name='delete_jobprovider'),
    path('create-order/', views.create_order, name='create-order'),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('transactionlist/',views.transactionlist,name='transactionlist'),
    path('certificateupload/',views.certificateupload,name='certificateupload'),
    
    
    path('resume/',views.resume,name='resume'),
    path('resumelist/', views.resumelist, name='resumelist'),
    path('apply/<int:job_id>/',views.apply,name='apply'),
    path('generate/', views.generate_question, name='generate_question'),
    path('quiz/', views.take_quiz, name='take_quiz'),
    path('create_exam/', views.create_exam, name='create_exam'),
    path('take_exam/<str:unique_link>/', views.take_exam, name='take_exam'),
    path('viewresults/', views.viewresults, name='viewresults'),
    path('applications/', views.applicationlist, name='applications'),
    path('viewexams/', views.view_exams, name='viewexams'),
    path('delete-exam/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('view_applicants/', views.view_applicants, name='view_applicants'),
    path('add_placement/', views.add_placement, name='add_placement'),
    
 
]