"""Test packages related modules are managed here."""
from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
from django.forms.models import BaseInlineFormSet
from .models import (CourseCategory, SubscriptionPackage, TimeSlot, Question,
                     Course, QuestionSet, DateSlot, AudioQuestion,
                     PassageQuestion)
import xlrd
from django.utils.safestring import mark_safe


class PassageQuestionInlineFormSet(BaseInlineFormSet):
    """Validate formset data here."""

    def clean(self):
        """Validation on feilds."""
        super(PassageQuestionInlineFormSet, self).clean()
        for form in self.forms:
            if form['question_type'].value() != 'passage':
                raise forms.ValidationError("Please select option value as passage")
            if form['choice1'].value() == '':
                raise forms.ValidationError("Please enter choice1 value")
            if form['choice2'].value() == '':
                raise forms.ValidationError("Please enter choice2 value")
            if form['choice3'].value() == '':
                raise forms.ValidationError("Please enter choice3 value")
            if form['choice4'].value() == '':
                raise forms.ValidationError("Please enter choice4 value")
            if form['answers'].value() == '':
                raise forms.ValidationError("Please enter answer value")


class PassageQuestionInline(admin.TabularInline):
    """Add inline form in passage question."""

    model = Question
    formset = PassageQuestionInlineFormSet
    extra = 0
    show_change_link = True
    template = 'admin/question/AudioQuestion/tabular.html'
    exclude = ['text_answer', 'audio_question', 'technology', 'title']


class PassageQuestionAdmin(admin.ModelAdmin):
    """Passage admin registration with certatin features."""

    class Media:
        """Include extra css."""

        css = {
            'all': ('css/custom_admin.css', )
        }

    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']
    inlines = [PassageQuestionInline]

admin.site.register(PassageQuestion, PassageQuestionAdmin)


class AudioQuestionForm(forms.ModelForm):
    """AudioQuestionForm to restrict feature."""

    class Meta:
        """Include model."""

        model = AudioQuestion
        exclude = ()

    def clean_audio_file(self):
        """Validation for audio feild."""
        string = self.cleaned_data['audio_file']
        lst = ['mp3', 'WAV', 'wav', 'ogg']
        if string.name[-3:] in lst:
            return self.cleaned_data['audio_file']
        else:
            raise forms.ValidationError("Please select the file mp3, wav, ogg extension")


class AudioQuestionInlineFormSet(BaseInlineFormSet):
    """Validate formset data here."""

    def clean(self):
        """Validation on feilds."""
        super(AudioQuestionInlineFormSet, self).clean()
        for form in self.forms:
            if form['question_type'].value() != 'audio':
                raise forms.ValidationError("Please select option value as audio")
            if form['course'].value() != '':
                raise forms.ValidationError("Please select course value")
            if form['choice1'].value() == '':
                raise forms.ValidationError("Please enter choice1 value")
            if form['choice2'].value() == '':
                raise forms.ValidationError("Please enter choice2 value")
            if form['choice3'].value() == '':
                raise forms.ValidationError("Please enter choice3 value")
            if form['choice4'].value() == '':
                raise forms.ValidationError("Please enter choice4 value")
            if form['answers'].value() == '':
                raise forms.ValidationError("Please enter answer value")


class AudioQuestionInline(admin.TabularInline):
    """Add inline form in audioquestion."""

    model = Question
    formset = AudioQuestionInlineFormSet
    extra = 0
    show_change_link = True
    template = 'admin/question/AudioQuestion/tabular.html'
    exclude = ['text_answer', 'passage_question', 'technology', 'title']


class AudioQuestionAdmin(admin.ModelAdmin):
    """AudioQuestion admin with certatin features."""

    class Media:
        """Include extra css."""

        css = {
            'all': ('css/custom_admin.css', )
        }

    form = AudioQuestionForm
    list_display = ['name', 'audio_file', 'description']
    search_fields = ['name']
    list_filter = ['name']
    inlines = [AudioQuestionInline]

admin.site.register(AudioQuestion, AudioQuestionAdmin)


