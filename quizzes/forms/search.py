import django.forms as forms

class CourseSearchForm(forms.Form):
    title = forms.CharField(required = False, label = 'タイトル')
    tag = forms.CharField(required = False, label = 'タグ')

    SORT_CHOICES = [
        ('latest_quiz_update', '公開日'),
        ('like_count','いいね数')
    ]

    ORDER_CHOICES = [
        ('desc', '降順'),
        ('asc', '昇順')
    ]

    sort_field = forms.ChoiceField(
        choices = SORT_CHOICES,
        required = False,
        label = '並び替え項目',
        initial = 'latest_quiz_update'
    )
    sort_order = forms.ChoiceField(
        choices = ORDER_CHOICES,
        required = False,
        label = '順序',
        initial = 'desc'
    )