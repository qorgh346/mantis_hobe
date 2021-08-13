from datetime import date
from django import forms
from django.contrib.auth import authenticate, login as auth_login
from django.utils import timezone
from django.contrib.auth.backends import RemoteUserBackend
from django.shortcuts import redirect, render, HttpResponse

from myapp.models import User_info,Menti_info, Cash, Payment
from mentoringapp.models import *
from .custom_data import *

# Create your views here.

# //이벤트    
#호준 파일 --> 8.12일 
def event(request):
    data = {}
    user = request.session.get('user')
    instance_lists = []
    eventList = EventList.objects.all()
    data['eventList'] = eventList
    for i in eventList: # i = EventList
        print('--->',i)
        user = User_info.objects.get(user_name=i.author)
        print('user = ',user)
        print(i.author)
        mento = Mentor_info.objects.get(user_info_id=user)
        contents = mento.convert_contents()
        print('zzzz')
        print(i.pk) #pk값 : 멘토의 아이디값임.
        custom_dataset = event_temp()
        custom_dataset.id = mento.pk #이벤트 DB의 기본키값.
        print('------------->>>',custom_dataset.id)
        custom_dataset.name = mento
        custom_dataset.contents = contents
        custom_dataset.title = i.title
        instance_lists.append(custom_dataset)
    data['eventLists'] = instance_lists
    return render(request, "event.html",data)


def event_detail(request,mento_id):
    data = {}
    print('=====>',mento_id)

    detailMento = Mentor_info.objects.get(pk=mento_id)
    print(detailMento)

    content_list = detailMento.convert_contents()
    print(content_list)
    event = EventList.objects.get(author =detailMento )
    print(event)
    
    data['user_name']=detailMento
    data['content_list'] = content_list
    data['event'] = event
    print(event.pk)
    
    return render(request, "event_detail1.html",data)


def event_sign(request,event_id): #이벤트 신청하기 버튼 누르면~ -> 이벤트의 pk값이 넘어옴
    #이벤트 어떤건지 가져오기.
    event = EventList.objects.get(pk=event_id)
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('user')
    user = User_info.objects.get(user_id=user_temp)
    print('user = ',user)
    print('event = ',event)
    event_apply = EventApply(
        apply_object = event,
        applicant = user,
        agreement = True
    )
    event_apply.save()

    return HttpResponse('지원 완료')

# 신청 완료 페이지
def apply_check(request):
    return render(request, "apply_check.html") 

def event_re(request):
    return render(request, "event_re.html")

# //강의
# 전체 강의 페이지
def lecture(request):
    # 멘토 이름, 멘토 설명, 강의 이름, 설명
    data = {}
    instance_lists = []
    try:
        lecture = Lecture.objects.all()
    except:
        print('no lecture')
       

    return render(request, "lecture.html")

# 각 강의별 페이지
def class_view(request, each_id):
    data={}
    # user_temp = request.session.get('user')
    # user = User_info.objects.get(user_id=user_temp)
    print('멘토의 기본키 --> ',each_id)
    mentor =  Mentor_info.objects.get(pk=each_id)
    Lec = Lecture.objects.filter(mentor_id=mentor.pk)



    review = Review.objects.filter(review_object_id=mentor.pk)
    
    data['mentor']  = mentor
    data['Lec']  = Lec
    data['review']  = review


    return render (request, 'class1.html', data)

def class1_play(request,each_id): #세부 강의 재생해주기.
    #매게변수로 받은 세부강의pk 값으로 -> DB에서 url을 가져온다.
    #그 다음 메인에 보여주기...
    data = {}
    
    detail_lecture = DetailLecture.objects.get(pk = each_id)

    #역참조가 될려나..
    orgin_lec = detail_lecture.lecture_title
    print(orgin_lec)
    #오류가 날 듯................
    print('zzzzz-->>> ',orgin_lec)
    lec_list = DetailLecture.objects.filter(lecture_title = orgin_lec) 
    print('zzzzz-->>> ',lec_list)
    print(lec_list)
    temp_url = detail_lecture.url.split(" ")[3]
    url = temp_url[5:-1]
    print('url -------------------<',url)
    data['lec_url'] = url


    data['detail_lec'] = lec_list  #세부강의 List를 담아야됌.
    return render(request, "class1_play.html",data)

