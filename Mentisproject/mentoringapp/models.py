#mentoringapp.models

from django.db import models
from django.utils import timezone

# Create your models here.

# 멘토 DB
class Mentor_info(models.Model):
    user_info_id = models.ForeignKey('myapp.User_info', on_delete=models.CASCADE, db_column="user_info_id", verbose_name='멘토 ID',db_constraint=False,null=True)
    contents = models.TextField(default='(주)멋사', verbose_name='멘토 이력')
    one_info = models.TextField(blank=True, null=True, verbose_name='멘토의 다짐')  
       
    MENTOR_FIELD = (
        ('IT/SW', 'IT/SW'),
        ('PM', 'PM'),
        ('건설/기계/기술', '건설/기계/기술'),
        ('광고/홍보', '광고/홍보'),
        ('금융/은행/보험', '금융/은행/보험'),
        ('디자인', '디자인'),
        ('미디어', '미디어'),
        ('연구개발', '연구개발'),
        ('유통/물류/무역', '유통/물류/무역'),
        ('인사총무', '인사총무'),
        ('품질', '품질'),
        ('의료', '의료'),
        ('영업/고객상담', '영업/고객상담'),
        ('생산제조', '생산제조'),
        ('마케팅/기획', '마케팅/기획'),
        ('경영/사무/행정', '경영/사무/행정'),
        ('MD/상품기획', 'MD/상품기획'),
        ('SCM', 'SCM'),
        ('기타', '기타')
    ) # 분야는 인프런을 참고함
    field = models.CharField(max_length=128,
                             choices=MENTOR_FIELD,
                             default='기타',
                             verbose_name='멘토 직무')

    class Meta:
        db_table = 'mentor_table'
        verbose_name = '멘토'
        verbose_name_plural = '멘토'

    def __str__(self):
        return str(self.user_info_id)
    
    # 수정
    def convert_contents(self):
        if self.contents is not None:
            return self.contents.split(',')
        else:
            return self.contents

# 강의 DB: 기본키(아마 알아서 들어가는 걸로 알고 있음), 강의 이름, 멘토ID(외래키 -> 왜??), 강의 설명서, 강의 가격, 강사 설명, 강의 분야(복수 개 -> 대체 어떻게? 하려면 분야 DB를 따로 빼야 하지 않을까?)
class Lecture(models.Model):
    lecture_title = models.CharField(max_length=256,
                                     verbose_name='강의 이름')
    mentor_id = models.ForeignKey(Mentor_info, on_delete=models.PROTECT, db_column="mentor_id", verbose_name='멘토') # 멘토가 강의를 올리고 자신을 설명함
    mentor_description = models.CharField(max_length=64,
                                          verbose_name='멘토 설명') # 강사 설명? 강사 이름? 뭐지?
    description = models.CharField(max_length=1000,
                                   verbose_name='설명')
    price = models.CharField(max_length=64,
                             verbose_name='가격') # IntegerField? CharField?
    LECTURE_FIELD = ( # 강의 분야 고르는 것에서 여러 개 중 하나 선택으로 만듦, 여러 분야를 선택하고 싶으면 DB를 추가로 만들어야 함 (프론트에 물어 볼까..?)
        # 수정
        ('IT/SW', 'IT/SW'),
        ('PM', 'PM'),
        ('건설/기계/기술', '건설/기계/기술'),
        ('광고/홍보', '광고/홍보'),
        ('금융/은행/보험', '금융/은행/보험'),
        ('디자인', '디자인'),
        ('미디어', '미디어'),
        ('연구개발', '연구개발'),
        ('유통/물류/무역', '유통/물류/무역'),
        ('인사총무', '인사총무'),
        ('품질', '품질'),
        ('의료', '의료'),
        ('영업/고객상담', '영업/고객상담'),
        ('생산제조', '생산제조'),
        ('마케팅/기획', '마케팅/기획'),
        ('경영/사무/행정', '경영/사무/행정'),
        ('MD/상품기획', 'MD/상품기획'),
        ('SCM', 'SCM'),
        ('기타', '기타')
    ) # 분야는 인프런을 참고함
    field = models.CharField(max_length=64,
                             choices=LECTURE_FIELD,
                             verbose_name='분야',
                             blank=True,
                             null=True)
    
    def __str__(self):
        return self.lecture_title

    class Meta:
        db_table = 'lecture_table'
        verbose_name = '전체 강의'
        verbose_name_plural = '전체 강의'