class QuestionAdmin(admin.ModelAdmin):
    """Question admin with certatin features."""

    list_display = ['question_type', 'id', 'get_question_text', 'choice1', 'choice2', 'choice3', 'choice4',
                    'is_multiple', 'course', "answers", 'title']
    search_fields = ['question_text', 'id']
    list_filter = ['question_type', 'is_multiple', 'course']
    change_list_template = "admin/question/Question/change_list.html"

    class Media:
        """Extrs JS."""

        js = ("js/jquery-1.9.1.min.js", 'js/refresh.js',)

    def get_question_text(self, obj):
        """Remove HTML tag."""
        return mark_safe(obj.question_text)
    get_question_text.short_description = 'question_text'

    def get_urls(self):
        """Return question URLs."""
        urls = super(QuestionAdmin, self).get_urls()
        urlpatterns = [
            url('import-question/', self.import_questions_from_xlsx,
                name="import-question")
        ]
        return urlpatterns + urls

    def import_questions_from_xlsx(self, request):
        """Import question from excel file."""
        try:
            input_excel = request.FILES['question-file']
            courses_file = xlrd.open_workbook(file_contents=input_excel.read())

            sh = courses_file.sheet_by_index(0)
            if sh.cell_value(rowx=0, colx=0).strip().lower() == 'question' and \
                    sh.cell_value(rowx=0, colx=1).strip().lower() == 'choice1' and \
                    sh.cell_value(rowx=0, colx=2).strip().lower() == 'choice2' and \
                    sh.cell_value(rowx=0, colx=3).strip().lower() == 'choice3' and \
                    sh.cell_value(rowx=0, colx=4).strip().lower() == 'choice4' and \
                    sh.cell_value(rowx=0, colx=6).strip().lower() == 'is_multiple' and \
                    sh.cell_value(rowx=0, colx=7).strip().lower() == 'courses' and \
                    sh.cell_value(rowx=0, colx=8).strip().lower() == 'level' and \
                    sh.cell_value(rowx=0, colx=5).strip().lower() == 'answer'and \
                    sh.cell_value(rowx=0, colx=9).strip().lower() == 'categories':
                try:
                    for row in range(1, sh.nrows):
                        if sh.cell_value(rowx=row, colx=9) == "":
                            continue
                        CourseCategory.objects.update_or_create(
                            name=sh.cell_value(rowx=row, colx=9).title().strip())
                        if sh.cell_value(rowx=row, colx=7) == "":
                            continue
                        category = CourseCategory.objects.get(name=sh.cell_value(rowx=row, colx=9).title().strip())
                        obj, created = Course.objects.update_or_create(
                            name=sh.cell_value(rowx=row, colx=7).title().strip(),
                            defaults={
                                'name': sh.cell_value(rowx=row, colx=7).title().strip(),
                                'level': sh.cell_value(rowx=row, colx=8).lower().strip(),
                                "category": category
                            }
                        )
                        if sh.cell_value(rowx=row, colx=0) == "":
                            continue
                        course = Course.objects.get(
                            name=sh.cell_value(rowx=row, colx=7).title().strip())
                        is_multiple = True
                        if sh.cell_value(rowx=row, colx=6) == 0.0:
                            is_multiple = False
                        obj, created = Question.objects.update_or_create(
                            question_text=sh.cell_value(rowx=row, colx=0).title().strip(),
                            defaults={
                                'question_type': 'objective',
                                'question_text': sh.cell_value(rowx=row, colx=0).title().strip(),
                                'choice1': sh.cell_value(rowx=row, colx=1).title().strip(),
                                'choice2': sh.cell_value(rowx=row, colx=2).title().strip(),
                                'choice3': sh.cell_value(rowx=row, colx=3).title().strip(),
                                'choice4': sh.cell_value(rowx=row, colx=4).title().strip(),
                                "course": course,
                                "is_multiple": is_multiple,
                                "answers": sh.cell_value(rowx=row, colx=5),
                            }
                        )
                    messages.success(request, 'question successfully imported')
                except Exception as e:
                    messages.error(request, 'Please select course to import question')
                if request.META.get('HTTP_REFERER'):
                    return HttpResponseRedirect(request.META["HTTP_REFERER"])
                else:
                    return HttpResponseRedirect('/admin/question/question/')
            elif sh.cell_value(rowx=0, colx=0).title().strip().lower() == 'question' and \
                    sh.cell_value(rowx=0, colx=1).title().strip().lower() == 'courses' and \
                    sh.cell_value(rowx=0, colx=2).title().strip().lower() == 'level' and \
                    sh.cell_value(rowx=0, colx=3).title().strip().lower() == 'categories':
                try:
                    for row in range(0, sh.nrows):
                        if sh.cell_value(rowx=row, colx=3) == "":
                            continue
                        CourseCategory.objects.update_or_create(
                            name=sh.cell_value(rowx=row, colx=3).title().strip())
                        if sh.cell_value(rowx=row, colx=1) == "":
                            continue
                        category = CourseCategory.objects.get(name=sh.cell_value(rowx=row, colx=3).title().strip())
                        obj, created = Course.objects.update_or_create(
                            name=sh.cell_value(rowx=row, colx=1).title().strip(),
                            defaults={
                                'name': sh.cell_value(rowx=row, colx=1).title().strip(),
                                'level': sh.cell_value(rowx=row, colx=2).lower().strip(),
                                "category": category
                            }
                        )
                        if sh.cell_value(rowx=row, colx=0) == "":
                            continue
                        course = Course.objects.get(
                            name=sh.cell_value(rowx=row, colx=1).title().strip())
                        obj, created = Question.objects.update_or_create(
                            question_text=sh.cell_value(rowx=row, colx=0).title().strip(),
                            defaults={
                                'question_type': 'subjective',
                                'question_text': sh.cell_value(rowx=row, colx=0).title().strip(),
                                "course": course,
                            }
                        )
                    messages.success(request, 'question successfully imported')
                except Exception as e:
                    messages.error(request, 'Please select course to import question')
                if request.META.get('HTTP_REFERER'):
                    return HttpResponseRedirect(request.META["HTTP_REFERER"])
                else:
                    return HttpResponseRedirect('/admin/question/question/')
            elif sh.cell_value(rowx=0, colx=1).strip().lower() == 'question' and \
                    sh.cell_value(rowx=0, colx=0).strip().lower() == 'technology' and \
                    sh.cell_value(rowx=0, colx=2).strip().lower() == 'courses' and \
                    sh.cell_value(rowx=0, colx=3).strip().lower() == 'level' and \
                    sh.cell_value(rowx=0, colx=4).strip().lower() == 'categories':
                try:
                    for row in range(1, sh.nrows):
                        if sh.cell_value(rowx=row, colx=4) == "":
                            continue
                        CourseCategory.objects.update_or_create(
                            name=sh.cell_value(rowx=row, colx=4).title().strip())
                        if sh.cell_value(rowx=row, colx=2) == "":
                            continue
                        category = CourseCategory.objects.get(name=sh.cell_value(rowx=row, colx=4).title().strip())
                        obj, created = Course.objects.update_or_create(
                            name=sh.cell_value(rowx=row, colx=2).title().strip(),
                            defaults={
                                'name': sh.cell_value(rowx=row, colx=2).title().strip(),
                                'level': sh.cell_value(rowx=row, colx=3).lower().strip(),
                                "category": category
                            }
                        )
                        if sh.cell_value(rowx=row, colx=1) == "":
                            continue
                        course = Course.objects.get(
                            name=sh.cell_value(rowx=row, colx=2).title().strip())

                        is_multiple = True
                        if sh.cell_value(rowx=row, colx=3) == 0.0:
                            is_multiple = False
                        obj, created = Question.objects.update_or_create(
                            question_text=sh.cell_value(rowx=row, colx=1).title().strip(),
                            defaults={
                                'question_type': 'technical',
                                'technology': sh.cell_value(rowx=row, colx=0).title().strip(),
                                'question_text': sh.cell_value(rowx=row, colx=1).title().strip(),
                                "course": course,
                            }
                        )
                    messages.success(request, 'question successfully imported')
                except Exception as e:
                    messages.error(request, 'Please select course to import question')
                if request.META.get('HTTP_REFERER'):
                    return HttpResponseRedirect(request.META["HTTP_REFERER"])
                else:
                    return HttpResponseRedirect('/admin/question/question/')
            elif sh.cell_value(rowx=0, colx=0).strip().lower() == 'title' and \
                    sh.cell_value(rowx=0, colx=1).strip().lower() == 'content' and \
                    sh.cell_value(rowx=0, colx=2).strip().lower() == 'no_of_question' and \
                    sh.cell_value(rowx=0, colx=3).strip().lower() == 'question' and \
                    sh.cell_value(rowx=0, colx=4).strip().lower() == 'choice1' and \
                    sh.cell_value(rowx=0, colx=5).strip().lower() == 'choice2' and \
                    sh.cell_value(rowx=0, colx=6).strip().lower() == 'choice3' and \
                    sh.cell_value(rowx=0, colx=7).strip().lower() == 'choice4' and \
                    sh.cell_value(rowx=0, colx=8).strip().lower() == 'answer'and \
                    sh.cell_value(rowx=0, colx=9).strip().lower() == 'is_multiple' and \
                    sh.cell_value(rowx=0, colx=10).strip().lower() == 'courses' and \
                    sh.cell_value(rowx=0, colx=11).strip().lower() == 'level' and \
                    sh.cell_value(rowx=0, colx=12).strip().lower() == 'categories':
                try:
                    for row in range(1, sh.nrows):
                        if sh.cell_value(rowx=row, colx=12) == "":
                            continue
                        CourseCategory.objects.update_or_create(
                            name=sh.cell_value(rowx=row, colx=12).title().strip())
                        if sh.cell_value(rowx=row, colx=10) == "":
                            continue
                        category = CourseCategory.objects.get(name=sh.cell_value(rowx=row, colx=12).title().strip())
                        obj, created = Course.objects.update_or_create(
                            name=sh.cell_value(rowx=row, colx=10).title().strip(),
                            defaults={
                                'name': sh.cell_value(rowx=row, colx=10).title().strip(),
                                'level': sh.cell_value(rowx=row, colx=11).lower().strip(),
                                "category": category
                            }
                        )
                        course = Course.objects.get(
                            name=sh.cell_value(rowx=row, colx=10).title().strip())
                        if sh.cell_value(rowx=row, colx=0).title().strip() != '':
                            no_of_questions = int(sh.cell_value(rowx=row, colx=2))
                            passage_obj = PassageQuestion.objects.create(
                                title=sh.cell_value(rowx=row, colx=0).title().strip(),
                                question_text=sh.cell_value(rowx=row, colx=1),
                                no_of_questions=no_of_questions,
                                course=course,)
                        is_multiple = True
                        if sh.cell_value(rowx=row, colx=9) == 0.0:
                            is_multiple = False
                        obj, created = Question.objects.update_or_create(
                            question_text=sh.cell_value(rowx=row, colx=3).title().strip(),
                            defaults={
                                'question_type': 'passage',
                                'question_text': sh.cell_value(rowx=row, colx=3).title().strip(),
                                'choice1': sh.cell_value(rowx=row, colx=4).title().strip(),
                                'choice2': sh.cell_value(rowx=row, colx=5).title().strip(),
                                'choice3': sh.cell_value(rowx=row, colx=6).title().strip(),
                                'choice4': sh.cell_value(rowx=row, colx=7).title().strip(),
                                "course": course,
                                "is_multiple": is_multiple,
                                "answers": sh.cell_value(rowx=row, colx=8),
                                'passage_question': passage_obj
                            }
                        )
                    messages.success(request, 'question successfully imported')
                except Exception as e:
                    messages.error(request, 'Please select course to import question')
                if request.META.get('HTTP_REFERER'):
                    return HttpResponseRedirect(request.META["HTTP_REFERER"])
                else:
                    return HttpResponseRedirect('/admin/question/question/')
        except Exception as e:
            print('Error ', e)
        messages.error(request, 'Please select correct file to import question')
        return HttpResponseRedirect('/admin/question/question/')

    class Meta:
        """Meta objects."""

        model = Question
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


