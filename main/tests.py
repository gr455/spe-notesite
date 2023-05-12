from django.test import TestCase
import main.models as models
# Create your tests here.

class CourseTestCase(TestCase):
	def setUp(self):
		models.Course.objects.create(course_name = "TestCourse1",
									 course_code = "TST 101")
		models.Course.objects.create(course_name = "TestCourse2",
									 course_code = "TST 102")

	def test_course_get(self):
		course = Course.objects.get(course_code = "TST 101")
		self.assertEqual(course.course_name, "TestCourse1")

	def test_course_create(self):
		pass
