from base.widgets import Ueditor
from django import forms
from base.models import Article

class PostForm(forms.ModelForm):	
	myContent = forms.CharField(widget = Ueditor())
	class Meta:
		model = Article
		fields = ('title','text',)