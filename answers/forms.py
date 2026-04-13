import django.forms as forms

class CourseSearchForm(forms.Form):
    keyword = forms.CharField(required = False, label = 'キーワード')

    SORT_CHOICES = [
        ('created_at', '作成日'),
        ('like_count','いいね数')
    ]

    ORDER_CHOICES = [
        ('asc', '昇順'),
        ('desc', '降順')
    ]

    sort_field = forms.ChoiceField(
        choices = SORT_CHOICES,
        required = False,
        label = '並び替え項目',
        initial = 'like_count'
    )
    sort_order = forms.ChoiceField(
        choices = ORDER_CHOICES,
        required = False,
        label = '順序',
        initial = 'desc'
    )

def filter_queryset(self, queryset):
    if not self.is_valid():
        return queryset

    keyword = self.cleaned_data.get('keyword')
    sort_field = self.cleaned_data.get('sort_field')
    sort_order = self.cleaned_data.get('sort_order')

    #NOTE:キーワード検索。タグ検索は#から始まるキーワードで行う。
    if keyword:
        if keyword.startswith('#'):
            tag = keyword.lstrip('#')
            queryset = queryset.filter(tag__icontains=tag)
        else:
            queryset = queryset.filter(title__icontains=keyword)

    allowed_fields = ['created_at', 'like_count']

    if sort_field in allowed_fields:
        sort_order = sort_order or 'desc'

        if sort_order == 'desc':
            sort_field = '-' + sort_field

        queryset = queryset.order_by(sort_field)
    else:
        queryset = queryset.order_by('-like_count')

    return queryset