"""Tests are managed here."""
from ckeditor.fields import RichTextField
from registration.models import BaseModel
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import datetime
from functools import reduce


class CourseCategory(MPTTModel):
    """Course category are managed here."""

    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        """Class definition."""

        order_insertion_by = ['name']

    def __str__(self):
        """Model Representation."""
        return str(self.name)


class Course(BaseModel):
    """Course model are managed here."""

    LEVEL = (
        ('-----', '-----'),
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    )
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=15, choices=LEVEL, default='-----')
    image = models.ImageField(upload_to="course_images", blank=True, null=True)
    category = models.ForeignKey(
        CourseCategory, on_delete=models.SET_NULL, related_name='course', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        """Model Representation."""
        return str(self.name)


class AudioQuestion(BaseModel):
    """Audio files are managed here."""

    audio_file = models.FileField(blank=True, null=True, upload_to='audiofile')
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    # marks_per_question = models.IntegerField(default=0)
    no_of_questions = models.IntegerField(default=5)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='audios', null=True, blank=True)

    def __str__(self):
        """Model Representation."""
        return str(self.name)

    @classmethod
    def questions(cls):
        """Return random list of questions."""
        return cls.objects.filter().order_by('?')

    def sub_questions(self):
        """Return random list of sub questions."""
        return self.audio_questions.all().order_by('?')


class PassageQuestion(BaseModel):
    """Audio files are managed here."""

    title = models.CharField(max_length=200, null=True, blank=True)
    question_text = RichTextField()
    # marks_per_question = models.IntegerField(default=0)
    no_of_questions = models.IntegerField(default=5)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='passages', null=True, blank=True)

    def __str__(self):
        """Model Representation."""
        return str(self.title)

    @classmethod
    def questions(cls):
        """Return random list of questions."""
        return cls.objects.filter().order_by('?')

    def sub_questions(self):
        """Return random list of sub questions."""
        return self.passage_questions.all().order_by('?')


class Question(BaseModel):
    """Questions and answers are managed here."""

    TYPE = (
        ('-----', '-----'),
        ('audio', 'Audio'),
        ('objective', 'Objective'),
        ('subjective', 'Subjective'),
        ('passage', 'Passage'),
        ('technical', 'Technical')
    )
    Technology = (
        ('-----', '-----'),
        ('c', 'C'),
        ('c++', 'C++'),
        ('java', 'Java'),
        ('python', 'Python'),
        ('javascript', 'Javascript')
    )
    question_type = models.CharField(max_length=15, choices=TYPE, default='-----')
    technology = models.CharField(max_length=15, choices=Technology, default='-----')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    audio_question = models.ForeignKey(
        AudioQuestion, on_delete=models.CASCADE, related_name='audio_questions', null=True, blank=True)
    passage_question = models.ForeignKey(
        PassageQuestion, on_delete=models.CASCADE, related_name='passage_questions', null=True, blank=True)
    question_text = RichTextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    is_multiple = models.BooleanField(default=False)
    choice1 = models.CharField(max_length=200, null=True, blank=True)
    choice2 = models.CharField(max_length=200, null=True, blank=True)
    choice3 = models.CharField(max_length=200, null=True, blank=True)
    choice4 = models.CharField(max_length=200, null=True, blank=True)
    answers = models.CharField(max_length=200, null=True, blank=True)
    text_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        """Model Representation."""
        return self.question_text

    def check_answer(self, data, attempted_test=None):
        """Checking answer of a particular question and add to the attempted questions model."""
        from student.models import AttemptedQuestion
        result = False
        marks = 0
        is_correct = False
        given_answer = ''
        if self.question_type in ["audio", "objective", "passage"]:
            given_answer = data.get("given_answer_choice")
            if self.is_multiple:
                if self.answers.split(",") == sorted(given_answer):
                    result = True
                    marks = data.get('marks')
                    is_correct = True
                given_answer = ",".join(given_answer)
            else:
                if given_answer[0] == self.answers:
                    result = True
                    marks = data.get('marks')
                    is_correct = True
                given_answer = given_answer[0]

        elif self.question_type in ["subjective", "technical"]:
            given_answer = data.get("given_answer")

        if attempted_test:
            AttemptedQuestion.objects.create(
                attempted_test=attempted_test, obtained_mark=marks,
                question=self, given_answer=given_answer, is_correct=is_correct)
        return result

    class Meta:
        """Defining the order of posts."""

        ordering = ['-updated_at']


