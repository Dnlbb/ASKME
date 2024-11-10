from django.core.management.base import BaseCommand
from app.models import User, Question, Answer, Tag, QuestionLike, AnswerLike
from random import choice
from django.utils import timezone

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        users = []
        user_set = set()
        for i in range(ratio):
            username = f"user_{i}"
            email = f"user_{i}@example.com"
            if username not in user_set:
                user, created = User.objects.get_or_create(username=username, email=email)
                users.append(user)
                user_set.add(username)

        tags = []
        tag_set = set()
        for i in range(ratio):
            name = f"tag_{i}"
            if name not in tag_set:
                tag, created = Tag.objects.get_or_create(name=name)
                tags.append(tag)
                tag_set.add(name)

        questions = []
        question_titles = set()
        for i in range(ratio * 10):
            title = f"Question {i}"
            if title not in question_titles:
                author = choice(users)
                created_at = timezone.now()
                question = Question(title=title, text=f"Text for question {i}", author=author, created_at=created_at)
                questions.append(question)
                question_titles.add(title)

        batch_size = 100
        for i in range(0, len(questions), batch_size):
            Question.objects.bulk_create(questions[i:i+batch_size])


        for question in questions:
            question_tags = choice(tags)
            question.tags.add(question_tags)

        answers = []
        answer_combinations = set()
        for i in range(ratio * 100):
            question = choice(questions)
            author = choice(users)

            if (question.id, author.id) not in answer_combinations:
                answer = Answer(question=question, author=author, text=f"Answer text {i}", created_at=created_at)
                answers.append(answer)
                answer_combinations.add((question.id, author.id))

        for i in range(0, len(answers), batch_size):
            Answer.objects.bulk_create(answers[i:i+batch_size])

        likes = []
        like_combinations = set()
        for i in range(ratio * 200):
            question = choice(questions)
            user = choice(users)

            if (question.id, user.id) not in like_combinations:
                likes.append(QuestionLike(question=question, user=user))
                like_combinations.add((question.id, user.id))

        for i in range(0, len(likes), batch_size):
            QuestionLike.objects.bulk_create(likes[i:i+batch_size])

        answer_likes = []
        answer_like_combinations = set()
        for i in range(ratio * 200):
            answer = choice(answers)
            user = choice(users)
            if (answer.id, user.id) not in answer_like_combinations:
                answer_likes.append(AnswerLike(answer=answer, user=user))
                answer_like_combinations.add((answer.id, user.id))

        for i in range(0, len(answer_likes), batch_size):
            AnswerLike.objects.bulk_create(answer_likes[i:i+batch_size])

        self.stdout.write(self.style.SUCCESS(f"База данных заполнена с коэффициентом {ratio}"))
