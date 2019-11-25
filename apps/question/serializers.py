"""Serializer class managed here."""

from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.utils.translation import ugettext_lazy as _

from .models import (
    SubscriptionPackage, QuestionSet, TimeSlot, DateSlot, Question, Course,
    CourseCategory, AudioQuestion, PassageQuestion)

from registration.models import PurchasedPackage


class TimeSlotSerializer(serializers.ModelSerializer):
    """Serializer class for Time slot."""

    class Meta():
        """Meta class."""

        model = TimeSlot
        fields = ['id', 'slot_name', 'start_time', 'end_time', 'duration_time']


class DateSlotSerializer(serializers.ModelSerializer):
    """Serializer class for Date slot."""

    timings = TimeSlotSerializer(source='time_slot', many=True)

    class Meta():
        """Meta class."""

        model = DateSlot
        fields = ['id', 'start_date', 'end_date', 'timings']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer class for Course."""

    class Meta():
        """Meta class."""

        model = Course
        fields = ['name']


class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer class for Course Detail."""

    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        """Category name."""
        return obj.category.name

    class Meta():
        """Meta class."""

        model = Course
        fields = ['id', 'name', 'category', 'level']


class QuestionSetListSerializer(serializers.ModelSerializer):
    """Serializer class for Question Set list."""

    course_detail = CourseSerializer(source='course')

    class Meta():
        """Meta class."""

        model = QuestionSet
        fields = ['id', 'name', 'course_detail',
                  'number_of_objective_questions', 'number_of_audio_questions',
                  'number_of_passage_questions',
                  'number_of_subjective_questions',
                  'number_of_technical_questions',
                  'description', 'scheduled_time_slot']


class QuestionSetDetailSerializer(serializers.ModelSerializer):
    """Serializer class for Time slot."""

    course_detail = CourseDetailSerializer(source='course')
    date_and_time = serializers.SerializerMethodField()

    def get_date_and_time(self, obj):
        """Provide Docstring."""
        return DateSlotSerializer(
            obj.scheduled_time_slot.all(), many=True).data

    class Meta():
        """Meta class."""

        model = QuestionSet
        fields = ['id', 'name', 'course_detail', 'description',
                  'number_of_objective_questions', 'number_of_audio_questions',
                  'number_of_passage_questions',
                  'number_of_subjective_questions',
                  'number_of_technical_questions',
                  'marks_per_objective_question',
                  'marks_per_audio_question',
                  'marks_per_passage_question',
                  'marks_per_subjective_question',
                  'marks_per_technical_question', 'date_and_time']


