from test.base import BaseTest
from accounts.models import User
from django.urls import reverse

class AnswerTest(BaseTest):
    def create_course(self, question_count = 3, is_public = True):
        #NOTE:回答用のコース作成。
        course = self.course_create()
        quiz = self.quiz_create(course)
        
        for i in range(question_count):
            question = self.question_create(quiz)
            self.choice1_create(question)
            self.choice2_create(question)

        #回答で表示でのは公開になっているコースと問題集だけなので公開にする。
        course.is_public = is_public
        course.save()
        quiz.is_public = is_public
        quiz.save()

        return course, quiz
    
    def test_answer_attempt_view_is_public_success(self):
        #NOTE:コースと問題集が公開されている問題だけが表示されるかテスト。
        course, quiz = self.create_course()
        response = self.client.get(
            reverse(
                'answer_attempt',
                kwargs = {
                    'course_uuid': course.uuid,
                    'quiz_uuid': quiz.uuid
                }
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_answer_attempt_view_is_not_public_fail(self):
        #NOTE:コースと問題集が公開されていない問題は表示されないかテスト。
        course, quiz = self.create_course(is_public = False)
        response = self.client.get(
            reverse(
                'answer_attempt',
                kwargs = {
                    'course_uuid': course.uuid,
                    'quiz_uuid': quiz.uuid
                }
            )
        )

        self.assertEqual(response.status_code, 404)

