from django.shortcuts import render,HttpResponse,redirect,get_object_or_404

from . import models



# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    placements = models.Placement.objects.all()
    return render(request, 'home.html',{'placements':placements})

def reg(request):
    if request.method=='POST':
        image=request.POST.get('name')
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        age=request.POST.get('age')
        phonenumber=request.POST.get('phonenumber')
        if models.Reg.objects.filter(email=email).exists():
            alert="<script>alert('email already exists');window.location.href='/reg/';</script>"
            return HttpResponse(alert)
        else:
            usr=models.Reg(name=name,email=email,password=password,dob=dob,age=age,phonenumber=phonenumber,gender=gender).save()
            return redirect('index')
    else:
        return render(request,'reg.html')
def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        print(email)
        password=request.POST.get('password')
        print(password)

        try:
            usr=models.Reg.objects.get(email=email, password=password)
            if usr.status == "Success ":
                request.session['email']=email
                alert="<script>alert('Login Successful');window.location.href='/home/';</script>"
                return HttpResponse(alert)
            request.session['ail']=email
            alert="<script>alert('please subscribe to complete registration');window.location.href='/profile/';</script>"
            return HttpResponse(alert)
        except Exception as e:
            print(e)
            alert="<script>alert('invalid email or password');window.location.href='/login/';</script>"
            return HttpResponse(alert)
    else:
        return render(request,'login.html')
    
def profile(request):
    if 'ail' in request.session:
        email=request.session['ail']
        user=models.Reg.objects.get(email=email)
        return render(request,'profile.html',{'user':user})
    else:
        return redirect('login')
def pprofile(request):
    if 'email' in request.session:
        email=request.session['email']
        user=models.Reg.objects.get(email=email)
        return render(request,'pprofile.html',{'user':user})
    else:
        return redirect('login')
    
# def update(request):
#     email=request.session['email']
#     user=models.Reg.objects.get(email=email)
#     print(user.name)
#     if request.method=='POST':
#             name=request.POST.get('name')
#             phonenumber=request.POST.get('phonenumber')
#             password=request.POST.get('password')
#             dob=request.POST.get('dob')
#             age=request.POST.get('age')
#             gender=request.POST.get('gender')
#             image=request.FILES.get('image')

#             user.name=name
#             user.phonenumber=phonenumber
#             user.password=password
#             user.dob=dob
#             user.age=age
#             user.gender=gender
#             if image:
#                 user.image=image
#             user.save()
#             print('success')
#             return redirect('pprofile')
            
            
#     else:
#         return render(request,'update.html',{'user':user})
#         return redirect('login')
from django.shortcuts import render, redirect


