from django.contrib import admin
from .models import *

# Register your models here.

# 참고 https://wayhome25.github.io/django/2017/03/22/django-ep8-django-admin/

# 멘토 DB
@admin.register(Mentor_info)
class Mentor_infoAdmin(admin.ModelAdmin):
    list_display = ('pk','user_info_id','contents', 'one_info')

# 강의 DB
@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('pk','lecture_title', 'mentor_id', 'mentor_description', 'description', 'price', 'field')

# 세부 강의 DB
@admin.register(DetailLecture)
class DetailLecutreAdmin(admin.ModelAdmin):
    list_display = ('pk','lecture_title', 'video_title', 'url')

# My 강의 DB
@admin.register(MyLecture)
class MyLectureAdmin(admin.ModelAdmin):
    list_display = ('pk','lecture_title','user_id')

# 즐겨찾기 강의 DB
@admin.register(FavouriteLecture)
class FavAdmin(admin.ModelAdmin):
    list_display = ('pk','lecture_title','user_id')


# 이벤트 DB
@admin.register(EventList)
class EventListAdmin(admin.ModelAdmin):
    list_display = ('title','author','created_at')

# 이벤트 신청 DB
@admin.register(EventApply)
class EventApplyAdmin(admin.ModelAdmin):
    list_display = ('apply_object','applicant', 'created_at', 'agreement')

# 후기 DB
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author','review_object', 'reivew_at', 'review_point')


# 칼럼 DB
@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title','author','created_at')

# 칼럼 댓글 DB
@admin.register(ColumnComment)
class ColumnCommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'column', 'user_id', 'comment', 'commented_at')
    
    def comment(self, comment):
        return comment.content[:30]

# 질문 DB
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title','author','created_at')

# 질문 댓글 DB
@admin.register(QuestionComment)
class QuestionCommentAdmin(admin.ModelAdmin):
    list_display = ('question', 'user_id', 'comment', 'commented_at')
    
    def comment(self, comment):
        return comment.content[:30]

# 멘토링 DB
@admin.register(Mentoring)
class MentoringAdmin(admin.ModelAdmin):
    list_display = ('pk','title','mentor','lecture')

# 멘토링 신청 내역 DB
@admin.register(ApplyMentoring)
class ApplyMentoringAdmin(admin.ModelAdmin):
    list_display = ('pk','mentoring','menti')

# 스펙 DB        >>> 근데 잠깐@! 멘토는 자소서없는데 user_cer이거 넣어야하나..?
@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('user_id','self_introduction_check')