# 세부 강의 DB: 기본키, 강의 ID(외래키), 영상 제목, 영상 URL
class DetailLecture(models.Model):
    lecture_title = models.ForeignKey(Lecture,
                                on_delete=models.PROTECT,
                                db_column="lecture_title",
                                verbose_name='강의 이름')
    video_title = models.CharField(max_length=256,
                                   verbose_name='영상 제목')
    url = models.CharField(max_length=256,
                           verbose_name='url')
    
    def __str__(self):
        return self.video_title

    class Meta:
        db_table = 'detail_lecture_table'
        verbose_name = '세부 강의'
        verbose_name_plural = '세부 강의'

# My 강의 -> 수정 필요
class MyLecture(models.Model):
    lecture_title = models.ForeignKey(Lecture, verbose_name='강의 이름', on_delete=models.PROTECT)
    user_id = models.ForeignKey('myapp.Menti_info', verbose_name='신청한 사람', db_column="user_id", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.lecture_title)

    class Meta:
        db_table = 'mylecture_table'
        verbose_name = 'My 강의'
        verbose_name_plural = 'My 강의'

# 즐겨찾기 강의 DB
class FavouriteLecture(models.Model):
    lecture_title = models.ForeignKey(Lecture, db_column="lecture_title", verbose_name='강의 이름', on_delete=models.CASCADE)
    user_id = models.ForeignKey('myapp.Menti_info',related_name="fav_user",db_column="user_id", verbose_name='즐겨찾기한 사람', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.lecture_title)

    class Meta:
        db_table = 'favourite_lecture_table'
        verbose_name = '즐겨찾기 강의'
        verbose_name_plural = '즐겨찾기 강의'

# 스펙 DB(토익, 토스 등): 유저 ID(외래키), 이미지(ImageField)
class Qualification(models.Model):
    user_id = models.ForeignKey('myapp.User_info', # User는 임의로 설정한 것 -> 이름 맞춰야 함 !
                                on_delete=models.PROTECT,
                                db_column="user_id",)

    self_introduction_file = models.FileField(upload_to='', null=True, blank=True, verbose_name='자기소개서 파일')

    self_introduction_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='자기소개서 파일이름')

    #자기소개서 공개 비공개
    self_introduction_check = models.BooleanField(default=False, verbose_name='자기소개서 공개 비공개')

    certificate = models.TextField(blank=True, 
                                    null=False, 
                                    verbose_name="자격증")

    certificate_verify = models.ImageField(upload_to="",
                                    blank=True,
                                    verbose_name="자격증 이미지")
    
    activity = models.TextField(blank=True, 
                                    null=False, 
                                    verbose_name="인턴, 대외활동")

    language = models.TextField(blank=True, 
                                    null=False, 
                                    verbose_name="어학")

    language_verify = models.CharField(max_length=1600000,
                                    blank=True, 
                                    null=False, 
                                    verbose_name="어학 취득번호")

    language_score = models.TextField(blank=True, 
                                    null=False, 
                                    verbose_name="어학 점수")

    prize = models.TextField(max_length=16000000, 
                                    blank=True, 
                                    null=False, 
                                    verbose_name='수상실적')

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = 'qualification_table'
        verbose_name = '스펙'
        verbose_name_plural = '스펙'


#이벤트DB
class EventList(models.Model):
    title = models.CharField(max_length=256, null=False,verbose_name='이벤트 제목')
    author = models.ForeignKey(Mentor_info, db_column="Mentor_id", on_delete=models.PROTECT, verbose_name='멘토 이름')
    event_content = models.TextField(blank=True, null=True, verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성 날짜/시간')
    event_photo = models.ImageField(upload_to="",blank=True, verbose_name='첨부 이미지')

    # 수정
    def __str__(self):
        return str(self.pk) #이벤트 타이틀이 제목으로

    class Meta:
        db_table = 'EventList_table'
        verbose_name = '이벤트'
        verbose_name_plural = '이벤트'

#이벤트신청DB
class EventApply(models.Model):
    apply_object = models.ForeignKey(EventList, db_column="EventList_id", on_delete=models.PROTECT, verbose_name='신청하는 이벤트')
    applicant = models.ForeignKey('myapp.User_info', db_column="Menti_id", on_delete=models.PROTECT, verbose_name='지원자 이름')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='신청 날짜/시간')

    #정보제공동의
    agreement = models.BooleanField(default=False, verbose_name='정보제공 동의')

    #간단하게 이벤트 지원 내용
    eventapply_content = models.CharField(max_length=1600, blank=True, null=False, verbose_name='이벤트지원서 내용')

    def __str__(self):
        return str(self.applicant) #지원자가 제목으로

    class Meta:
        db_table = 'EventApply_table'
        verbose_name = '이벤트신청'
        verbose_name_plural = '이벤트신청'


