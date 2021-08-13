from django.db import models
from django.utils import timezone

# Create your models here.
# 유저 DB, 멘티 DB, 캐시 DB, 결제 DB

# 유저 DB
class User_info(models.Model): 
    user_id = models.CharField(primary_key=True,max_length=256,null=False,verbose_name='아이디')
    user_pw = models.CharField(max_length=1000, null=False, verbose_name='비밀번호')
    user_name = models.CharField(max_length=256, null=False, verbose_name='성명')
    user_email = models.EmailField(max_length=256, unique=True, null=False, verbose_name='이메일')
    user_register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')
    user_phone_number = models.IntegerField(unique=True, null=False, verbose_name='전화번호')
    user_RRN1 = models.IntegerField(unique=True, null=False, verbose_name='주민번호 앞자리')
    user_RRN2 = models.IntegerField(unique=True, null=False, verbose_name='주민번호 뒷자리')
    user_certification = models.ImageField(blank=True, null=False, upload_to='', verbose_name='본인증명서')
    user_certification_check = models.BooleanField(default=False, verbose_name='인증여부')
    user_cash = models.IntegerField(default=0, verbose_name='잔액')
    user_school = models.CharField(max_length=256, default='경기대학교', verbose_name='학력')
    
    ROLE = (
        ('멘토', '멘토'),
        ('멘티', '멘티'),
    )
    user_role = models.CharField(max_length=16,
                             choices=ROLE,
                             verbose_name='멘토/멘티',
                             blank=True)

    def __str__(self):
        # 수정?? id로??
        return self.user_name
    
    class Meta:
        db_table = 'user_table'
        verbose_name = '유저'
        verbose_name_plural = '유저'

# 멘티 DB
class Menti_info(models.Model):
    #pk = 1,2,3,4,5
    user_info_id = models.ForeignKey(User_info,on_delete=models.CASCADE,related_name="user_menti" ,
                                                    db_column="user_info_id", verbose_name='멘티 ID',db_constraint=False,null=True)
    contents = models.TextField(blank=True, null=True, verbose_name='멘티 이력')

    class Meta:
        db_table = 'menti_table'
        verbose_name = '멘티'
        verbose_name_plural = '멘티'

    def __str__(self):
        return str(self.user_info_id)

# 캐시 DB
class Cash(models.Model):
    payer = models.CharField(max_length=256, verbose_name='입금자명')
    user_id = models.OneToOneField(User_info, db_column="user_id", on_delete=models.PROTECT, verbose_name='유저 ID')
    cash_charge = models.IntegerField(default=0, verbose_name='충전 금액')
    cash_at = models.DateTimeField(auto_now_add=True, verbose_name='충전 날짜/시간') #충전날짜, 시간
    success_true_false =  models.BooleanField(default=False, verbose_name='충전 성공 여부')
    
    def __str__(self):
        return self.payer

    class Meta:
        db_table = 'cash_table'
        verbose_name = '캐시'
        verbose_name_plural = '캐시'

# 결제 DB
class Payment(models.Model):
    user_id = models.ForeignKey(User_info, db_column="user_id", on_delete=models.PROTECT, verbose_name='유저 ID',db_constraint=False,null=True) #유저 아이디
    payment_at = models.DateTimeField(auto_now_add=True, verbose_name='결제 날짜/시간')
    sum = models.ForeignKey('mentoringapp.Lecture', db_column="sum", on_delete=models.PROTECT, verbose_name='합계')

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = 'payment_table'
        verbose_name = '결제'
        verbose_name_plural = '결제'