def update(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    
    try:
        user = models.Reg.objects.get(email=email)
    except models.Reg.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        user.name = request.POST.get('name', user.name)
        user.phonenumber = request.POST.get('phonenumber', user.phonenumber)
        password = request.POST.get('password',user.password)# Hash password properly
        user.dob = request.POST.get('dob', user.dob)
        user.age = request.POST.get('age', user.age)
        user.gender = request.POST.get('gender', user.gender)
        if request.FILES.get('image'):
            user.image = request.FILES.get('image')
        
        user.save()
        return redirect('pprofile')
    
    return render(request, 'update.html', {'user': user})
def delete_user(request,uid):
   user=models.Reg.objects.get (id=uid) 
   user.delete()
   return redirect('index')  

def logout(request):
    request.session.flush()
    return redirect('index')

def admin_dashboard(request):
    # Get the count of job postings and registered users
    job_postings_count = models.Addjob.objects.count()
    registered_users_count = models.Reg.objects.count()

    # Pass the counts to the template
    return render(request, 'admin.html', {
        'job_postings_count': job_postings_count,
        'registered_users_count': registered_users_count,
    })
def adminlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if email=='admin@gmail.com' and password=='admin':
            request.session['email']=email
            alert="<script>alert('Login successful'); window.location.href='/admin_dashboard/'; </script>"
            return HttpResponse(alert)
        else:
            alert="<script>alert('Invalid email or password'); window.location.href='/adminlogin/'; </script>"
            return HttpResponse(alert)
                    
    else:
        return render(request,'adminlogin.html')
    
def userlist(request):
    user=models.Reg.objects.all()
    return render(request,'userlist.html',{'user':user})

def deleteusr_admin(request,uid):
    user=models.Reg.objects.get (id=uid) 
    user.delete()
    return redirect('admin_dashboard')  

from datetime import datetime

def addjob(request):
    if request.method == 'POST':
        companyName = request.POST.get('companyName')
        companyAddress = request.POST.get('companyAddress')
        jobTitle = request.POST.get('jobTitle')
        jobDescription = request.POST.get('jobDescription')
        jobResponsibilities = request.POST.get('jobResponsibilities')
        jobQualifications = request.POST.get('jobQualifications')
        jobType = request.POST.get('jobType')
        salaryRange = request.POST.get('salaryRange')
        contactEmail = request.POST.get('contactEmail')
        applicationDeadline_str = request.POST.get('applicationDeadline')
        try:
            applicationDeadline = datetime.strptime(applicationDeadline_str, '%Y-%m-%d').date() 
        except ValueError:
            return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")
        usr = models.Addjob(
                companyName=companyName,
                companyAddress=companyAddress,
                jobTitle=jobTitle,
                jobDescription=jobDescription,
                jobResponsibilities=jobResponsibilities,
                jobQualifications=jobQualifications,
                salaryRange=salaryRange,
                contactEmail=contactEmail,
                applicationDeadline=applicationDeadline
        )
        usr.save()
        return redirect('admin_dashboard')
    else:
        return render(request, 'addjob.html')

def job_list(request):
    search_query = request.GET.get('search', '')
    salary_range = request.GET.get('salary_range', '')
    qualification = request.GET.get('qualification', '')
    jobs = models.Addjob.objects.all()

    if search_query:
        jobs = jobs.filter(jobTitle__icontains=search_query)
    
    if salary_range:
        jobs = jobs.filter(salaryRange__icontains=salary_range)

    if qualification:
        jobs = jobs.filter(jobQualifications__icontains=qualification)

    return render(request, 'job_list.html', {'jobs': jobs})

def view_job(request):
    jobs=models.Addjob.objects.all()
    return render(request,'view_job.html',{'jobs':jobs})
def view_job(request):
    search = request.GET.get('search', '')
    jobs = models.Addjob.objects.all()

    if search:
        jobs = jobs.filter(jobTitle__icontains=search)

    return render(request, 'view_job.html', {'jobs': jobs})

def edit_job(request, job_id):
    job = models.Addjob.objects.get(id=job_id)
    if request.method == 'POST':
        # Update job details from the form data
        job.companyName = request.POST['companyName']
        job.companyAddress = request.POST['companyAddress']
        job.jobTitle = request.POST['jobTitle']
        job.jobDescription = request.POST['jobDescription']
        job.jobResponsibilities = request.POST['jobResponsibilities']
        job.jobQualifications = request.POST['jobQualifications']
        job.salaryRange = request.POST['salaryRange']
        job.contactEmail = request.POST['contactEmail']
        job.applicationDeadline = request.POST['applicationDeadline']
        job.save()

        return redirect('view_job')

    return render(request, 'edit_job.html', {'job': job})

def delete_job(request,job_id):
    job=models.Addjob.objects.get (id=job_id) 
    job.delete()
    return redirect('view_job')  

def userfeedback(request):
    semail = request.session.get('email')  # Safely get session email
    try:
        user = models.Reg.objects.get(email=semail)
    except models.Reg.DoesNotExist:
        user = None  # Handle case where the user is not found

    

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')
        rating=request.POST.get('rating')
        


        try:
            models.Feedback(
                name=name,
                email=email,
                feedback=feedback,
                rating=rating,
            ).save()

            alert = "<script>alert('Feedback added successfully!'); window.location.href='/userfeedback/'; </script>"
            return HttpResponse(alert)

        except Exception as e:
            print(e)
    else:
        # Pass the current date to the template
        return render(request, 'userfeedback.html', {'user': user})
def feedbacklist(request):
    feedbacks=models.Feedback.objects.all()
    return render(request,'feedbacklist.html',{'feedbacks':feedbacks})

def delete_feedback(request, feedback_id):
        feedback = models.Feedback.objects.get(id=feedback_id)
        feedback.delete()
        return redirect('feedbacklist') 

def reg_job(request):
    if request.method=='POST':
        companyName=request.POST.get('companyName')
        contactPerson=request.POST.get('contactPerson')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        password=request.POST.get('password')
        confirmPassword=request.POST.get('confirmPassword')
        if models.job_provider.objects.filter(email=email).exists():
            alert="<script>alert('email already exists');window.location.href='/reg_job/';</script>"
            return HttpResponse(alert)
        else:
            usr=models.job_provider(companyName=companyName,contactPerson=contactPerson,email=email,phone=phone,address=address,password=password,confirmPassword=confirmPassword).save()
            return redirect('jobprovider_login')
    else:
        return render(request,'reg_job.html')

def jobprovider_login(request):        
    if request.method=='POST':
        loginEmail=request.POST.get('loginEmail')
        loginPassword=request.POST.get('loginPassword')
        try:
            print(loginEmail)
            print(loginPassword)
            usr= models.job_provider.objects.get(email=loginEmail,password=loginPassword)
            request.session['email']=usr.email
            request.session['id']=usr.id
            alert="<script>alert('Login Successful');window.location.href='/job_provider/';</script>"
            return HttpResponse(alert)
        except Exception as e:
            print(e)
            alert="<script>alert('invalid email or password');window.location.href='/jobprovider_login/';</script>"
            return HttpResponse(alert)
    else:
        return render(request,'jobprovider_login.html')

def job_provider1(request):
    return render(request,'job_provider.html')

# def jobprovider_list(request):
#     providers = models.job_provider.objects.all().values('companyName', 'contactPerson', 'email', 'phone', 'address') # Select only needed fields
#     return render(request,'jobprovider_list.html',{'providers':providers})



def jobprovider_list(request):
    providers = models.job_provider.objects.all()  
    return render(request, 'jobprovider_list.html', {'providers': providers})



def delete_jobprovider(request, id):
    try:
        provider = models.job_provider.objects.get(id=id)
        provider.delete()
    except models.job_provider.DoesNotExist:
        # Handle case if provider does not exist (optional: show a message)
        pass
    return redirect('jobprovider_list')




import json
import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Initialize Razorpay client
clien = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create Razorpay Order
@csrf_exempt
def create_order(request):
    if request.method == "POST":
        try:
            # Create order for ₹200
            data = json.loads(request.body)
            amount = data['amount'] * 100  # Convert to paise
            payment_order = clien.order.create(dict(
                amount=amount,
                currency='INR'
            ))
            return JsonResponse({
                'order_id': payment_order['id'],
                'amount': amount
            })
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Payment success view

@csrf_exempt
def payment_success(request):
    email = request.session['ail']
    print(email)
    try:
        juser = models.Reg.objects.get(email=email)
        print("User fetched:", juser)
        juser.status = 'Success '
        juser.save()
        lop=juser.status
        print(lop)
        if request.method == "POST":
            data = json.loads(request.body)
            
            # Verify the payment signature from Razorpay
            try:
                clien.utility.verify_payment_signature({
                    'razorpay_order_id': data['razorpay_order_id'],
                    'razorpay_payment_id': data['razorpay_payment_id'],
                    'razorpay_signature': data['razorpay_signature']
                })
                
                # Log the order and payment ID for debugging
                print("Order ID:", data['razorpay_order_id'])
                print("Payment ID:", data['razorpay_payment_id'])
                
                # Save the transaction details to the database
                models.Transaction(
                    user=juser,
                    order_id=data['razorpay_order_id'],
                    payment_id=data['razorpay_payment_id'],
                    amount=200,
                    status='success'
                ).save()
                return JsonResponse({'status': 'success'})
            
            except Exception as e:
                print("Error during payment verification:", e)
                return JsonResponse({'status': 'failed', 'error': str(e)})
        
    except models.Reg.DoesNotExist:
        print(f"User with email {email} not found.")
        return JsonResponse({'status': 'failed', 'error': 'User not found'})
    
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

from .models import Transaction
def transactionlist(request):
    transactions = models.Transaction.objects.all()  # Fetch all transactions
    return render(request, 'transactionlist.html', {'transactions': transactions})



from django.shortcuts import render
from .models import Certificate, Reg

def certificateupload(request):
    message = None
    uploaded_certificates = []  # List to store user's certificates

    if request.method == 'POST':
        # Get the logged-in user based on the session email
        email = request.session.get('email')
        
        if email:
            try:
                user = Reg.objects.get(email=email)  # Get the user based on email
            except Reg.DoesNotExist:
                message = "User not found."
                return render(request, 'certificateupload.html', {'message': message})
            
            certificate_image = request.FILES.get('certificate_images')
            if certificate_image:
                Certificate.objects.create(image=certificate_image, user=user)
                message = "Certificate uploaded successfully."
            
            # Retrieve all certificates uploaded by the user
            uploaded_certificates = Certificate.objects.filter(user=user)

    return render(request, 'certificateupload.html', {
        'message': message,
        'uploaded_certificates': uploaded_certificates
    })


from django.shortcuts import render
from django.http import HttpResponse
from .models import Resume

def resume(request):
    if request.method == 'POST':
        # Retrieving form data safely
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        location = request.POST.get('location', '')
        objective = request.POST.get('objective', '')

        job_title_1 = request.POST.get('job_title_1', None)
        company_1 = request.POST.get('company_1', None)
        dates_1 = request.POST.get('dates_1', None)
        responsibilities_1 = request.POST.get('responsibilities_1', None)

        job_title_2 = request.POST.get('job_title_2', None)
        company_2 = request.POST.get('company_2', None)
        dates_2 = request.POST.get('dates_2', None)
        responsibilities_2 = request.POST.get('responsibilities_2', None)

        degree = request.POST.get('degree', '')
        university = request.POST.get('university', '')
        graduation_date = request.POST.get('graduation_date', None)

        skills = request.POST.get('skills', '')
        references = request.POST.get('references', None)

        # Creating and saving the resume
        try:
            resume = Resume.objects.create(
                email=email,
                phone=phone,
                location=location,
                objective=objective,
                job_title_1=job_title_1,
                company_1=company_1,
                dates_1=dates_1 if dates_1 else None,  # Handle empty dates
                responsibilities_1=responsibilities_1,
                job_title_2=job_title_2,
                company_2=company_2,
                dates_2=dates_2 if dates_2 else None,
                responsibilities_2=responsibilities_2,
                degree=degree,
                university=university,
                graduation_date=graduation_date if graduation_date else None,
                skills=skills,
                references=references
            )
            resume.save()
            return render(request, 'resumeview.html', {'resume': resume})
            return HttpResponse("Resume submitted successfully!")  # Success response
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=400)  # Handle errors
        
    return render(request, 'resume.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .models import JobApplication, Addjob, Reg

def apply(request, job_id):
    if "email" not in request.session:
        messages.warning(request, "You need to log in to apply for jobs.")
        return redirect("login")
    
    user_email = request.session.get("email")
    user = get_object_or_404(Reg, email=user_email)
    job = get_object_or_404(Addjob, id=job_id)
    
    if request.method == "POST":
        cover_letter = request.POST.get("cover_letter")
        
        # Check if user has already applied
        if JobApplication.objects.filter(user=user, job=job).exists():
            messages.warning(request, "You have already applied for this job.")
            return redirect('job_list')
        # Create job application
        JobApplication.objects.create(user=user, job=job, cover_letter=cover_letter)
        messages.success(request, "Your application has been submitted successfully.")
        
        return redirect("job_list")  # Ensure "job_list" exists in urls.py
    
    context = {"job": job, "user": user}
    return render(request, "apply.html", context)

def resumelist(request):
    resumes = Resume.objects.all()  # Fetch all resumes
    return render(request, 'resumelist.html', {'resumes': resumes})

def applicationlist(request):
    applications=JobApplication.objects.all() # Fetch all applications
    return render(request, 'applicationlist.html', {'applications':applications})

# from .models import Quiz
# import openai

# # Set your OpenAI API key
# openai.api_key = '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'

# def generate_question(request):
#     if request.method == "POST":
#         topic = request.POST.get("topic", "general knowledge")
#         prompt = f"Please generate exactly 10 multiple-choice questions that are directly related to the topic '{topic}'. Each question should have 4 options (A, B, C, D), with one correct answer. After each question, indicate the correct answer in this format: 'Correct answer: <option>'. Important: Do not generate more than 10 questions. If you generate more than 10, only provide the first 10 questions. Each question must relate specifically to {topic}. Separate each question with a blank line."
        
#         try:
#             # Clear existing questions in the Quiz model
#             Quiz.objects.all().delete()

#             # Generate new questions using OpenAI API
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt},
#                 ],
#                 max_tokens=1000,
#             )
#             content = response["choices"][0]["message"]["content"].strip()
#             questions = content.split("\n\n")[:10]  # Ensure only the first 10 questions are taken
            