admin.site.register(Question, QuestionAdmin)


class CourseCategoryAdmin(admin.ModelAdmin):
    """CourseCategory admin registration with certatin features."""

    list_display = ['name', 'parent']
    search_fields = ['name']
    list_filter = ['parent']

admin.site.register(CourseCategory, CourseCategoryAdmin)


class CourseAdmin(admin.ModelAdmin):
    """Course admin registration with certatin features."""

    list_display = ['name', 'category', 'level']
    search_fields = ['name']
    list_filter = ['is_active', 'is_featured', 'level']

admin.site.register(Course, CourseAdmin)


class QuestionSetAdmin(admin.ModelAdmin):
    """QuestionSet admin registration with certatin features."""

    list_display = ['name', 'course']
    search_fields = ['name', 'course']
    list_filter = ['course', 'course__category']
    filter_horizontal = ('scheduled_time_slot',)

    # class Media:
    #     """Extrs JS."""

    #     js = ("js/jquery-1.9.1.min.js", 'js/questionset.js',)

admin.site.register(QuestionSet, QuestionSetAdmin)


class SubscriptionPackageAdmin(admin.ModelAdmin):
    """SubscriptionPackage admin registration with certatin features."""

    list_display = ['id', 'name', 'price', 'discount', 'id']
    search_fields = ['name']
    list_filter = ['is_active', 'is_paid']
    # filter_horizontal = ('scheduled_time_slot',)

admin.site.register(SubscriptionPackage, SubscriptionPackageAdmin)


class TimeSlotAdmin(admin.ModelAdmin):
    """TimeSlot admin registration with certatin features."""

    list_display = ['id', 'slot_name', 'start_time', 'end_time', 'time_duration']
    search_fields = ['slot_name']
    list_filter = ['slot_name']

    def time_duration(self, obj):
        """Custom time format."""
        return str(obj.duration_time // 60) + " hr(s)"

admin.site.register(TimeSlot, TimeSlotAdmin)


class DateSlotAdmin(admin.ModelAdmin):
    """DateSlot admin registration with certatin features."""

    list_display = ['id', 'name', 'start_date', 'end_date', 'number_of_time_slots']
    search_fields = ['name', 'start_date', 'end_date']
    filter_horizontal = ('time_slot',)

    def start_date(self, obj):
        """Get start date."""
        return obj.start_date.strftime("%d-%m-%y")

    def end_date(self, obj):
        """Get end date."""
        return obj.end_date.strftime("%d-%m-%y")

    def number_of_time_slots(self, obj):
        """Get number of available time slots."""
        return obj.time_slot.all().count()

admin.site.register(DateSlot, DateSlotAdmin)
