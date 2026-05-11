import django
from django.test import TestCase


class ViewTest(TestCase): # Contains unit tests for verifying application views | Uygulama görünümlerini doğrulamak için birim testlerini içerir

    if django.VERSION[:2] >= (1, 7):
        @classmethod
        def setUpClass(cls): # Ensures Django is properly initialized for testing | Django'nun test için düzgün şekilde başlatılmasını sağlar
            super(ViewTest, cls).setUpClass()
            django.setup()

    def test_home(self): # Verifies the home page loads correctly with expected content | Ana sayfanın beklenen içerikle yüklendiğini doğrular
        response = self.client.get('/')
        self.assertContains(response, 'Home Page', 1, 200)

    def test_contact(self): # Verifies the contact page accessibility and content | İletişim sayfasının erişilebilirliğini ve içeriğini doğrular
        response = self.client.get('/contact')
        self.assertContains(response, 'Contact', 3, 200)

    def test_about(self): # Verifies the about page availability and content | Hakkında sayfasının mevcudiyetini ve içeriğini doğrular
        response = self.client.get('/about')
        self.assertContains(response, 'About', 3, 200)