from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify

from sortedm2m.fields import SortedManyToManyField

from accounts.models import GRADE_LEVEL_MAX_LENGTH, GradeLevels


def user_upload_directory(instance, filename):
    """Return the upload directory for a given File (should have an owner)."""
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

OTHER = 0
STUDENT_HANDOUT = 1
TEACHER_REFERENCE = 2
SLIDES = 3
CODE = 4
SCHEMATIC = 5

FILE_TYPES = (
    (OTHER, "Other"),
    (STUDENT_HANDOUT, "Student handout"),
    (TEACHER_REFERENCE, "Teacher reference"),
    (SLIDES, "Slides"),
    (CODE, "Code"),
    (SCHEMATIC, "Schematic"),
)

class LessonResource(models.Model):
    # The original filename - or whatever is displayed.
    name = models.CharField(max_length=60)

    # The mime type of the uploaded document
    mime_type = models.CharField(max_length=129, blank=True)

    # The semantic type of document (from options above)
    semantic_type = models.SmallIntegerField(choices=FILE_TYPES, default=OTHER)

    # The uploader of the file, should only be null if a user is deleted.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    # The actual reference to the file on the filesystem.
    file = models.FileField(upload_to=user_upload_directory)

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        semantic_type_str = FILE_TYPES[0][1]
        for file_type in FILE_TYPES:
            if file_type[0] == self.semantic_type:
                semantic_type_str = file_type[1]
                break
        return '(LessonResource ' + str(self.id) + ') ' + self.name + ' (' + semantic_type_str + ')'

class LessonResourceExternalLink(models.Model):
    name = models.CharField(max_length=60)
    semantic_type = models.SmallIntegerField(choices=FILE_TYPES, default=OTHER)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    link = models.URLField(max_length=400)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        semantic_type_str = FILE_TYPES[0][1]
        for file_type in FILE_TYPES:
            if file_type[0] == self.semantic_type:
                semantic_type_str = file_type[1]
                break
        return '(LessonResourceExternalLink ' + str(self.id) + ') ' + self.name + ' (' + semantic_type_str + ')'


class Material(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return '(Material) ' + self.name


class LessonPlan(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=120, unique=True)
    summary = models.CharField(max_length=2000, blank=True)
    grade_level = models.CharField(max_length=GRADE_LEVEL_MAX_LENGTH, choices=GradeLevels)

    total_prep_time = models.DurationField()
    num_classes = models.IntegerField()
    single_class_time = models.DurationField()

    # Chromebooks only support web-only curriculums!
    web_only = models.BooleanField()

    # uploaded files!
    resources = models.ManyToManyField(LessonResource, blank=True)
    resource_links = models.ManyToManyField(LessonResourceExternalLink, blank=True)

    materials = SortedManyToManyField(Material, blank=True)

    # enable feedback?
    feedback_enabled = models.BooleanField(default=True)

    # Temporarily removed while this is implemented
    # Notify this user when someone leaves feedback?
    # notify_of_feedback = models.BooleanField(default=True)

    # Drafts are available via detailed view, but not listed with all published lesson plans.
    draft = models.BooleanField(default=False)

    last_modified_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse('detail-lesson-plan', kwargs={
            'pk': self.id,
            'slug': self.slug
        })

    def __str__(self):
        return '(LessonPlan) ' + self.title

class FiveStarRatingField(models.SmallIntegerField):
    ratings = (
        (1, "One star"),
        (2, "Two stars"),
        (3, "Three stars"),
        (4, "Four stars"),
        (5, "Five stars"),
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = kwargs.get('choices', self.ratings)
        super().__init__(*args, **kwargs)


class LessonFeedback(models.Model):
    lesson = models.ForeignKey(LessonPlan, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # Temporarily removed while this is implemented!
    # Should we email the author of this feedback if the lesson plan gets updated?
    # notify_author_of_changes = models.BooleanField(default=True)

    # 1 star = complete failure; 5 stars = complete success
    overall_rating = FiveStarRatingField()

    # 2500 characters is appox. 2-3 meaty paragraphs.
    comments = models.TextField(max_length=2500)

    create_time = models.DateTimeField(auto_now_add=True)


class WebsiteFeedback(models.Model):
    # 1 star = complete failure; 5 stars = complete success
    overall_rating = FiveStarRatingField()

    # 2500 characters is appox. 2-3 meaty paragraphs.
    strengths = models.TextField(max_length=2500)
    weaknesses = models.TextField(max_length=2500)

    # The form is anonymous, so we ask for an email so we can follow-up with the user
    email = models.EmailField(blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
