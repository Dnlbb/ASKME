from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
import random
from faker import Faker
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from datetime import timezone as dt_timezone
import pytz

fake = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for the amount of data to create')

    def handle(self, *args, **options):
        ratio = options['ratio']

        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio * 2
        num_likes = ratio * 200

        self.stdout.write(f'Starting data generation with ratio {ratio}')

        with transaction.atomic():
            users = self._create_users(num_users)
            tags = self._create_tags(num_tags)
            questions = self._create_questions(num_questions, users, tags)
            answers = self._create_answers(num_answers, users, questions)
            self._create_likes(num_likes, users, questions, answers)

        self.stdout.write(self.style.SUCCESS('Database populated successfully.'))

    def _create_users(self, count):
        users = [User(
            username = fake.unique.user_name(),
            email=fake.email(),
            password='password'
        ) for _ in range(count)]
        created_users = User.objects.bulk_create(users)

        profiles = [Profile(user=user, avatar=None) for user in created_users]
        Profile.objects.bulk_create(profiles)
        return created_users

    def _create_tags(self, count):
        tags_set = set()
        for _ in range(count):
            tags_set.add(fake.word())

        tags = [Tag(name=tag) for tag in tags_set]
        return Tag.objects.bulk_create(tags)

    def _create_questions(self, count, users, tags):
        questions = []
        for _ in range(count):
            created_at = fake.date_time_this_year(tzinfo=pytz.UTC)
            question = Question(
                title=fake.sentence(),
                text=fake.text(),
                author=random.choice(users),
                created_at=created_at,
                rating=random.randint(0, 100)
            )
            questions.append(question)

        created_questions = Question.objects.bulk_create(questions)
        for question in created_questions:
            question.tags.set(random.sample(tags, k=random.randint(1, 3)))
        return created_questions

    def _create_answers(self, count, users, questions):
        answers = [Answer(
            question=random.choice(questions),
            author=random.choice(users),
            text=fake.paragraph(),
            created_at=fake.date_time_this_year(tzinfo=dt_timezone.utc)
        ) for _ in range(count)]
        return Answer.objects.bulk_create(answers)

    def _create_likes(self, count, users, questions, answers):
        question_likes = []
        answer_likes = []
        for _ in range(count):
            user = random.choice(users)
            if random.choice([True, False]):
                question_likes.append(QuestionLike(user=user, question=random.choice(questions)))
            else:
                answer_likes.append(AnswerLike(user=user, answer=random.choice(answers)))

        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)
        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
