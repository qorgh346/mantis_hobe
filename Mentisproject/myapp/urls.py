from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),

    path('mypage/update/',views.mypage_update,name='mypage_update'),
    path('cash/',views.cash,name='cash'),

    # 자격증
    path('mypage/certification/',views.certification,name='certification'),
    path('mypage/certification/view/',views.profile,name='profile'),

    # 강의
    path('mypage/mylecture/',views.mylecture,name='mylecture'),
    path('mypage/mylecture/<str:each_id>/', views.LectureDetail, name='urlnameLectureDetail'),

    # 멘토 마이페이지
    path('mypage_mentor/',views.mypage_mentor,name='mentor'), #멘토의 마이페이지
    path('mypage_mentor/update/',views.mypage_mentor_up,name='mentor_up'), #멘토의 마이페이지 업데이트
    path('mypage/mentorlecture/<str:each_id>/', views.mentor_lecture, name='mentordetail'),

    # 칼럼
    path('mypage/column_write/',views.column_write,name='column_write'),

    # 즐찾 페이지
    path('mypage/favorite_Lectures/<str:each_id>/', views.fav_lecture, name='fav_lecture'),
    path('cash_check/', views.cash_check, name='cash_check'),

    # 강의 업로드
    path('class_upload/',views.class_upload, name='class_upload'), # 강의 페이지 업로드 들어가는 url

    # 마이페이지?
    path('myinfo_up/',views.myinfo_up, name='myinfo_up'),
    path('myinfo_re/',views.myinfo_re, name='myinfo_re'),
    path('myclass/',views.myclass, name='myclass'),

    path('event_up/',views.event_up, name='event_up'),
]