#             # Process and save exactly 10 questions
#             for q in questions:
#                 lines = q.split("\n")
#                 if len(lines) < 6:  # Ensure question has question text, 4 options, and correct answer
#                     continue
                
#                 question = lines[0].strip()
#                 options = [line.split(") ", 1)[-1].strip() for line in lines[1:5]]
#                 correct_option_text = next((line for line in lines if "Correct answer:" in line), None)
                
#                 if not correct_option_text:
#                     continue  # Skip if no correct answer is provided
                
#                 correct_letter = correct_option_text.split(":")[-1].strip().upper()
#                 correct_option = {"A": 1, "B": 2, "C": 3, "D": 4}.get(correct_letter)

#                 if correct_option is None:
#                     continue  # Skip invalid questions

#                 # Save the question to the Quiz model
#                 Quiz.objects.create(
#                     question=question,
#                     option1=options[0],
#                     option2=options[1],
#                     option3=options[2],
#                     option4=options[3],
#                     correct_option=correct_option,
#                 )
            
#             # Redirect to the quiz page after saving exactly 10 questions
#             return redirect("take_quiz")
        
#         except Exception as e:
#             return render(request, "generate_question.html", {"error": str(e)})
    
#     return render(request, "generate_question.html")

# def take_quiz(request):
#     quizzes = Quiz.objects.all()
#     if request.method == "POST":
#         score = 0
#         total_questions = quizzes.count()
        
