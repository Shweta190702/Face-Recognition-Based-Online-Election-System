from django.contrib.messages.api import success
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from OnlineVotingSystem import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from .models import UserProfile, Party
# from .models import Vote
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
import face_recognition
import cv2
import os
import numpy as np
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control

usr = None
adm = None


def home(request):
    return render(request, 'users/home.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        facepic = request.POST['photo']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']

        error_message = None
        success_message = None

        if User.objects.filter(username=username):
            error_message = "Username already exist! Please try some other Username"
            return render(request, 'users/signup.html', {'error': error_message})

        if User.objects.filter(email=email):
            error_message = "Email Address already exist! Please try some other Email Address"
            return render(request, 'users/signup.html', {'error': error_message})

        if pass1 != pass2:
            error_message = "Password didn't match!"
            return render(request, 'users/signup.html', {'error': error_message})

        if not username.isalnum:
            error_message = "Username must be Alpha-Numeric!"
            return render(request, 'users/signup.html', {'error': error_message})

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.userprofile.age = age
        myuser.userprofile.gender = gender
        myuser.userprofile.phone = phone
        myuser.userprofile.address = address
        myuser.userprofile.head_shot = 'profile_images/'+facepic


        success_message = "Your Account has been successfully created. We have sent you a confirmation email, please confirm your account in order to activate your account"

        # Welcome Email
        subject = "Welcome to Online Voting System"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Online Voting System!! \nThank you for visiting our website \nWe have also sent you a confermation email, please confirm your email address in order to activate your account. \n\nThanking You \nPravin Kumar Mahato"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Online Voting System"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        myuser.save()
        myuser.userprofile.save()

        return render(request, 'users/signin.html', {'success': success_message})

    return render(request, "users/signup.html")


def facedect(loc):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    path = loc
    image = cv2.imread(f'{path}')

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encodeimage = face_recognition.face_encodings(img)[0]

    if ret:
        face = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        facelocation = face_recognition.face_locations(face)
        encodesface = face_recognition.face_encodings(face, facelocation)

        match = face_recognition.compare_faces(encodeimage, encodesface)
        faceDis = face_recognition.face_distance(encodeimage, encodesface)

        matchIndex = np.argmin(faceDis)

        if match[matchIndex]:
            return True
        else:
            return False


def signin(request):
    if request.method == 'POST':
        global usr
        uname = request.POST['username']
        pass1 = request.POST['pass1']

        error_message = None
        user = authenticate(username=uname, password=pass1)
        usr = user

        if user is not None:
            if facedect(user.userprofile.head_shot.path):
                login(request, user)
                return render(request, "users/profile.html")
            else:
                error_message = "Face Doesn't Match!"
                logout(request)
                return render(request, 'users/signin.html', {'error': error_message})

        else:
            error_message = "Bad Credentials!"
            logout(request)
            return render(request, 'users/signin.html', {'error': error_message})

    return render(request, "users/signin.html")


def signout(request):
    logout(request)
    return redirect('home')


@cache_control(no_cache=True, must_revalidate=True)
def profile(request):
    if usr is not None:
        # return JsonResponse({"message": "not authenticated"})
        return render(request, 'users/profile.html')
    else:
        # return render(request, 'users/profile.html')
        return redirect('signout')


@cache_control(no_cache=True, must_revalidate=True)
def vote(request):
    # print(usr.id)
    # userModel = UserProfile
    # userObj = userModel.objects.get(user_id = usr.id)
    # if(userObj.voted):
    #     return JsonResponse({"status" : 200, "message" : "You have already voted"})

    displayparty = Party.objects.all()
    # displayvote = Vote.objects.all()

    # if request.method == 'POST':
    #     vote_party = request.POST['party']
    #     if usr is not None:
    #         myvote = Vote()
    #         myvote.user = usr
    #         myvote.party_name = vote_party
    #         myvote.save()
    #     else:
    #         print("Voting Unsuccesfull")

    return render(request, 'users/vote.html', {"Party":displayparty})


def giveVote(request):
    message = None
    if request.method == 'POST':
        if usr is not None:
            partyid = request.POST.get('selectedParty', False)
            userid = usr.userprofile.user_id
            print("userid: ",userid)
            userModel = UserProfile
            userObj = userModel.objects.get(user_id=userid)
            print(request.POST)
            if (userObj.voted):
                message = "You have already voted"
                # return JsonResponse({"status": 200, "message": "You have already voted"})
                return render(request, 'users/voted.html', {'msg': message})
            print(userObj.voted)

            # print(request.body)
            print(userid)
            print(request.POST)
            # print(request.POST['csrefmiddlewaretoken'])
            # if usr is not None:
            #     myvote = Party()
            #     partyObj = myvote.get(id=partyid)
            #     partyVotes = partyObj.vote_count
            #     partyObj.vote_count = int(partyVotes) + 1
            #     partyObj.save()
            #     #myvote.filter(id=partyid).update(votes = votes+1)
            #     return JsonResponse({"status" : 200, "message" : "You have voted successfully"})
            # else:
            #     return JsonResponse({"status" : 400, "message" : "Voting unsuccessfull"})


            partyModel = Party
            partyObj = partyModel.objects.get(id = partyid)
            # partyObj = myvote.getParty(id=partyid)
            partyVotes = partyObj.vote_count
            partyObj.vote_count = int(partyVotes) + 1
            partyObj.save()
            partyModel.objects.filter(id=partyid).update(vote_count = partyVotes+1)


            # userVoted = userObj.voted
            userObj.voted = True
            userObj.save()
            userModel.objects.filter(user_id = userid).update(voted = True)

            print(userObj)
            message = "You have voted successfully"
            # return JsonResponse({"status" : 200, "message" : "You have voted successfully"})
            return render(request, 'users/voted.html', {'msg': message})
        else:
            return redirect('logout')


def voted(request):
    return render(request, 'users/voted.html')


@cache_control(no_cache=True, must_revalidate=True)
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('signout')
    else:
        return render(request, 'activation_failed.html')


def adminSignin(request):
    global adm
    if request.method == 'POST':
        usrname = request.POST['adminUname']
        passwd = request.POST['adminPasswd']
        error_message = None
        adminauth = authenticate(username=usrname, password=passwd)
        adm = adminauth
        print(adminauth)
        if adminauth is not None:
            usrModel = User
            usrObj = usrModel.objects.get(username=usrname)
            isusrSuper = usrObj.is_superuser
            if isusrSuper == True:
                login(request, adminauth)
                return redirect('adminPanel')
            else:
                error_message = "Bad Credentials!"
                logout(request)
                return render(request, 'adminTemplate/login.html', {'error': error_message})
        else:
            error_message = "Bad Credentials!"
            logout(request)
            return render(request, 'adminTemplate/login.html', {'error': error_message})

    return render(request, "adminTemplate/login.html")


def adminPanel(request):
    vc = 0
    if adm is not None:
        displayparty = Party.objects.all()
        for i in displayparty:
            vc = vc + i.vote_count
        print(vc)
        return render(request, 'adminTemplate/index.html', {"totalvotecount":vc})
    else:
        return redirect('adminlogout')


def adminlogout(request):
    adm = None
    logout(request)
    return redirect('adminSignin')


def adminTable(request):
    if adm is not None:
        displayparty = Party.objects.all()
        return render(request, 'adminTemplate/tables.html', {"Party":displayparty})
    else:
        return redirect('adminlogout')