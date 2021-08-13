from django import forms
from django.contrib.auth.backends import RemoteUserBackend
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from mentoringapp.models import *
from myapp.models import User_info, Menti_info, Cash, Payment
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.utils import timezone
from mentoringapp.custom_data import *

# 수정
def index(request):
    data = {}
    login = request.session.get('user')
    if login:
        user = User_info.objects.get(user_id=login)
        data['user'] = user
    else:
        data['login'] = 1
    return render(request, "index.html", data)

#회원가입
def signup(request):
    data = {}
    login = request.session.get('user')

    if login:
        user = User_info.objects.get(user_id=login)
        data['user'] = user

        return HttpResponse("이미 로그인한 상태입니다.")

    else:
        data['login'] = 1 #로그인 안됐다라는 뜻
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
                users = User_info(
                    user_id = user_id,
                    user_pw = user_pw,
                    user_name = user_name,
                    user_email = user_email,
                    user_phone_number = user_phone_number,
                    user_RRN1 = user_RRN1,
                    user_RRN2 = user_RRN2,
                    user_role = user_role
                )
                users.save()
                print('유저 DB 들어감')
                if user_role == '멘토':
                    print(users.user_name)
                    mentor = Mentor_info(
                        user_info_id = users
                    )
                    mentor.save()
                    print('멘토 DB 들어감')
                elif user_role == '멘티':
                    menti = Menti_info(
                        user_info_id = users
                    )
                    menti.save()
                    print('멘티 DB 들어감')
                return render(request, 'index.html', data)
            return render(request, 'index.html', data)

        else:
            print('GET')
            return render(request, 'signup.html', data)



#로그인
def login(request):

    data = {}
    login = request.session.get('user')

    if login:
        user = User_info.objects.get(user_id=login)
        data['user'] = user

        return HttpResponse("이미 로그인한 상태입니다.")

    else:
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
            

# //수정
def logout(request):
    try:
        user = request.session.get('user')
    except:
        user = None
    if user:
        del request.session['user']
    else:
        print('로그인 중이 아님')
    return redirect('/')

def profile(request):
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user') # 'tony346'
    user = User_info.objects.get(user_id=user_temp)
    print('profi')
    return render(request,'certification_check.html',{'profile':user})

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

'''
def LectureDetail(request, each_id):
    data={}
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user') # 'tony346'
    user = User_info.objects.get(user_id=user_temp)

    lectruredetail= get_object_or_404(Lecture, pk = each_id)

    data['object'] = lectruredetail
    return render (request, 'lecture.html', data)

    
'''

#강좌 상세보기

def LectureDetail(request, each_id):
    data={}
    #로그인 한 사용자를 가져오기
    data={}
    user_temp = request.session.get('user')
    user = User_info.objects.get(user_id=user_temp)

    mentor =  Mentor_info.objects.get(pk=each_id)
    Lec = Lecture.objects.filter(mentor_id = mentor.pk)
    detailLec = DetailLecture.objects.filter(lecture_title = mentor.pk)
    
    data['mentor']  = mentor

    data['Lec']  = Lec

    data['detailLec']  = detailLec

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

#지원님 파일


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

# 검색?
#호준님 파일
def mento_Search(request):
    data = {}
    instance_obj = []
    mento_list = Mentor_info.objects.all()
    data['mentos']  = mento_list
    for mento in mento_list:
        contents = mento.convert_contents()
        custom_dataset = mento_temp()
        custom_dataset.id = mento.pk #멘토 DB의 기본키값.
        temp = Lecture.objects.filter(mentor_id = mento).values()
        custom_dataset.title=temp[0]['lecture_title']
        custom_dataset.lec = temp[0]['description']
        custom_dataset.field = temp[0]['field']
        
        print(temp[0]['lecture_title'])
        custom_dataset.name = mento
        custom_dataset.contents = contents
        instance_obj.append(custom_dataset)

    for i in instance_obj:
        print('->>>',i.lec)    
    print('------------->',)
    data['objects'] = instance_obj
    return render(request,'search.html',data)

