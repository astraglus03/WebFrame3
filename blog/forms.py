from .models import Comment
from django import forms
class CommentForm(forms.ModelForm):
    class Meta:       # ModelForm에서 상속받은 경우에 있어야함
        model=Comment # field 5개인데 content하나만 사용 나머지는 다 결정되어있음.
        fields=('content',)
        # views에 formdetail로 이동후 -> post_detail에서 comment_form가능