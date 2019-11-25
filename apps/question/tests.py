"""Create your tests here."""
# from django.test import TestCase
from .models import Question, Course, CourseCategory


def publish_questions(limit, course_name):
    """Creating demo questions."""
    level = "Beginner"
    is_multiple = False
    answers = "A"
    course = Course.objects.get(name=course_name)
    for i in range(limit):
        i = str(i)
        question_text = course_name + ": This is question no." + i
        choice1 = "A" + i
        choice2 = "B" + i
        choice3 = "C" + i
        choice4 = "D" + i
        question = Question(question_text=question_text, choice1=choice1, choice2=choice2,
                            choice3=choice3, choice4=choice4, level=level, course=course,
                            is_multiple=is_multiple, answers=answers)
        question.save()
        print(question.id)


def generate_courses():
    """Creating demo courses from the categories."""
    for category in CourseCategory.objects.all():
        Course.objects.create(name=category.name, category=category, is_active=True,
                              is_featured=True)
