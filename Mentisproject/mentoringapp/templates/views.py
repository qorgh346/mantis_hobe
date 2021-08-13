from django import forms
from django.contrib.auth.backends import RemoteUserBackend
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from mentoringapp.models import FavouriteLecture, Mentor_info, MyLecture, Lecture
from myapp.models import User_info, Menti_info, Cash, Payment
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.utils import timezone

# Create your views here.

def index(request):
    data = {}
    login = request.session.get('user')
    if login:
        user = User_info.objects.get(user_id=login)
        data['user'] = user
    else:
        data['login'] = 1
    return render(request, "index.html", data)

def mypage(request):
    data = {}
    user_temp = request.session.get('user') # 로그인 성공 시 session 값은 user에 저장됨
    print(user_temp)
    user = User_info.objects.get(user_id=user_temp) 
    print(user.pk)
    menti =  Menti_info.objects.get(user_info_id = user.pk)
    print(menti)
    fav = FavouriteLecture.objects.filter(user_id=menti.pk)
    print(fav)
   
    data['user'] = user
    data['favLec'] = fav    
    #print(favLecture[1].user_id)
    return render(request,"mypage.html",data)



def login(request):
    data = {}
    data['login'] = 1
    if request.method == 'GET':
        return render(request, 'login.html', data)
    else:
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')
        if not(user_id and user_pw):
            data['error'] = "모든 값을 입력해야 함"
        else:
            try:
                user = User_info.objects.get(user_id = user_id)
            except:
                data['error'] = '유저 없음'
                return render(request, 'login.html')
            if user_pw == user.user_pw: # check_password를 쓰니깐 안 됨 -> 왜냐면 회원가입 시에 make_password로 값을 넣지 않아서 DB 내 비밀번호가 그냥 스트링임
                request.session['user'] = user.user_id
                print('로그인 성공 -> ' + user.user_id)
                return redirect('/')
            else:
                data['error'] = '비밀번호가 틀렸음'
        return render(request,"login.html", data)

def logout(request):
    try:
        user = request.session['user']
    except:
        user = None
    if user:
        del request.session['user']
    else:
        print('로그인 중이 아님')
    return redirect('/')

def signup(request):
    data = {}
    data['login'] = 1 # 로그인 안 한 상태
    print('signup ')
    if request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        user_pw = request.POST.get('user_pw', None)
        user_name = request.POST.get('user_name', None)
        user_email = request.POST.get('user_email', None)
        user_phone_number = request.POST.get('user_phone_number', None)
        user_RRN1 = request.POST.get('user_RRN1', None)
        user_RRN2 = request.POST.get('user_RRN2', None)
        user_role = request.POST.get('user_role', None)

        if not(user_id and user_pw and user_name and user_email and user_phone_number and user_RRN1 and user_RRN2):
            data['error'] = "모든 값을 입력해야 함"
            print('dddddd')
        else:
            print('else 문')
            user = User_info(
                user_id = user_id,
                user_pw = user_pw,
                user_name = user_name,
                user_email = user_email,
                user_phone_number = user_phone_number,
                user_RRN1 = user_RRN1,
                user_RRN2 = user_RRN2,
                user_role = user_role
            )
            user.save()
            print('유저 DB 들어감')
            if user_role == '멘토':
                print(user.user_name)
                mentor = Mentor_info(
                    user_info_id = user
                )
                mentor.save()
                print('멘토 DB 들어감')
            elif user_role == '멘티':
                menti = Menti_info(
                    user_info_id = user
                )
                menti.save()
                print('멘티 DB 들어감')
            return render(request, 'index.html', data)
        return render(request, 'index.html', data)
    else:
        print('GET')
        return render(request, 'signup.html', data)


def cash(request):
    data = {}
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user') # 'tony'
    user = User_info.objects.get(user_id=user_temp) 

    if request.method == "POST":
        try:
            cash_money = request.POST.get('cash') #충전 할 금액
            #캐시 DB에 저장
            myCash = Cash(payer=user.user_name, user_id = user,
                                cash_charge = cash_money
                                )
            myCash.save()
            return HttpResponse('충전신청이 완료 되었습니다.')    
        except:
            #캐시 DB를 ManyToMany로 바꿔서 여러번 충전이 가능하도록 해야되지 않나욤?
            #현재는 한번 들어가면 못들어가게 설정.
            #아니면 충전 신청이 완료되서 입금을 확인 후 --> DB를 지우는 방법도 있음 ( 추천^^)
            return HttpResponse('충전 대기중입니다.')
    else:
        data['user'] = user
        return render(request,"cash.html",data)


def certification(request):
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user') # 'tony346'
    user = User_info.objects.get(user_id=user_temp)
    
    if request.method == "POST": #인증서를 추가하고 다 놓은것
        try:
            user.user_certification=request.FILES['image']
        except: #이미지가 없어도 그냥 지나가도록-!
            return HttpResponse('파일이 없습니다...')
        user.save()
    else: #GET으로 들어올 때
        if user.user_certification_check: #인증이 완료된 경우에는 인증서를 보여주기.
                return HttpResponse('인증이 완료되었습니다.')
        else: #인증이 완료가 안 된 경우에는 --> 인증서를 추가할 수 있는 기능
                return render(request,'certification.html')

    return render(request,'certification.html')

