from django.urls import path
from . import views
urlpatterns = [
    # 이벤트
    path('event/',views.event, name='event'),
    #-----------------------------호준 파일
    path('event_detail/<int:mento_id>/',views.event_detail, name='event_detail'),    
    path('event_sign/<int:event_id>/',views.event_sign,name ='event_sign'), #이벤트 신청하기 버튼 누르면~
    #----------------------------------------
    path('event_re/',views.event_re, name='event_re'),

    # 세부 강의
    path('class_view/<str:each_id>/',views.class_view, name='class_view'), # 세부 강의 페이지로 들어가는 url
    path('class1_play/<str:each_id>/',views.class1_play, name='class1_play'), # 세부 강의의 영상 페이지로 들어가는 url

    #지영님 파일
    path('about/<str:each_id>/',views.About,  name ='about'), # mentor_detail을 넣으려고 했음 -> 멘토 페이지
    path('review_filter/<str:filter_id>/', views.review_filter,name= 'review_filter'),
    path('review_up/', views.review_up ,name= 'review_up'),

    # 칼럼 //수정
    path('column/<int:mentor_pk>',views.column,name='column'),
    path('column/detail/<int:column_pk>',views.column_detail1,name='column_detail1'),
    
    # 질문
    path('qna/<int:mentor_pk>',views.qna,name='qna'),
    path('qna/detail/<int:question_pk>',views.qna_detail1,name='qna_detail1'),
    path('qna_write/',views.qna_write,name='qna_write'),

    # 멘토
    path('mentoring/',views.mentoring,name='mentoring'),
    path('mentoring/register/<int:mentoring_id>/',views.mentoring_register,name='mentoring_register'),
    path('mentoring/mento_detail/<int:mento_id> ',views.mento_detail,name='mento_detail'),

    # 뭐야?
    path('apply_check/',views.apply_check, name='apply_check'),

    # 결제
    path('buy_lec/',views.buy_lec, name='buy_lec'), 
    path('buy_lec/<str:each_id>/',views.buy_detail, name='buy_detail'),
    path('buy_process/<str:buy_id>/',views.buy_process, name='buy_process'),
    path('buy_sucess/', views.buy_sucess,name='buy_sucess'),
]
