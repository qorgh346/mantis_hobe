# Generated by Django 3.2.5 on 2021-08-13 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myapp', '0001_initial'),
        ('mentoringapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(db_column='Menti_id', on_delete=django.db.models.deletion.PROTECT, to='myapp.menti_info', verbose_name='멘티 이름'),
        ),
        migrations.AddField(
            model_name='review',
            name='review_object',
            field=models.ForeignKey(db_column='Mentor_id', on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.mentor_info', verbose_name='대상 멘토'),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.question', verbose_name='질문 제목'),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='myapp.user_info', verbose_name='유저 ID'),
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.PROTECT, to='myapp.menti_info', verbose_name='작성한 멘티 ID'),
        ),
        migrations.AddField(
            model_name='qualification',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to='myapp.user_info'),
        ),
        migrations.AddField(
            model_name='mylecture',
            name='lecture_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.lecture', verbose_name='강의 이름'),
        ),
        migrations.AddField(
            model_name='mylecture',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to='myapp.menti_info', verbose_name='신청한 사람'),
        ),
        migrations.AddField(
            model_name='mentoring',
            name='lecture',
            field=models.ForeignKey(blank=True, db_column='lecture', null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.lecture', verbose_name='강의'),
        ),
        migrations.AddField(
            model_name='mentoring',
            name='mentor',
            field=models.ForeignKey(db_column='mentor', on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.mentor_info', verbose_name='담당 멘토'),
        ),
        migrations.AddField(
            model_name='mentor_info',
            name='user_info_id',
            field=models.ForeignKey(db_column='user_info_id', db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.user_info', verbose_name='멘토 ID'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='mentor_id',
            field=models.ForeignKey(db_column='mentor_id', on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.mentor_info', verbose_name='멘토'),
        ),
        migrations.AddField(
            model_name='favouritelecture',
            name='lecture_title',
            field=models.ForeignKey(db_column='lecture_title', on_delete=django.db.models.deletion.CASCADE, to='mentoringapp.lecture', verbose_name='강의 이름'),
        ),
        migrations.AddField(
            model_name='favouritelecture',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, related_name='fav_user', to='myapp.menti_info', verbose_name='즐겨찾기한 사람'),
        ),
        migrations.AddField(
            model_name='eventlist',
            name='author',
            field=models.ForeignKey(db_column='Mentor_id', on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.mentor_info', verbose_name='멘토 이름'),
        ),
        migrations.AddField(
            model_name='eventapply',
            name='applicant',
            field=models.ForeignKey(db_column='Menti_id', on_delete=django.db.models.deletion.PROTECT, to='myapp.user_info', verbose_name='지원자 이름'),
        ),
        migrations.AddField(
            model_name='eventapply',
            name='apply_object',
            field=models.ForeignKey(db_column='EventList_id', on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.eventlist', verbose_name='신청하는 이벤트'),
        ),
        migrations.AddField(
            model_name='detaillecture',
            name='lecture_title',
            field=models.ForeignKey(db_column='lecture_title', on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.lecture', verbose_name='강의 이름'),
        ),
        migrations.AddField(
            model_name='columncomment',
            name='column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.column', verbose_name='칼럼 제목'),
        ),
        migrations.AddField(
            model_name='columncomment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='myapp.user_info', verbose_name='유저 ID'),
        ),
        migrations.AddField(
            model_name='column',
            name='author',
            field=models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.mentor_info', verbose_name='작성한 멘토 ID'),
        ),
        migrations.AddField(
            model_name='applymentoring',
            name='menti',
            field=models.ForeignKey(db_column='menti', on_delete=django.db.models.deletion.PROTECT, to='myapp.menti_info', verbose_name='신청 멘티'),
        ),
        migrations.AddField(
            model_name='applymentoring',
            name='mentoring',
            field=models.ForeignKey(db_column='mentoring', on_delete=django.db.models.deletion.PROTECT, to='mentoringapp.mentoring', verbose_name='신청 멘토링'),
        ),
    ]