#         # Get user email from session
#         user_email = request.session.get('email')
#         user=
        
#         # Calculate score
#         for quiz in quizzes:
#             selected = request.POST.get(f"q{quiz.id}")
#             if selected and int(selected) == quiz.correct_option:
#                 score += 1
                
#         # Determine rating
#         rating = "Excellent" if score > total_questions * 0.8 else "Good" if score > total_questions * 0.5 else "Needs Improvement"
        
#         # Save result to the database if we have user email
#         if user_email:
#             models.QuizResult.objects.create(
#                 email=user_email,
#                 score=score,
#                 total_questions=total_questions,
#                 rating=rating
#             )
        
#         # Render results before deleting quiz questions
#         result_response = render(request, "result.html", {
#             "score": score,
#             "total": total_questions,
#             "rating": rating
#         })
        
#         # Delete all quiz questions after calculating results
#         Quiz.objects.all().delete()
        
#         return result_response
    
#     return render(request, "take_quiz.html", {"quizzes": quizzes})

from django.shortcuts import render, redirect
from .models import Quiz
from groq import Groq

client = Groq(api_key="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")

def generate_question(request):
    if request.method == "POST":
        topic = request.POST.get("topic", "general knowledge")
        prompt = f"Generate exactly 10 multiple-choice questions on '{topic}'. Each question must have 4 options (A, B, C, D) and one correct answer. Format each as: question\nA) option\nB) option\nC) option\nD) option\nCorrect answer: <letter>. Separate questions with a blank line. Do not exceed 10 questions."
        
        try:
            Quiz.objects.all().delete()

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            
            questions = content.split("\n\n")[:10]
            
            for q in questions:
                lines = q.strip().split("\n")
                if len(lines) < 6:
                    continue
                
                question = lines[0].strip()
                options = [line.split(") ", 1)[-1].strip() for line in lines[1:5]]
                correct_option_text = next((line for line in lines if "Correct answer:" in line), None)
                
                if not correct_option_text:
                    continue
                
                correct_letter = correct_option_text.split(":")[-1].strip().upper()
                correct_option = {"A": 1, "B": 2, "C": 3, "D": 4}.get(correct_letter)

                if correct_option is None:
                    continue

                Quiz.objects.create(
                    question=question,
                    option1=options[0],
                    option2=options[1],
                    option3=options[2],
                    option4=options[3],
                    correct_option=correct_option,
                )
            
            if not Quiz.objects.exists():
                return render(request, "generate_question.html", {"error": "No valid questions generated"})
                
            return redirect("take_quiz")
        
        except Exception as e:
            return render(request, "generate_question.html", {"error": str(e)})
    
    return render(request, "generate_question.html")

