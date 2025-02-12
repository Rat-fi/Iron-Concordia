from django.test import TestCase
from django.urls import reverse
from .models.NewCookUser import MealInstructions

class MealInstructionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        MealInstructions.objects.create(
            name="Vegan Salad",
            difficulty="Easy",
            dietary_restrictions="vegan, gluten-free",
            price=15.00,
            prepare_time=10,
            calories=250,
            protein=5,
            steps="Step 1: Wash vegetables.\nStep 2: Chop them.\nStep 3: Mix with dressing."
        )
        MealInstructions.objects.create(
            name="Grilled Chicken",
            difficulty="Medium",
            dietary_restrictions="",
            price=25.00,
            prepare_time=30,
            calories=400,
            protein=35,
            steps="Step 1: Marinate the chicken.\nStep 2: Grill for 20 minutes."
        )
    
    def test_view_without_filters(self):
        response = self.client.get(reverse('newcookuser_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vegan Salad")
        self.assertContains(response, "Grilled Chicken")
    
    def test_view_with_dietary_filter(self):
        response = self.client.get(reverse('newcookuser_list'), {'dietary_restrictions': 'vegan'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vegan Salad")
        self.assertNotContains(response, "Grilled Chicken")