def About(request, each_id):
    data={}
    user_temp = request.session.get('user')
    user = User_info.objects.get(user_id=user_temp)

    mentor =  Mentor_info.objects.get(pk=each_id)
    Lec = Lecture.objects.filter(mentor_id=mentor.pk)
    review = Review.objects.filter(review_object_id=mentor.pk)
    
    data['mentor']  = mentor
    print(mentor)
    data['Lec']  = Lec
    print(Lec)
    data['review']  = review

    return render (request, 'mentor_detail.html', data)

def review_up(request): #제출이 안되는 상황 
    #로그인 한 사용자를 가져오기
    data = {}
    user_temp = request.session.get('user') # 'tony346'
    user = User_info.objects.get(user_id = user_temp)
    

    #data = {}
    if user.user_role == '멘티':
        #근데 여기서 해당멘토가 맞냐는 검사도 필요하지않을까?
        if request.method == 'POST':
            
            review_object = request.POST.get('review_object', None)
            author = request.POST.get('author', None)
            content = request.POST.get('content', None)
            review_point = request.POST.get('review_point', None)
            
            new_review = Review(

                review_object = review_object,
                author = user.user_name,
                content = content ,
                review_point = review_point,
                reivew_at = timezone.now(),

            )

            new_review.save()

            data['review_object'] = review_object
            data['author'] = author
            data['content'] = content
            data['review_point'] = review_point

            #data['review'] = new_review
            return render(request, 'review_re.html', data )
        else:
            return render (request, 'review_up.html', data )

    else:
        return HttpResponse('멘티만 작성할 수 있습니다.') 



def review_filter(request, filter_id):
    data={}
    mentor_review = Review.objects.filter(review_object=filter_id) 
    count_review = mentor_review.count()
    review_lastest = Review.objects.order_by('-reivew_at').filter(review_object=filter_id)
    review_GPA = Review.objects.order_by('review_point').filter(review_object=filter_id)
    
    data['mentor_review'] = mentor_review
    data['count_review'] = count_review
    data['review_lastest'] = review_lastest
    data['review_GPA'] = review_GPA

    return render(request, 'review_re.html', data)

# 현진님 파일

# column.html: 멘토의 전체 칼럼
# column_write.html: 멘토가 칼럼을 작성하는 곳
# column_re.html: 작성한 칼럼을 수정하는 곳
# column_coment_re.html: 칼럼 댓글을 수정하는 곳
# 내가 추가: column_comment: 칼럼 댓글 작성하는 곳

# 선택한 멘토의 전체 칼럼 페이지
def column(request, mentor_pk):
    data = {}
    user_id = request.session.get('user')
    user = User_info.objects.get(user_id=user_id)
    data['user'] = user
    mentor = Mentor_info.objects.get(pk = mentor_pk)
    data['mentor'] = mentor
    try:
        column = Column.objects.filter(author=mentor_pk)
        data['column'] = column.order_by("created_at")
    except:
        print('칼럼 없음 !')
    return render(request, 'column.html', data)

# 칼럼 상세 + 댓글 페이지
def column_detail1(request, column_pk):
    data = {}
    user_id = request.session.get('user')
    column_detail = Column.objects.get(pk=column_pk)
    data['column_detail'] = column_detail
    column_comment = ColumnComment.objects.filter(column=column_detail)
    data['column_comment'] = column_comment
    if request.method == 'GET':
        return render(request, "column_detail1.html", data)
    else: # 댓글 작성 시: 해당 칼럼의 pk 값과 나머지 정보들을 받아와서 이를 ColumnComment에 저장해야 함
        user_id = User_info.objects.get(user_id=user_id)
        comment = request.POST.get('column_comment', None)
        if not(comment):
            print('댓글 입력 필수')
        else:
            column_comment = ColumnComment(
                column = column_detail,
                user_id = user_id,
                comment = comment,
            )
            column_comment.save()
            print('칼럼 댓글 저장')
        return redirect('/column/detail/'+str(column_pk))