def profile(request):
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user') # 'tony346'
    user = User_info.objects.get(user_id=user_temp)
    print('profi')
    return render(request,'certification_check.html',{'profile':user})

def certification_create(request):
    pass

def mypage_update(request):
    if request.method == "POST": #변경 버튼을 눌렀을 때
        #로그인 한 사용자를 가져오기
        user_temp = request.session.get('user') # 'tony346'
        user = User_info.objects.get(user_id=user_temp)
        
        try:
            # user.user_name = request.POST.get('name')s
            user.user_email = request.POST.get('email')
            user.user_phone_number = request.POST.get('phoneNumber')
            user.user_certification = request.FILES['image']
        except:
            return HttpResponse('폼 에러 입니다.')
        user.save() #변경ㅋ
    else:
        return render(request,'myinfo_up.html')
    return redirect(reverse('mypage'))
    

def mylecture(request): # My강의
    data = {}
    user_temp = request.session.get('user') # 'tony'
    print(user_temp)
    user = User_info.objects.get(user_id=user_temp) 
    print(user.pk)
    menti = Menti_info.objects.get(user_info_id = user.pk)
    print(menti.pk)
    myLec = MyLecture.objects.filter(user_id = menti.pk)
    print(myLec)

    count = myLec.count()
    
    data['user'] = user
    data['myLec'] = myLec
    data['views_count'] = count
    

    return render(request,"myclass.html",data)


def LectureDetail(request, each_id):
    data={}
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user') # 'tony346'
    user = User_info.objects.get(user_id=user_temp)

    lectruredetail= get_object_or_404(Lecture, pk = each_id)

    data['object'] = lectruredetail
    return render (request, 'lecture.html', data)


def mypage_mentor(request): #마이페이지(멘토)
    data = {}
    user_temp = request.session.get('user') 
    print(user_temp)
    user = User_info.objects.get(user_id = user_temp) #유저
    print(user.pk)
    mentor =  Mentor_info.objects.get(user_info_id = user.pk) #멘토
    print(mentor)
    mylecture = Lecture.objects.filter(mentor_id = mentor.pk) #강의
    print(mylecture)
   
    data['user'] = user
    data['mentor'] = mentor
    data['mylecT'] = mylecture    
    #print(favLecture[1].user_id)
    
    return render(request,"mypage_mentor.html",data)

def lecture(request):
    data = {}
    user_temp = request.session.get('user')
    print(user_temp)
    user = User_info.objects.get(user_id=user_temp) #유저
    print(user.pk)
    mentor =  Mentor_info.objects.get(user_info_id = user.pk) #멘토
    print(mentor)
    mylecture = Lecture.objects.filter(mentor_id=user.pk) #강의
    print(mylecture)

    data['user'] = user
    data['mentor'] = mentor
    data['mylecT'] = mylecture    
    #print(favLecture[1].user_id)
    return render(request,"lec.html",data)

def mypage_mentor_up(request): #멘토마이페이지 업데이트
    if request.method == "POST": #변경 버튼을 눌렀을 때
        #로그인 한 사용자를 가져오기
        user_temp = request.session.get('user')
        user = User_info.objects.get(user_id=user_temp)
        
        try:
            # user.user_name = request.POST.get('name')
            user.user_email = request.POST.get('email')
            user.user_phone_number = request.POST.get('phoneNumber')
            user.user_certification = request.FILES['image']
        except:
            return HttpResponse('폼 에러 입니다.')
        user.save() 
    else:
        return render(request,'mentor_up.html')
    return redirect(reverse('mentor'))

def mentor_lecture(request, each_id):
    mentordetail= get_object_or_404(Lecture, pk = each_id)
    return render (request, 'mentorLec.html', {'views_mentordetail': mentordetail})

def fav_lecture(request, each_id):
    fav_lecture= get_object_or_404(Lecture, pk = each_id)
    return render (request, 'fav_lecture.html', {'views_fav_lecture': fav_lecture})


# def dummy(request):
#     data = {}
#     #로그인 한 사람이 누구인제 체크 ( 예외처리는 아직. )
#     user_temp = request.session.get('temp') # 'tony346' -> 

#     user = User_info.objects.get(user_id=user_temp) 

#     menti =  Menti_info.objects.get(user_info_id = user.pk)
#     #그 사람이 신청한 수강을 가져온다.
#     myLectureList =  LectureList.objects.filter(user_id = menti.pk)
#     sum = 0
#     #신청한 수강들의 price를 가져온다.
#     for lecture in myLectureList:
#         sum += lecture.price
#     print('sum = ',sum)
#     #다 더한 뒤 cash.html에 data로 보내준다.
#     data['price_sum'] = sum
#     return render(request,"cash.html",data)