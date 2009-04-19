from django.test import TestCase

class TigerTest(TestCase):
    fixtures = ['courses.json']

    def test_course_list(self):
        rsp = self.client.get('/courses/')
        self.assertContains(rsp, 'turpis eros')

    def test_course_detail(self):
        rsp = self.client.get('/courses/sample-course-2')
        self.assertContains(rsp, 'purus nec ullamcorper aliquam')

    def test_course_request(self):
        rsp = self.client.get('/courses/sample-course-2/request')
        self.assertEqual(rsp.status_code, 200)
