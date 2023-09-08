from django.test import TestCase
import datetime
from django.utils import timezone

from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=5)
        future_question = Question(pub_date= time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=5)
        old_question = Question(pub_date= time)
        self.assertIs(old_question.was_published_recently(),False)
        
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now()
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(),True)

def create_question(question_text,days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date= time)

def create_choice_set(question_id):
    question = Question.objects.get(pk= question_id)
    return question.choice_set.create(choice_text= "choice")


class QuestionIndexViewsTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
    
    def test_past_question(self):
        question = create_question("past_question",days=-30)
        create_choice_set(question.id)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])

    def test_future_question(self):
        question = create_question("future_quesiton",days = 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question_and_past_question(self):
        question = create_question("past_question",days=-30)
        create_question("future_question",days=30)
        create_choice_set(question.id)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])

    def test_two_past_question(self):
        question1 = create_question("past_question 1",days=-3)
        question2 = create_question("past_question 2",days=-5)
        create_choice_set(question1.id)
        create_choice_set(question2.id)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question2,question1])

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question("future question",days=(30))
        url = reverse("polls:detail",args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        past_question = create_question("past question",days=-30)
        create_choice_set(past_question.id)
        url = reverse('polls:detail',args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,past_question.question_text)

class QuestionResultViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question("future question",days=(30))
        url = reverse("polls:detail",args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        past_question = create_question("past question",days=-30)
        url = reverse('polls:detail',args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,past_question.question_text)

class ChoiceModelTests(TestCase):
    
    def test_choice_set(self):
        question = create_question("question",days=-3)
        response = self.client.get(reverse("polls:index"))
    
       
        if question.choice_set.count() > 0:
            self.assertContains(response,question.question_text)
        else:
            self.assertNotContains(response,question.question_text)    
   
        