def class_upload(request):
    #현재 로그인 한 사람이 누구인지 체크
    user_temp = request.session.get('user') # 'tony'
    user = User_info.objects.get(user_id=user_temp) 
    #만약에 멘토 --> 이 조건은 class_upload.html 안에서 if문으로 구현하기.
    mento =  Mentor_info.objects.get(user_info_id = user) #멘토를 찾는다.
    print(mento)
    #이 부분은 따로 변경해야된다. 세부 강의의 정보를 매게변수로 받아야함.
    print('멘토의 pk = ',mento.pk)
    if request.method == "POST": #제출하기 버튼을 눌렀을 때
        if request.POST.get('class_name') != 'pass':
            
        #일단 강의DB에 저장해야된다.
            try:
                myLec = Lecture(
                    lecture_title = request.POST.get('class_name'),
                    mentor_id = mento,
                    description = request.POST.get('class_intro'),
                    price = request.POST.get('class_price'),
                    #임시코드
                    field = '개발·프로그래밍'
                )
            except:
                return HttpResponse('유효하지 않는 데이터입니다.')
            myLec.save()
            print('강좌가 업로드 되었습니다.')
            
        #세부 강의 저장해보자. --> CLASS에 강좌 이런거에 아무것도 안입력했을 때 
            try:
                total_input_data = int(request.POST.get('total'))
                temp_lec_name = request.POST.get('class_name')
                print(temp_lec_name)
                try:
                    lec = Lecture.objects.get(lecture_title = temp_lec_name)
                    print('lec ==>>',lec)
                except:
                        return HttpResponse('먼저 강좌를 업로드 하세요.')
                for i in range(1,total_input_data+1):
                    detail_lec = DetailLecture( 
                    lecture_title = lec,
                    video_title = request.POST.get('title'+str(i)),
                    url = request.POST.get('youtube_iframe'+str(i))
                    )
                    detail_lec.save()
            except:
                return HttpResponse('유효하지 않는 데이터입니다.')

        else:
            return HttpResponse('클래스 강좌를 입력하세요. ')
        print('DB에 저장이 완료되었습니다.')
        return HttpResponse('DB에 저장이 완료되었습니다')
    else:
        return render(request,'class_upload.html')

# 강의 상세 페이지
def LectureDetail(request, each_id): #강의의 기본키가 들어옴.
    data={}
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user')
    user = User_info.objects.get(user_id=user_temp)
    print(each_id)
    #예외처리 하기. 뭐 수강중인지 아닌지! + 먼저 멘티인지 멘토인지 구분하기
    lec = Lecture.objects.get(pk=each_id)
    print(lec.mentor_id)
    if user.user_role =='멘토' : 
        #현재 로그인한 사람이 멘토인데 강의를 올린 사람이면 볼 수 있도록!
        try:
            detail_lec = DetailLecture.objects.filter(lecture_title=lec)
            data['detail_lec'] = detail_lec
            a = detail_lec.values()
            print(a[0]['url'])
            data['lec_url'] = a[0]['url'].split(" ")[3][5:-1]
                          
        except:
                return HttpResponse('세부강의가 존재하지 않습니다.')
    else:
        return HttpResponse('멘토는 수강할 수 없습니다.') 
    
    
    return render (request, 'class1_play.html', data)


# 마이페이지 > 수정하기
def myinfo_re(request):
    return render(request,'myinfo_re.html')

