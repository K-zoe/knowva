from django.views.generic import ListView
from quizzes.models import (
    Course,
    Quiz,
    Question,
    Choice
)
from quizzes.forms.search import CourseSearchForm
from django.db.models import Max, Q

ALLOWED_SORT_FIELDS = {'latest_quiz_update', 'like_count'}

class CourseSearchView(ListView):
    template_name = 'quizzes/course_search.html'
    model = Course
    context_object_name = 'courses'
    paginate_by = 10

    def get_form(self):
        # formの生成を1箇所に集約。キャッシュして複数回呼ばれても安全。
        if not hasattr(self, '_form'):
            self._form = CourseSearchForm(self.request.GET)
        return self._form

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            is_public = True,
            quiz__is_public = True
        ).annotate(latest_quiz_update = Max('quiz__updated_at'))
        
        #入力フォームの制御はFormクラスに任せる。
        form = self.get_form()

        if not form.is_valid():
            return queryset.order_by('-latest_quiz_update','pk')

        return self.query_filter(queryset, form.cleaned_data)

    def query_filter(self, queryset, cleaned_data):
        title = cleaned_data.get('title')
        tag = cleaned_data.get('tag')
        sort_field = cleaned_data.get('sort_field')
        sort_order = cleaned_data.get('sort_order')

        # キーワード・タグのAND検索
        q = Q()
        if title:
            q &= Q(title__icontains=title)
        if tag:
            q &= Q(tag__icontains=f'#{tag}')
        queryset = queryset.filter(q)

        # 並び替え
        if sort_field in ALLOWED_SORT_FIELDS:
            order_prefix = '-' if sort_order == 'desc' else ''
            queryset = queryset.order_by(f'{order_prefix}{sort_field}')
        else:
            queryset = queryset.order_by('-latest_quiz_update')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context