#후기DB
class Review(models.Model):
    review_object = models.ForeignKey(Mentor_info, db_column="Mentor_id", on_delete=models.PROTECT, verbose_name='대상 멘토')
    author = models.ForeignKey('myapp.Menti_info', db_column="Menti_id", on_delete=models.PROTECT, verbose_name='멘티 이름')
    content = models.CharField(max_length=1600, null=False,verbose_name='작성내용')
    reivew_at = models.DateTimeField(auto_now_add=True, verbose_name='작성 날짜/시간')
    review_point_choice = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    )
    review_point =  models.IntegerField(choices = review_point_choice, verbose_name='평점', blank=True, null=True)
    #를 써야하나?

    def __str__(self):
        return str(self.author) #후기작성자가 제목으로

    class Meta:
        db_table = 'Review_table'
        verbose_name = '후기'
        verbose_name_plural = '후기'

class Column(models.Model):
    title = models.CharField(max_length=256, verbose_name='칼럼 제목')
    author = models.ForeignKey('mentoringapp.Mentor_info', db_column="author", on_delete=models.PROTECT, verbose_name='작성한 멘토 ID')
    content = models.TextField(verbose_name='칼럼 내용')
    photo = models.ImageField(upload_to="",blank=True, verbose_name='첨부 이미지')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성 날짜/시간')
    update_at = models.DateTimeField(auto_now=True, verbose_name='칼럼 수정일')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='칼럼 공개일')

    #공개/비공개 기능 함수 (공개 할 때 날짜를 갱신하기 위해)
    def publish(self):
        self.publish_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'column_table'
        verbose_name = '칼럼'
        verbose_name_plural = '칼럼'

# 칼럼 댓글 DB
class ColumnComment(models.Model):
    column = models.ForeignKey(Column, on_delete=models.PROTECT, verbose_name='칼럼 제목')
    user_id = models.ForeignKey('myapp.User_info',
                                on_delete=models.PROTECT,
                                verbose_name='유저 ID')
    comment = models.TextField(verbose_name='댓글 내용')
    commented_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name='작성 날짜/시간')
    
    def __str__(self):
        return str(self.column)
    
    class Meta:
        db_table = 'column_comment_table'
        verbose_name = '칼럼 댓글'
        verbose_name_plural = '칼럼 댓글'

# 질문 DB
class Question(models.Model):
    title = models.CharField(max_length=256, verbose_name='질문 제목')
    author = models.ForeignKey('myapp.Menti_info', db_column="author", on_delete=models.PROTECT, verbose_name='작성한 멘티 ID')
    content = models.TextField(verbose_name='질문 내용')
    photo = models.ImageField(upload_to="", blank=True, verbose_name='첨부 이미지')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성 날짜/시간')
    update_at = models.DateTimeField(auto_now=True, verbose_name='질문 수정일')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'question_table'
        verbose_name = '질문'
        verbose_name_plural = '질문'

# 질문 댓글 DB
class QuestionComment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT, verbose_name='질문 제목')
    user_id = models.ForeignKey('myapp.User_info',
                                on_delete=models.PROTECT,
                                verbose_name='유저 ID')
    comment = models.TextField(verbose_name='댓글 내용')
    commented_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name='작성 날짜/시간')
    
    def __str__(self):
        return str(self.question)
    
    class Meta:
        db_table = 'question_comment_table'
        verbose_name = '질문 댓글'
        verbose_name_plural = '질문 댓글'

# 멘토링 DB -> 현진님 작성
class Mentoring(models.Model):
    title = models.CharField(max_length=128, verbose_name='멘토링 이름')
    mentor = models.ForeignKey(Mentor_info, on_delete=models.PROTECT, db_column="mentor", verbose_name='담당 멘토')
    image = models.ImageField(upload_to="",verbose_name='관련 이미지',blank=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.PROTECT, db_column="lecture", blank=True, null=True, verbose_name='강의')
    # info = models.TextField(null=True,default='X',db_column="info",verbose_name='멘토링 내용',blank=True)
    # info 필드는 해당 멘토링에 대한 간략한 설명을 해주는 필드 넣기. 

    # 멘티님 안녕하세요?? 저는 ~~에서 근무한 땡땡땡 입니다 뭐 이런식으로 필드 하나 넣어놓기
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        db_table = 'mentoring_table'
        verbose_name = '멘토링'
        verbose_name_plural = '멘토링'

# 멘토링 신청 내역 DB
class ApplyMentoring(models.Model):
    mentoring = models.ForeignKey(Mentoring, on_delete=models.PROTECT, db_column="mentoring", verbose_name='신청 멘토링')
    menti = models.ForeignKey('myapp.Menti_info', on_delete=models.PROTECT, db_column="menti", verbose_name='신청 멘티')
    
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        db_table = 'apply_mentoring_table'
        verbose_name = '멘토링 신청 내역'
        verbose_name_plural = '멘토링 신청 내역'