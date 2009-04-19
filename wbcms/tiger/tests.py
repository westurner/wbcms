from django.test import TestCase

class TigerTest(TestCase):
    fixtures = ['courses.json']

    def test_course_list(self):
        rsp = self.client.get('/courses/')
        self.failUnlessEqual(rsp.status_code, 200)
