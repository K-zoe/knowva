from django.db import models

class QuizQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(
            is_public = True,
            course__is_public = True
        )
    
    def by_uuid(self, course_uuid, quiz_uuid):
        return self.filter(
            course__uuid = course_uuid,
            uuid = quiz_uuid
        )