# 질문 메인 페이지 -> 모두 접근 가능
def qna(request,mentor_pk):
    data = {}
    user_id = request.session.get('user')
    user = User_info.objects.get(user_id=user_id)
    data['user'] = user
    mentor = Mentor_info.objects.get(pk = mentor_pk)
    data['mentor'] = mentor
    try:
        question = Question.objects.all()
        data['question'] = question.order_by("created_at")
    except:
        print('질문 없음 !')
    return render(request, 'qna.html', data)

# 질문 상세 + 댓글 페이지 -> 모두 접근 가능
def qna_detail1(request, question_pk):
    data = {}
    user_id = request.session.get('user')
    qna_detail = Question.objects.get(pk=question_pk)
    data['qna_detail'] = qna_detail
    qna_comment = QuestionComment.objects.filter(question=qna_detail)
    data['qna_comment'] = qna_comment
    if request.method == 'GET':
        return render(request, "qna_detail1.html", data)
    else: # 댓글 작성 시: 해당 칼럼의 pk 값과 나머지 정보들을 받아와서 이를 QuestionComment 저장해야 함
        user = User_info.objects.get(user_id=user_id)
        comment = request.POST.get('qna_comment', None)
        if not(comment):
            print('댓글 입력 필수')
        else:
            qna_comment = QuestionComment(
                question = qna_detail,
                user_id = user,
                comment = comment,
            )
            qna_comment.save()
            print('qna 댓글 저장')
        return redirect('/qna/detail/'+str(question_pk))

# 질문 작성 페이지 -> 반드시 멘티만 접근할 수 있도록 html 쪽에서 막아줘야 함
def qna_write(request):
    user = request.session.get('user')
    menti = Menti_info.objects.get(user_info_id=user)
    if request.method == 'POST':
        title = request.POST.get('title', None)
        print('title :', title)
        author = menti
        print('author :', author)
        content = request.POST.get('content', None)
        print('content :', content)
        photo = request.POST.get('photo', None)
        if not(title and author and content):
            print('모두 입력해야 함')
        else:
            question = Question(
                title = title,
                author = author,
                content = content,
                photo = photo
            )
            question.save()
            print('질문 저장')
        return redirect('/mentoring')
    return render(request, 'qna_write.html')

# //멘토링
# 멘토링: 멘토 이름(user_info), 멘토 설명(mentoring), 멘토의 분야(mentor_info), 
def mentoring(request):
    data = {}
    user = request.session.get('user')
    if user:
        user = User_info.objects.get(user_id=user)
        data['user'] = user
    else:
        data['login'] = 1
    instance_obj = []
    mento_list = Mentor_info.objects.all()
    data['mentos']  = mento_list
    for mento in mento_list:
        print(mento)
        contents = mento.convert_contents()
        custom_dataset = mento_temp()
        custom_dataset.id = mento.pk #멘토 DB의 기본키값.
        user = User_info.objects.get(user_name = mento)
        custom_dataset.name = user
        custom_dataset.field = mento.field
        custom_dataset.contents = contents
        instance_obj.append(custom_dataset)
    data['objects'] = instance_obj
    return render(request, 'mentoring.html', data)


# mentoring에서 하나 클릭 시 넘어가는 멘토 관련 페이지
#http://127.0.0.1:8000/mento_Search/mento_detail
def mento_detail(request,mento_id): #mento_id 는 mento의 기본키 값임.
    data = {}
    mento_obj = Mentor_info.objects.get(pk=mento_id)

    user_temp = request.session.get('user')
    if not user_temp:
        return redirect('/login')
    user = User_info.objects.get(user_id=user_temp)

    lec_list= Lecture.objects.filter(mentor_id=mento_obj)
    mento_convert =  mento_obj.convert_contents()

    try:
        mentoring  = Mentoring.objects.filter(mentor = mento_obj)
    except:
        print('no mentoring')
    
    view_Lec_list = []
    for lec in lec_list:
        detail_lecture_List =  detail_lecture_list()
        print('->>',lec)
        detail_lecture_List.lec = lec
        detail_Lec_List = DetailLecture.objects.filter(lecture_title=lec)
        detail_lecture_List.detail_lec_list = detail_Lec_List
        print('잘 들어갔어?',detail_lecture_List.detail_lec_list)
        view_Lec_list.append(detail_lecture_List)

    print('-zzzzz>>',view_Lec_list)
    for temp in view_Lec_list:
        print('나의 강좌: ',temp.lec)
        for lec in temp.detail_lec_list:
            print(lec)
    
    print(mentoring)
    data['lecture_list'] = view_Lec_list
    data['mento_major'] = mento_convert[0]
    data['mento'] = mento_obj
    data['lec_list'] = lec_list
    data['mentoring_list'] = mentoring
    data['mento_convert_list'] = mento_convert
    data['user'] = user

    return render(request,'mentor.html',data)