class TimeSlot(BaseModel):
    """Time Slots are managed here."""

    slot_name = models.CharField(max_length=150, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    @property
    def duration_time(self):
        """Saving the duration time."""
        end_time = datetime.datetime.combine(datetime.date.today(), self.end_time)
        start_time = datetime.datetime.combine(datetime.date.today(), self.start_time)
        time_difference = end_time - start_time
        return time_difference.total_seconds() / 60

    def __str__(self):
        """Model Representation."""
        return str(self.start_time.strftime('%H:%M'))


class DateSlot(BaseModel):
    """Date Slots are managed here."""

    name = models.CharField(max_length=150, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    time_slot = models.ManyToManyField(TimeSlot, related_name='dates')

    def __str__(self):
        """Model Representation."""
        return str(self.name)


class QuestionSet(BaseModel):
    """Questions sets are managed here."""

    TYPE = (
        ('-----', '-----'),
        ('audio', 'Audio'),
        ('objective', 'Objective'),
        ('subjective', 'Subjective'),
        ('passage', 'Passage'),
        ('technical', 'Technical')
    )
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, related_name='question_sets', null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    number_of_objective_questions = models.IntegerField(default=0)
    number_of_audio_questions = models.IntegerField(default=0)
    number_of_passage_questions = models.IntegerField(default=0)
    number_of_subjective_questions = models.IntegerField(default=0)
    number_of_technical_questions = models.IntegerField(default=0)
    marks_per_objective_question = models.IntegerField(default=0)
    marks_per_audio_question = models.IntegerField(default=0)
    marks_per_passage_question = models.IntegerField(default=0)
    marks_per_subjective_question = models.IntegerField(default=0)
    marks_per_technical_question = models.IntegerField(default=0)
    scheduled_time_slot = models.ManyToManyField(
        DateSlot, related_name='question_sets')

    def __str__(self):
        """Model Representation."""
        return str(self.name)

    class Meta:
        """Defining the order of posts."""

        ordering = ['-updated_at']

    def questions(self):
        """Return random list of objective questions."""
        questions = {}
        all_question = Question.objects.filter(course=self.course)
        questions['objective_questions'] = all_question.filter(
            question_type='objective').order_by('?')[:self.number_of_objective_questions]
        questions['audio_questions'] = AudioQuestion.objects.filter(
            course=self.course).order_by('?')[:self.number_of_audio_questions]
        questions['passage_questions'] = PassageQuestion.objects.filter(
            course=self.course).order_by('?')[:self.number_of_passage_questions]
        questions['subjective_questions'] = all_question.filter(
            question_type='subjective').order_by('?')[:self.number_of_subjective_questions]
        questions['technical_questions'] = all_question.filter(
            question_type='technical').order_by('?')[:self.number_of_technical_questions]
        return questions


class SubscriptionPackage(BaseModel):
    """Test Packages are managed here."""

    price = models.FloatField(default=0)
    question_set = models.ForeignKey(
        QuestionSet, related_name='subscription_packages', on_delete=models.CASCADE, blank=True, null=True)
    instruction = models.TextField(blank=True, null=True)
    syllabus = models.FileField(blank=True, null=True, upload_to='test_syllabus')
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    discount = models.FloatField(default=0)
    time_duration = models.IntegerField(default=0)

    def __str__(self):
        """Model Representation."""
        return self.name

    class Meta:
        """Defining the order of posts."""

        ordering = ['-updated_at']

    def question_set_all_details(self):
        """Provide Docstring."""
        from functools import reduce
        data = {
            'passage_questions': 0,
            'objective_questions': 0,
            'subjective_questions': 0,
            'audio_questions': 0,
            'technical_questions': 0,
        }
        for question_set in self.question_set.all():
            data['passage_questions'] = question_set.number_of_passage_questions
            data["objective_questions"] = question_set.number_of_objective_questions
            data['audio_questions'] = question_set.number_of_audio_questions
            data['subjective_questions'] = question_set.number_of_subjective_questions
            data['technical_questions'] = question_set.number_of_objective_questions
        return data, reduce(lambda a, b: a + b, data.values())

    def total_questions(self):
        """Get all questions count."""
        questions_count = (question_set.Number_of_questions for question_set in self.question_set.all())
        return reduce(lambda a, b: a + b, questions_count)