def take_quiz(request):
    quizzes = Quiz.objects.all()
    if request.method == "POST":
        score = 0
        total_questions = quizzes.count()
        email=request.session['email']
        user=models.Reg.objects.get(email=email)
        user_email = request.session['email']
        
        for quiz in quizzes:
            selected = request.POST.get(f"q{quiz.id}")
            if selected and int(selected) == quiz.correct_option:
                score += 1
                
        rating = "Excellent" if score > total_questions * 0.8 else "Good" if score > total_questions * 0.5 else "Needs Improvement"
        
        if user:
            models.QuizResult.objects.create(
                user=user,
                score=score,
                total_questions=total_questions,
                rating=rating
            )
        
        result_response = render(request, "result.html", {
            "score": score,
            "total": total_questions,
            "rating": rating
        })
        
        Quiz.objects.all().delete()
        
        return result_response
    
    return render(request, "take_quiz.html", {"quizzes": quizzes})


from django.shortcuts import render, redirect
from django.http import Http404
from .models import Exam, ExamQuestion, ExamResult, job_provider
from groq import Groq
import uuid

client = Groq(api_key="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")

def create_exam(request):
    if request.method == "POST":
        job_provider_id = request.session.get('id')
        if not job_provider_id:
            return redirect('login')  # Add your login URL

        job_prov = job_provider.objects.get(id=job_provider_id)
        title = request.POST.get("title")
        topic = request.POST.get("topic")
        
        prompt = f"Generate exactly 10 multiple-choice questions on '{topic}'. Each question must have 4 options (A, B, C, D) and one correct answer. Format each as: question\nA) option\nB) option\nC) option\nD) option\nCorrect answer: <letter>. Separate questions with a blank line. Do not exceed 10 questions."
        
        try:
            unique_link = str(uuid.uuid4())[:8]
            exam = Exam.objects.create(
                job_provider=job_prov,
                title=title,
                topic=topic,
                unique_link=unique_link
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            questions = content.split("\n\n")[:10]
            
            for q in questions:
                lines = q.strip().split("\n")
                if len(lines) < 6:
                    continue
                
                question = lines[0].strip()
                options = [line.split(") ", 1)[-1].strip() for line in lines[1:5]]
                correct_option_text = next((line for line in lines if "Correct answer:" in line), None)
                
                if not correct_option_text:
                    continue
                
                correct_letter = correct_option_text.split(":")[-1].strip().upper()
                correct_option = {"A": 1, "B": 2, "C": 3, "D": 4}.get(correct_letter)

                if correct_option is None:
                    continue

                ExamQuestion.objects.create(
                    exam=exam,
                    question=question,
                    option1=options[0],
                    option2=options[1],
                    option3=options[2],
                    option4=options[3],
                    correct_option=correct_option,
                )
            
            if not ExamQuestion.objects.filter(exam=exam).exists():
                exam.delete()
                return render(request, "create_exam.html", {"error": "No valid questions generated"})
                
            return render(request, "exam_created.html", {"link": f"/take_exam/{exam.unique_link}/"})
        
        except Exception as e:
            return render(request, "create_exam.html", {"error": str(e)})
    
    return render(request, "create_exam.html")

def take_exam(request, unique_link):
    try:
        exam = Exam.objects.get(unique_link=unique_link)
    except Exam.DoesNotExist:
        raise Http404("Exam not found")

    questions = ExamQuestion.objects.filter(exam=exam)
    
    if request.method == "POST":
        score = 0
        total_questions = questions.count()
        user_email = request.POST.get("email")
        
        for question in questions:
            selected = request.POST.get(f"q{question.id}")
            if selected and int(selected) == question.correct_option:
                score += 1
                
        rating = "Excellent" if score > total_questions * 0.8 else "Good" if score > total_questions * 0.5 else "Needs Improvement"
        
        ExamResult.objects.create(
            exam=exam,
            user_email=user_email,
            score=score,
            total_questions=total_questions,
            rating=rating
        )
        
        return render(request, "exam_result.html", {
            "score": score,
            "total": total_questions,
            "rating": rating
        })
    
    return render(request, "take_exam.html", {"exam": exam, "questions": questions})

def viewresults(request):
    results=ExamResult.objects.all()
    return render(request, "viewresults.html", {"results": results})

def view_exams(request):
    email = request.session.get('email')  # Get email from session
    exams = Exam.objects.filter(job_provider__email=email)  # Filter by job provider email
    return render(request, "viewexams.html", {"exams": exams})

def delete_exam(request,exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
        exam.delete()
        return redirect("viewexams")
    except Exam.DoesNotExist:
        return redirect("viewexams")
from django.core.mail import send_mail
from django.shortcuts import render

def view_applicants(request):
    try:
        job_pro = job_provider.objects.get(email=request.session['email'])
        applicants = JobApplication.objects.filter(job__companyName=job_pro.companyName)
    except (job_provider.DoesNotExist, KeyError):
        return render(request, 'applicants.html', {'error': 'Login required'})

    exam_link = request.session.get('exam_link', '')

    if request.method == 'POST':
        if 'save_link' in request.POST:
            exam_link = request.POST.get('exam_link', '')
            request.session['exam_link'] = exam_link
        elif 'applicant_id' in request.POST:
            applicant_id = request.POST.get('applicant_id')
            print(f"Applicant ID from form: {applicant_id}")  # Debug
            try:
                applicant = JobApplication.objects.get(id=applicant_id)
                email = applicant.user.email  # Assumes Reg has email field
                print(f"Sending to: {email}")
                if exam_link:
                    send_mail(
                        'Exam Link',
                        f'Here is your exam link: {exam_link}',
                        'newgrapes2025@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                    print('Email sent successfully')
                else:
                    return render(request, 'applicants.html', {'applicants': applicants, 'error': 'No exam link provided'})
            except JobApplication.DoesNotExist:
                print(f"No JobApplication found for ID: {applicant_id}")
                return render(request, 'applicants.html', {'applicants': applicants, 'error': 'Applicant not found'})
            except Exception as e:
                print(f"Error: {e}")
                return render(request, 'applicants.html', {'applicants': applicants, 'error': str(e)})

    return render(request, 'applicants.html', {'applicants': applicants, 'exam_link': exam_link})


def add_placement(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        job_id = request.POST.get('job')
        user = Reg.objects.get(id=user_id)
        job = Addjob.objects.get(id=job_id)
        models.Placement.objects.create(
            user=user,
            job=job,
        )
        return redirect('job_provider')
    users = Reg.objects.all()
    jobs = Addjob.objects.all()
    return render(request, 'add_placement.html', {'users': users, 'jobs': jobs})