#나의 직무와 맞는 멘토 찾아보기
def search_field(request):
    event_title = request.POST.get('temp')
    print(event_title)
    a = Mentor_info.objects.filter(field = event_title)
    print(a)
    return render(request, 'mentoring.html')

def mentoring_register(request,mentoring_id):
    mentoring_detail = Mentoring.objects.get(pk=mentoring_id)
    user_temp = request.session.get('user')
    print(user_temp)
    user = User_info.objects.get(user_id=user_temp)
    if user.user_role =='멘티':
        menti = Menti_info.objects.get(user_info_id = user)
        result = ApplyMentoring(
                                mentoring = mentoring_detail,
                                menti = menti
                                )
        result.save()
        return HttpResponse('신청 완료')
    else: #멘토일때
        return HttpResponse('멘토는 멘토링 신청이 불가능 합니다.')

# 지영님 새로 추가한 부분 멘토링 뷰스
# 결제 관련
def buy_lec(request): #모든 강의들 보여주기
    data={}
    all_lecture = Lecture.objects.all()
    data['all_lecture'] = all_lecture    


    return render(request, 'buy_lec.html', data)

def buy_detail(request, each_id): #해당강의 결제하러가기
    data = {}
    lec = Lecture.objects.get(pk=each_id)
    detail_lec = DetailLecture.objects.filter(lecture_title_id = lec.pk)

    data['lec'] = lec
    data['detail_lec'] = detail_lec


    return render(request, "buy_detail.html", data)

def buy_process(request, buy_id): #결제 과정

    #if request.method == 'POST':
        data ={}
        user_temp = request.session.get('user')
        user = User_info.objects.get(user_id=user_temp) 
        Lec = Lecture.objects.get(pk = buy_id)
        menti = Menti_info.objects.get(user_info_id = user)


        buy_lec_detail = DetailLecture.objects.filter(lecture_title = Lec)
        cash = Cash.objects.filter(user_id = user)

        menti_cash_money = User_info.objects.get(user_id = user_temp)
        mentor= User_info.objects.get(user_id = Lec.mentor_id)

        data['user'] = user
        data['menti'] = menti
        data['mentor']= mentor
        data['Lec'] = Lec
        data['cash'] = cash
        data['buy_lec_detail'] = buy_lec_detail
        data['menti_cash_money'] = menti_cash_money

        if int(menti_cash_money.user_cash) >= int(Lec.price):

            Menti_cash = User_info(
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
                user_cash = str(int(menti_cash_money.user_cash) - int(Lec.price)) ,
            )
            
            Mentor_cash = User_info(
                user_id = mentor.user_id,
                user_pw = mentor.user_pw,
                user_name = mentor.user_name,
                user_email= mentor.user_email,
                user_register_dttm= mentor.user_register_dttm ,
                user_phone_number= mentor.user_phone_number ,
                user_RRN1 = mentor.user_RRN1 ,
                user_RRN2 = mentor.user_RRN2 ,
                user_certification= mentor.user_certification,
                user_certification_check= mentor.user_certification_check ,
                user_role = mentor.user_role ,
                user_cash = str(int(mentor.user_cash) + int(Lec.price)),
            )
            

            My_lec = MyLecture(
                lecture_title = Lec,
                user_id = menti,
            )
            Pay = Payment(
                user_id = user,
                payment_at = timezone.now(),
                sum = Lec,
            )
            print("type=")
            print(type(Menti_cash.user_cash))
            Pay.save()
            My_lec.save()
            Mentor_cash.save()
            Menti_cash.save()

            return render(request, 'buy_sucess.html', data)

        else :
            return HttpResponse('포인트가 부족합니다.')


def buy_sucess(request):
    data ={}
    user_temp = request.session.get('user')
    user = User_info.objects.get(user_id=user_temp) 
    data['user'] = user 

    return render(request, 'buy_sucess.html', data)
