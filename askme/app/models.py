from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def best_questions(self):
        return self.annotate(like_count=Count('likes')).order_by('-like_count')

    def new_questions(self):
        return self.order_by('-created_at')

    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    tags = models.ManyToManyField('Tag', related_name="questions")
    rating = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/questions/{self.id}/"

    def like_count(self):
        return self.likes.count()

    def tag_list(self):
        return [tag.name for tag in self.tags.all()]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.author.username} on {self.question.title}"


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'user')

    def __str__(self):
        return f"Like by {self.user.username} on {self.question.title}"


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('answer', 'user')

    def __str__(self):
        return f"Like by {self.user.username} on answer to {self.answer.question.title}"
