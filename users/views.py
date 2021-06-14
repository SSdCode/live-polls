from users.models import Question, Choice
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.urls import reverse
from django.contrib.auth  import authenticate,  login as auth_login, logout



# superuser - admin - admin
# user - sdcode - 1234

# Create your views here.
def index(request):
    return render(request,'users/index.html')

def about(request):
    return render(request,'users/about.html')

def contact(request):
    return render(request,'users/contact.html')
    

def login(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user = authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("users:index")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("users:login")   
    return render(request, 'users/login.html')

def hlogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("users:index")

def signup(request):
    if request.method=="POST":
        # Get the post parameters
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        gender=request.POST['gender']
        email =request.POST['email']
        pass1 =request.POST['pass1']
        pass2 =request.POST['pass2']

        # check for errorneous input
        # if len(username)>10:
        #     messages.debug(request, " Your user name must be under 10 characters")
        #     return redirect('users:signup')

        if not username.isalnum():
            messages.warning(request, " User name should only contain letters and numbers")
            return redirect('users:signup')

        if (pass1!= pass2):
            messages.warning(request, " Passwords do not match")
            return redirect('users:signup')


        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.gender=gender
        myuser.save()
        messages.success(request, " Your account has been successfully created. Login Now.")
        return redirect('users:index')

    else:
        return render(request,'users/signup.html')

def postpoll(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user=request.user
            question_text = request.POST.get('question_text')
            # livestatus = request.POST.get('livestatus')
            livestatus = request.POST.get('livestatus', '') == 'on'
            publicstatus = request.POST.get('publicstatus')
            
            option1 = request.POST.get('option1')
            option2 = request.POST.get('option2')
            option3 = request.POST.get('option3')
            option4 = request.POST.get('option4')

    
            poll=Question(question_text= question_text, livestatus=livestatus, publicstatus=publicstatus, user=user)
            poll.save()
            pollchoice1=Choice(question = poll, choice_text = option1, votes=0)
            pollchoice1.save()
            pollchoice2=Choice(question = poll, choice_text = option2, votes=0)
            pollchoice2.save()
            pollchoice3=Choice(question = poll, choice_text = option3, votes=0)
            pollchoice3.save()
            pollchoice4=Choice(question = poll, choice_text = option4, votes=0)
            pollchoice4.save()
            messages.success(request, "Your Poll has been published successfully")
        else:
            messages.warning(request, "Login First")
    return redirect('users:index')

def mypolls(request):
    if request.user.is_authenticated:
        latest_question_list = Question.objects.order_by('-timestamp')[:5]
        context = {'latest_question_list': latest_question_list}
        return render(request, 'users/mypolls.html', context)
    else:
            messages.warning(request, "Login First")
    return redirect('users:index')

def publicpolls(request):
    # latest_question_list = Question.objects.order_by('-timestamp')[:5]
    latest_question_list = Question.objects.all()
    context = {'latest_question_list': latest_question_list}
    return render(request, 'users/publicpolls.html', context)

# Show specific question and choices
def details(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'users/details.html', {'question': question})

# # Get question and display results
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'users/results.html', {'question': question})

# Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    total = 0
    for choice in question.choice_set.all():
        total += choice.votes
    
    listchoice = []
    for choice in question.choice_set.all():
        listchoice.append(choice.choice_text)


    if total != 0:
        list1 = []
        for choice in question.choice_set.all():
            list1.append(((choice.votes)*100)/total)
    else:
        list1 = [0,0,0,0]
    return render(request, 'users/results.html', {'question': question, 'list1': list1, 'listchoice': listchoice})

# Vote for a question choice
def vote(request, question_id):
    if request.user.is_authenticated:
        # print(request.POST['choice'])
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'users/index.html', {
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('users:results', args=(question.sno,)))
    else:
        messages.warning(request, "Login First")
    return redirect('users:index')