# 마이페이지 > 정보등록
def myinfo_up(request):
    try:
        user_temp = request.session.get('user')  #현재 로그인한 사람
        user = User_info.objects.get(user_id = user_temp) 

        data={}
        data['user'] = user

    except:
        return HttpResponse('로그인 하세요.')

    if request.method == "POST":
        up_user_school = request.POST.get('user_school',None)
        activity = request.POST.get('activity',None)
        certificate = request.POST.get('certificate',None)
        prize = request.POST.get('prize',None)
        language = request.POST.get('language',None)
        self_introduction_file = request.POST.get('self_introduction_file', None)
        

        user = User_info(
            user_id = user.user_id,
            user_pw = user.user_pw,
            user_name = user.user_name,
            user_email= user.user_email,
            user_register_dttm = user.user_register_dttm ,
            user_phone_number = user.user_phone_number ,
            user_RRN1 = user.user_RRN1 ,
            user_RRN2 = user.user_RRN2 ,
            user_certification = user.user_certification,
            user_certification_check= user.user_certification_check ,
            user_role = user.user_role ,
            user_cash = user.user_cash,
            user_school = up_user_school,
        
        )
        qual = Qualification(
            user_id = user,
            activity =                activity       ,         
            certificate =             certificate     ,            
            prize =                   prize            ,           
            language =                language         ,
            self_introduction_file =  self_introduction_file,          

        )

        user.save()
        print("유저저장")
        qual.save()
        print("스펙저장")

        return render(request, 'index.html' ,data )
    
    else:
        return render(request,'myinfo_up.html', data)


##지영수정
def certification(request):
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user') # 'tony346'
    user = User_info.objects.get(user_id=user_temp)

    data={}
    data['user'] = user

    if request.method == "POST": #인증서를 추가하고 다 놓은것
        try:
            user.user_certification = request.FILES['image']
            
        except: #이미지가 없어도 그냥 지나가도록-!
            return render(request, 'certification_check.html', data)
        user.save()


    else: #GET으로 들어올 때
        if user.user_certification_check == True : #인증이 완료된 경우에는 인증서를 보여주기.
            show_cer = user.user_certification

            data['show_cer'] = show_cer
            return render(request, 'certification.html', data)

        else: #인증이 완료가 안 된 경우에는 --> 인증서를 추가할 수 있는 기능
                show_cer = user.user_certification
                data['show_cer'] = show_cer
                
                #user.user_certification = request.FILES['image'] 보류

                return render(request,'certification.html', data)

    return render(request,'certification.html', data)

# 지원 수정
# 캐쉬 충전하기
def cash_check(request):
    data = {}
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user') # 'tony'
    user = User_info.objects.get(user_id=user_temp) 

    if request.method == "POST":
        try:
            cash_money = request.POST.get('cash') #충전 할 금액
            myCash = Cash(payer=user.user_name, user_id = user,
                                cash_charge = cash_money
                                )
            myCash.save()
            return HttpResponse('충전신청이 완료 되었습니다.')    
        except:
            #캐시 DB를 ManyToMany로 바꿔서 여러번 충전이 가능하도록 해야되지 않나욤?
            #현재는 한번 들어가면 못들어가게 설정.
            #아니면 충전 신청이 완료되서 입금을 확인 후 --> DB를 지우는 방법도 있음 ( 추천^^)
            return HttpResponse('충전신청이 정상 진행되지않았습니다. 나중에 다시 시도해주세요.')
    else:
        data['user'] = user
        return render(request,"cash_check.html",data)

