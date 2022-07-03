from django.test import TestCase
from django.test import Client

from django.urls import reverse

from model_bakery import baker
from contactsapp.models import Employees


class TestEmployeeIntegration(TestCase):
    def setUp(self):
        self.employee_count = 10
        self.client = Client()
        # self.employee_model = baker.make("contactsapp.Employees")
        self.employee_service_models = baker.make(
            "contactsapp.EmployeeService", _quantity=self.employee_count
        )
        self.employee_object = Employees()

    def test_get_all_employees(self):
        self.assertEqual(
            self.employee_count, len(self.employee_object.get_all_employees())
        )

    # def test_post_success(self):
    #     choice = self.choice_models[0]
    #     response = self.client.post(
    #         reverse("polls:vote_result", kwargs={"pk": choice.question.id}),
    #         {"choice": choice.id},
    #         follow=True,
    #     )
    #     self.assertIn(302, response.redirect_chain[0])
    #     self.assertTemplateUsed(response, "polls/results.html")

    # def test_post_failure(self):
    #     choice = self.choice_models[0]
    #     response = self.client.post(
    #         reverse("polls:vote_result", kwargs={"pk": choice.question.id}), follow=True
    #     )
    #     self.assertIn(302, response.redirect_chain[0])
    #     self.assertTemplateUsed(response, "polls/detail.html")
