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
		course = models.Course.objects.get(course_code = "TST 101")
		self.assertEqual(course.course_name, "TestCourse1")

	def test_course_create(self):
		models.Course.objects.create(course_name = "TestCourse3",
									 course_code = "TST 103")

	def test_course_delete(self):
		course = models.Course.objects.get(course_code = "TST 102")
		course.delete()

class ChapterTestCase(TestCase):
	def setUp(self):
		models.Course.objects.create(course_name = "TestCourse1",
									 course_code = "TST 101")
		course = models.Course.objects.get(course_code = "TST 101") 
		models.Chapter.objects.create(chapter_no = 1,
									 chapter_name = "Chapter1ForCourse1",
									 chapter_course = course)
	def test_chapter_get(self):
		chapter = models.Chapter.objects.get(chapter_no = 1)
		self.assertEqual(chapter.chapter_name, "Chapter1ForCourse1")

	def test_chapter_create(self):
		course = models.Course.objects.get(course_code = "TST 101")
		models.Chapter.objects.create(chapter_no = 2,
									 chapter_name = "Chapter2ForCourse1",
									 chapter_course = course)

	def test_chapter_delete(self):
		chapter = models.Chapter.objects.get(chapter_no = 1)
		chapter.delete()

class NoteTestCase(TestCase):
	def setUp(self):
		models.Course.objects.create(course_name = "TestCourse1",
									 course_code = "TST 101")
		course = models.Course.objects.get(course_code = "TST 101") 
		models.Chapter.objects.create(chapter_no = 1,
									 chapter_name = "Chapter1ForCourse1",
									 chapter_course = course)
		chapter = models.Chapter.objects.get(chapter_no = 1)
		models.Note.objects.create(note_title = "TestNote1",
								   note_summary = "Test Note 1",
								   note_chapter = chapter)

	def test_note_get(self):
		note = models.Note.objects.get(note_title = "TestNote1")
		self.assertEqual(note.note_summary, "Test Note 1")

	def test_note_create(self):
		chapter = models.Chapter.objects.get(chapter_no = 1)
		models.Note.objects.create(note_title = "TestNote2",
								   note_summary = "Test Note 2",
								   note_chapter = chapter)

	def test_note_delete(self):
		note = models.Note.objects.get(note_title = "TestNote1")
		note.delete()