#마이페이지 통합
def mypage(request):
    data = {}
    user_temp = request.session.get('user') 
    print(user_temp)
    user = User_info.objects.get(user_id=user_temp)
    print(user.pk)

    if user.user_certification_check:
        check = "인증완료"
    
    else:
        check = "인증실패"
    data['check'] = check # 인증여부


    if user.user_role == '멘티':
        menti =  Menti_info.objects.get(user_info_id = user.pk)
        print(menti)
        fav = FavouriteLecture.objects.filter(user_id = menti.pk)
        print(fav)        
        mylecture = MyLecture.objects.filter(user_id = menti.pk) #강의
        print(mylecture)
        menti_count = mylecture.count()
        
        data['mylecT'] = mylecture  
        data['menti_count'] = menti_count
        data['menti'] = menti
        data['favLec'] = fav

        try: #충전 승인 받으면 충전 되도록
            cashDB = Cash.objects.get(user_id = user)
            print('zzzzz--> ',cashDB)
            print(cashDB.cash_charge)
            print(cashDB.success_true_false)
            
            if cashDB.success_true_false:
                print('zzzzzzzzzzzzzzz::')
                print(user.user_cash)
                user.user_cash += cashDB.cash_charge
                print(user.user_cash)
                user.save()
        except:
            pass

        data['user'] = user
        return render(request,"mypage.html",data)

    elif user.user_role == '멘토': #멘토 마이페이지
        mentor =  Mentor_info.objects.get(user_info_id = user.pk) #멘토
        print(mentor)
        try:
            mylecture = Lecture.objects.filter(mentor_id = mentor.pk) #강의
            mentor_count = mylecture.count()
        except:
            print('no lecture')

        data['mentor'] = mentor
        data['mylecT'] = mylecture   
        data['mentor_count'] = mentor_count
        return render(request,"mypage.html",data)


# 마이페이지 캐쉬 보여주기 
def cash(request): 
    data = {}
    user_temp = request.session.get('user')
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
    
    if user.user_certification_check:
        check = "인증완료"
    
    else:
        check = "인증실패"
    
    data['check'] = check

    return render(request,"cash.html",data)

# 멘티의 My강의  --> 호준 최종 --> myapp views.py 
def myclass(request): 
    data = {}
    user_temp = request.session.get('user') # 'tony'
    print(user_temp)
    user = User_info.objects.get(user_id=user_temp) 
    print(user.pk)
    data['user'] = user
    if user.user_role == '멘티':
        menti = Menti_info.objects.get(user_info_id = user.pk)
        print(menti.pk)
        myLec = MyLecture.objects.filter(user_id = menti.pk)
        print(myLec)
        FavorLec = FavouriteLecture.objects.filter(user_id = menti.pk)
        print(FavorLec)

        count = myLec.count()
        fav_count = FavorLec.count()
        
        data['user'] = user
        data['myLec'] = myLec
        data['views_count'] = count
        data['FavorLec']= FavorLec
        data['fav_count']= fav_count    
    else:
        mento = Mentor_info.objects.get(user_info_id = user)
        data['mento'] =mento
    return render(request,'myclass.html',data)


# 칼럼 작성 페이지 -> 반드시 멘토만 접근할 수 있도록 html 쪽에서 막아줘야 함
def column_write(request):
    user = request.session.get('user')
    mentor = Mentor_info.objects.get(user_info_id=user)
    if request.method == 'POST':
        title = request.POST.get('title', None)
        author = mentor
        content = request.POST.get('content', None)
        photo = request.POST.get('photo', None)
        if not(title and author and content):
            print('모두 입력해야 함')
        else:
            column = Column(
                title = title,
                author = author,
                content = content,
                photo = photo
            )
            column.save()
            print('칼럼 저장')
        return redirect('/mentoring')
    return render(request, 'column_write.html')

# 이벤트 작성
def event_up(request):
    try:
        user_temp = request.session.get('user')  #현재 로그인한 사람
        user = User_info.objects.get(user_id=user_temp) 
        print(user)
        mento = Mentor_info.objects.get(user_info_id = user) #현재 로그인 한 사람이 
                                                            #멘토인지 확인해본다.
        #없으면 쿼리를 못찾는다고 오류가 발생함.
    except:
        return HttpResponse('로그인 하세요 또는 멘토가 아닙니다.')
    
    if request.method == "POST":
         
        event_title = request.POST.get('title') 
        event_content = request.POST.get('event_content') 
        event_photo = request.FILES.get('photo') #파일이 없을 때 예외처리 해야함.

        new_event = EventList(title = event_title, 
                                event_content = event_content,
                                author = mento,
                                event_photo = event_photo,
                                )
        new_event.save()
        return HttpResponse('작성이 완료되었습니다.') 
    else:
        return render(request, 'event_up.html')