class SubscriptionPackageListSerializer(serializers.ModelSerializer):
    """Serializer class for subscription package list."""

    description = serializers.SerializerMethodField()
    full_time_duration = serializers.SerializerMethodField()
    question_sets = serializers.SerializerMethodField()

    def get_question_sets(self, obj):
        """Get the question_sets."""
        question_set_detail = {}
        question_set_detail['id'] = obj.question_set.id
        question_set_detail['name'] = obj.question_set.name
        return question_set_detail

    def get_description(self, obj):
        """Get the description."""
        try:
            return obj.instruction
        except AttributeError:
            return ""

    def get_full_time_duration(self, obj):
        """Get the description."""
        try:
            time_in_min = obj.time_duration
            return str(time_in_min // 60) + " hour(s), " + str(time_in_min % 60) + " minutes"
        except AttributeError:
            return ""

    class Meta():
        """Meta class."""

        model = SubscriptionPackage
        fields = ['id', 'time_duration', 'price',
                  'name',
                  'discount', 'description', 'full_time_duration', 'question_sets', 'syllabus']


class QuestionSetListForPackageSerializer(serializers.ModelSerializer):
    """Serializer class for Time slot."""

    class Meta():
        """Meta class."""

        model = QuestionSet
        fields = ['name', 'id', 'marks_per_question']


class SubscriptionPackageSerializer(serializers.ModelSerializer):
    """Serializer class for subscription package details."""

    que_set = QuestionSetListForPackageSerializer(source='question_set')
    additional_instructions = serializers.CharField(source='instruction')
    time_duration = serializers.SerializerMethodField()
    full_time_duration = serializers.SerializerMethodField()

    def get_time_duration(self, obj):
        """Get the description."""
        try:
            return obj.question_set.scheduled_time_slot.first().time_slot.first().duration_time
        except AttributeError:
            return ""

    def get_full_time_duration(self, obj):
        """Get the description."""
        try:
            time_in_min = obj.question_set.scheduled_time_slot.first().time_slot.first().duration_time
            return str(time_in_min // 60) + " hour(s), " + str(time_in_min % 60) + " minutes"
        except AttributeError:
            return ""

    class Meta():
        """Meta class."""

        model = SubscriptionPackage
        fields = ['id', 'price', 'additional_instructions', 'name', 'discount', 'description',
                  'time_duration', 'full_time_duration', 'que_set']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer class for Time slot."""

    choices = serializers.SerializerMethodField()

    def get_choices(self, obj):
        """Choice for an answer."""
        choices = {
            'choice1': obj.choice1,
            'choice2': obj.choice2,
            'choice3': obj.choice3,
            'choice4': obj.choice4,
        }
        return choices

    class Meta():
        """Meta class."""

        model = Question
        fields = ['id', 'question_text', 'choices', 'is_multiple']


class ChildCategoryListSerializer(serializers.ModelSerializer):
    """Serializer for listing course child category."""

    class Meta():
        """Meta class."""

        model = CourseCategory
        fields = ['id', 'name']


class CategoryListSerializer(serializers.ModelSerializer):
    """Serializer for listing course category."""

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        """Get the filtered childrens."""
        filtered_courses_id = self.context.get('filtered_courses_id')
        if filtered_courses_id:
            children = obj.get_children().filter(pk__in=filtered_courses_id)
        else:
            children = obj.get_children()
        return ChildCategoryListSerializer(children, many=True).data

    class Meta():
        """Meta class."""

        model = CourseCategory
        fields = ['id', 'name', 'children']


class ObjectiveQuestionListSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    choices = serializers.SerializerMethodField()
    marks = serializers.SerializerMethodField()

    def get_choices(self, obj):
        """Choice for an answer."""
        choices = {
            'choice1': obj.choice1,
            'choice2': obj.choice2,
            'choice3': obj.choice3,
            'choice4': obj.choice4,
        }
        return choices

    def get_marks(self, obj):
        """Choice for an answer."""
        marks = self.context.get('marks_per_sub_question')
        return float("{0:.2f}".format(marks))

    class Meta():
        """Provide Docstring."""

        model = Question
        fields = ['id', 'question_text', 'choices', 'marks']


class ObjectiveQuestionSerializer(serializers.ModelSerializer):
    """Qbjective question set serializer class."""

    class Meta():
        """Provide Docstring."""

        model = QuestionSet
        fields = ['id', 'course_detail', 'name', 'Number_of_questions']

    def to_representation(self, obj):
        """Provide Docstring."""
        context = {'marks_per_sub_question': obj.marks_per_question}
        question_list = obj.questions()
        return {
            'id': obj.id,
            'name': obj.name,
            'Number_of_questions': obj.Number_of_questions,
            'question_list': ObjectiveQuestionListSerializer(
                question_list, many=True, context=context).data
        }


class AudioQuestionListSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    class Meta():
        """Provide Docstring."""

        model = AudioQuestion
        fields = ['id', 'audio_file', 'name', 'description']

    def to_representation(self, obj):
        """Method to_representation."""
        marks_per_audio = self.context.get('marks_per_audio')
        audio_sub_questions_count = obj.no_of_questions
        question_list = obj.sub_questions()[:audio_sub_questions_count]
        marks_per_sub_question = marks_per_audio / audio_sub_questions_count
        context = {'marks_per_sub_question': marks_per_sub_question}
        return {
            'id': obj.id,
            'name': obj.name,
            'marks_of_this_question': marks_per_audio,
            'file_url': obj.audio_file.url if obj.audio_file.url else "",
            'question_list': ObjectiveQuestionListSerializer(
                question_list, many=True, context=context).data
        }


class AudioQuestionSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    class Meta():
        """Provide Docstring."""

        model = QuestionSet
        fields = ['id', 'name', 'Number_of_questions']

    def to_representation(self, obj):
        """Provide Docstring."""
        question_list = AudioQuestion.questions()[:obj.Number_of_questions]
        context = {'marks_per_audio': obj.marks_per_question}
        return {
            'id': obj.id,
            'name': obj.name,
            'Number_of_questions': obj.Number_of_questions,
            'question_list': AudioQuestionListSerializer(
                question_list, many=True, context=context).data
        }


class PassageQuestionListSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    class Meta():
        """Provide Docstring."""

        model = PassageQuestion
        fields = ['id']

    def to_representation(self, obj):
        """Method to_representation."""
        marks_per_passage = self.context.get('marks_per_passage')
        passage_sub_questions_count = obj.no_of_questions
        question_list = obj.sub_questions()[:passage_sub_questions_count]
        marks_per_sub_question = marks_per_passage / passage_sub_questions_count
        context = {'marks_per_sub_question': marks_per_sub_question}
        return {
            'id': obj.id,
            'title': obj.title,
            'question_text': obj.question_text,
            'marks_of_this_question': marks_per_passage,
            'question_list': ObjectiveQuestionListSerializer(
                question_list, many=True, context=context).data
        }


class PassageQuestionSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    class Meta():
        """Provide Docstring."""

        model = QuestionSet
        fields = ['id']

    def to_representation(self, obj):
        """Provide Docstring."""
        question_list = PassageQuestion.questions()[:obj.Number_of_questions]
        context = {'marks_per_passage': obj.marks_per_question}
        return {
            'id': obj.id,
            'name': obj.name,
            'Number_of_questions': obj.Number_of_questions,
            'marks_per_question': obj.marks_per_question,
            'question_list': PassageQuestionListSerializer(
                question_list, many=True, context=context).data
        }


class SubjectiveQuestionListSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    marks = serializers.SerializerMethodField()

    class Meta():
        """Provide Docstring."""

        model = Question
        fields = ['id', 'question_text', 'title', 'marks']

    def get_marks(self, obj):
        """Choice for an answer."""
        return self.context.get('marks_per_question')


class TechQuestionListSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    marks = serializers.SerializerMethodField()

    class Meta():
        """Provide Docstring."""

        model = Question
        fields = ['id', 'question_text', 'title', 'marks', 'technology']

    def get_marks(self, obj):
        """Choice for an answer."""
        return self.context.get('marks_per_question')


class SubjectiveQuestionSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    class Meta():
        """Provide Docstring."""

        model = QuestionSet
        fields = ['id']

    def to_representation(self, obj):
        """Provide Docstring."""
        context = {'marks_per_question': obj.marks_per_question}
        question_list = Question.objects.filter(
            question_type="subjective")[:obj.Number_of_questions]
        return {
            'id': obj.id,
            'Number_of_questions': obj.Number_of_questions,
            'marks_per_question': obj.marks_per_question,
            'question_list': SubjectiveQuestionListSerializer(
                question_list, many=True, context=context).data
        }


class TechnicalQuestionSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    class Meta():
        """Provide Docstring."""

        model = QuestionSet
        fields = ['id']

    def to_representation(self, obj):
        """Provide Docstring."""
        context = {'marks_per_question': obj.marks_per_question}
        question_list = Question.objects.filter(
            question_type="technical")[:obj.Number_of_questions]
        return {
            'id': obj.id,
            'Number_of_questions': obj.Number_of_questions,
            'marks_per_question': obj.marks_per_question,
            'question_list': TechQuestionListSerializer(
                question_list, many=True, context=context).data
        }


class SubscriptionPackageAllQuestionSerializer(serializers.ModelSerializer):
    """Serializer class for Question Set Detail."""

    class Meta():
        """Meta class."""

        model = SubscriptionPackage
        fields = ['id']

    def to_representation(self, obj):
        """Method to_representation."""
        passage_question_set_data = {}
        objective_question_set_data = {}
        subjective_question_set_data = {}
        audio_question_set_data = {}
        technical_question_set_data = {}
        for question_set in obj.question_set.all():
            if question_set.question_type == 'passage':
                passage_question_set_data = PassageQuestionSerializer(
                    question_set).data
            if question_set.question_type == 'objective':
                objective_question_set_data = ObjectiveQuestionSerializer(
                    question_set).data
            if question_set.question_type == 'audio':
                audio_question_set_data = AudioQuestionSerializer(
                    question_set).data
            if question_set.question_type == 'subjective':
                subjective_question_set_data = SubjectiveQuestionSerializer(
                    question_set).data
            if question_set.question_type == 'technical':
                technical_question_set_data = TechnicalQuestionSerializer(
                    question_set).data
        return {
            "id": obj.id,
            "price": obj.price,
            "name": obj.name,
            "description": obj.description,
            "time_duration": obj.time_duration,
            "other_details": self.get_purchased_package_details(),
            "full_time_duration": self.get_full_time_duration(obj.time_duration),
            "audio_question_set": audio_question_set_data,
            "subjective_question_set": subjective_question_set_data,
            "passage_question_set": passage_question_set_data,
            "objective_question_set": objective_question_set_data,
            "technical_question_set": technical_question_set_data,
        }

    def get_full_time_duration(self, time_in_min):
        """Get the description."""
        return str(time_in_min // 60) + " hour(s), " + str(time_in_min % 60) + " minutes"

    def get_purchased_package_details(self):
        """Purchased package general details."""
        package = self.context.get("purchased_package")
        if package:
            return {
                "date": package.date,
                "start_time": package.test_time.start_time,
                "end_time": package.test_time.end_time,

            }
        else:
            return "wrong package id provided"


class SubscriptionPackageDetailSerializer(serializers.ModelSerializer):
    """Serializer class for Question Set Detail."""

    question_sets = serializers.SerializerMethodField()

    def get_question_sets(self, obj):
        """Display data related question_set."""
        return QuestionSetDetailSerializer(obj.question_set).data

    class Meta():
        """Meta class."""

        model = SubscriptionPackage
        fields = ['id', 'instruction', 'syllabus', 'discount',
                  'price', 'time_duration', 'name', 'question_sets']


class QuestionSetSerializer(serializers.ModelSerializer):
    """Serializer class for Question Set list."""

    course_detail = CourseSerializer(source='course')
    total_questions = serializers.SerializerMethodField()

    def get_total_questions(self, obj):
        """Provide Docstring."""
        total = obj.number_of_objective_questions + obj.number_of_audio_questions + obj.number_of_passage_questions + obj.number_of_subjective_questions + obj.number_of_technical_questions
        return total

    class Meta():
        """Meta class."""

        model = QuestionSet
        fields = ['id', 'name', 'course_detail',
                  'number_of_objective_questions', 'number_of_audio_questions',
                  'number_of_passage_questions',
                  'number_of_subjective_questions',
                  'number_of_technical_questions', 'total_questions',
                  'description']


class PurchasedPackageDetailSerializer(serializers.ModelSerializer):
    """Serializer class for Question Set Detail."""

    question_set_details = serializers.SerializerMethodField()
    package = SubscriptionPackageListSerializer(source='subscription_package')
    date_and_time = serializers.SerializerMethodField()
    instruction = serializers.SerializerMethodField()

    def get_question_set_details(self, obj):
        """Display question_set detail."""
        return QuestionSetSerializer(obj.subscription_package.question_set).data

    def get_instruction(self, obj):
        """Provide Docstring."""
        return obj.subscription_package.instruction

    def get_date_and_time(self, obj):
        """Provide Docstring."""
        start_time = obj.test_time.start_time
        end_time = obj.test_time.end_time
        date = obj.date
        return {
            'start_time': start_time,
            'end_time': end_time,
            'date': date,
            'full_duration_time': self.get_full_time_duration(obj),
            'duration_time': self.get_time_duration(obj)
        }

    def get_full_time_duration(self, obj):
        """Get the description."""
        try:
            time_in_min = obj.test_time.duration_time

            return str(time_in_min // 60) + " hour(s), " + str(time_in_min % 60) + " minutes"
        except AttributeError:
            return ""

    def get_time_duration(self, obj):
        """Get the description."""
        try:
            return obj.test_time.duration_time
        except AttributeError:
            return ""

    class Meta():
        """Meta class."""

        model = PurchasedPackage
        fields = ['id', 'package',
                  'instruction', 'question_set_details', 'date_and_time']

class AllObjectiveQuestionSerializer(serializers.ModelSerializer):
    """Serializer class for Time slot."""

    choices = serializers.SerializerMethodField()
    marks = serializers.SerializerMethodField()

    def get_marks(self, obj):
        """Choice for an answer."""
        marks = self.context.get('marks_per_objective_question')
        return float("{0:.2f}".format(marks))

    def get_choices(self, obj):
        """Choice for an answer."""
        choices = {
            'A': obj.choice1,
            'B': obj.choice2,
            'C': obj.choice3,
            'D': obj.choice4,
        }
        return choices

    class Meta():
        """Meta class."""

        model = Question
        fields = ['id', 'question_text', 'choices', 'is_multiple', 'marks']


class AllsubjectiveQuestionSerializer(serializers.ModelSerializer):
    """Serializer class for Time slot."""

    marks = serializers.SerializerMethodField()

    def get_marks(self, obj):
        """Choice for an answer."""
        marks = self.context.get('marks_per_subjective_question')
        return float("{0:.2f}".format(marks))

    class Meta():
        """Meta class."""

        model = Question
        fields = ['id', 'question_text', 'marks']


class AllTechnicalQuestionSerializer(serializers.ModelSerializer):
    """Serializer class for Time slot."""

    marks = serializers.SerializerMethodField()

    def get_marks(self, obj):
        """Choice for an answer."""
        marks = self.context.get('marks_per_technical_question')
        return float("{0:.2f}".format(marks))

    class Meta():
        """Meta class."""

        model = Question
        fields = ['id', 'question_text', 'technology', 'marks']


class SubAudioQuestionSerializer(serializers.ModelSerializer):
    """Serializer class for Time slot."""

    choices = serializers.SerializerMethodField()
    marks = serializers.SerializerMethodField()

    def get_marks(self, obj):
        """Choice for an answer."""
        marks = self.context.get('marks_per_sub_question')
        return float("{0:.2f}".format(marks))

    def get_choices(self, obj):
        """Choice for an answer."""
        choices = {
            'choice1': obj.choice1,
            'choice2': obj.choice2,
            'choice3': obj.choice3,
            'choice4': obj.choice4,
        }
        return choices

    class Meta():
        """Meta class."""

        model = Question
        fields = ['id', 'question_text', 'choices', 'is_multiple', 'marks']


class SubPassageQuestionSerializer(serializers.ModelSerializer):
    """Serializer class for Time slot."""

    choices = serializers.SerializerMethodField()
    marks = serializers.SerializerMethodField()

    def get_marks(self, obj):
        """Choice for an answer."""
        marks = self.context.get('marks_per_sub_question')
        return float("{0:.2f}".format(marks))

    def get_choices(self, obj):
        """Choice for an answer."""
        choices = {
            'choice1': obj.choice1,
            'choice2': obj.choice2,
            'choice3': obj.choice3,
            'choice4': obj.choice4,
        }
        return choices

    class Meta():
        """Meta class."""

        model = Question
        fields = ['id', 'question_text', 'choices', 'is_multiple', 'marks']


class AllAudioQuestionListSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    class Meta():
        """Provide Docstring."""

        model = AudioQuestion
        fields = ['id', 'audio_file']

    def to_representation(self, obj):
        """Method to_representation."""
        marks_per_audio = self.context.get('marks_per_audio_question')
        audio_sub_questions_count = obj.no_of_questions
        marks_per_sub_question = marks_per_audio / audio_sub_questions_count
        context = {'marks_per_sub_question': marks_per_sub_question}
        question_list = obj.sub_questions()[:audio_sub_questions_count]
        return {
            'id': obj.id,
            'file_url': obj.audio_file.url if obj.audio_file.url else "",
            'question_list': SubAudioQuestionSerializer(
                question_list, many=True, context=context).data,
        }


class AllPassageQuestionListSerializer(serializers.ModelSerializer):
    """Provide Docstring."""

    class Meta():
        """Provide Docstring."""

        model = PassageQuestion
        fields = ['id', 'question_text']

    def to_representation(self, obj):
        """Method to_representation."""
        marks_per_passage = self.context.get('marks_per_passage_question')
        passage_sub_questions_count = obj.no_of_questions
        marks_per_sub_question = marks_per_passage / passage_sub_questions_count
        context = {'marks_per_sub_question': marks_per_sub_question}
        question_list = obj.sub_questions()[:passage_sub_questions_count]
        return {
            'id': obj.id,
            'question_text': obj.question_text,
            'question_list': SubPassageQuestionSerializer(
                question_list, many=True, context=context).data
        }


class CourseSerializer(serializers.ModelSerializer):
    """Serializer class for Course."""

    class Meta():
        """Meta class."""

        model = Course
        fields = ['id', 'name']


class SearchCourseSerializer(serializers.ModelSerializer):
    """Serializer for listing course category."""

    children = serializers.SerializerMethodField()
    # parent = serializers.SerializerMethodField()

    def get_children(self, obj):
        """Get the filtered childrens."""
        filtered_courses_id = self.context.get('filtered_courses_id')
        filtered_category_id = self.context.get('filtered_category_id')
        subject = self.context.get('subject')
        if filtered_category_id:
            if subject in obj.name.lower():
                children = obj.course.all()
            else:
                children = obj.course.all().filter(name__icontains=subject)
        elif filtered_courses_id:
            children = obj.course.all().filter(pk__in=filtered_courses_id)
        else:
            children = obj.course.all()
        return CourseSerializer(children, many=True).data

    class Meta():
        """Meta class."""

        model = CourseCategory
        fields = ['id', 'name', 'children']


class TestPackageDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail of purchased package."""

    booking_date = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    duration_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    syllabus_pdf = serializers.SerializerMethodField()

    def get_syllabus_pdf(self, obj):
        """Get syllabus of test."""
        return obj.subscription_package.syllabus.url

    def get_booking_date(self, obj):
        """Get booking date of test."""
        return obj.start_date.date()

    def get_start_time(self, obj):
        """Get start time of test."""
        return obj.test_time.start_time

    def get_end_time(self, obj):
        """Get end time of test."""
        return obj.test_time.end_time

    def get_subscription(self, obj):
        """Get name of test."""
        return obj.subscription_package.name

    def get_duration_time(self, obj):
        """Get duration time of test."""
        start_time = obj.test_time.start_time.strftime('%H')
        end_time = obj.test_time.end_time.strftime('%H')
        return (int(end_time) - int(start_time)) * 60

    class Meta():
        """Class meta."""

        model = PurchasedPackage
        fields = ['id', 'booking_date', 'date', 'subscription', 'start_time', 'end_time', 'duration_time', 'syllabus_pdf']
