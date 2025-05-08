from django import forms

class URLForm(forms.Form):
  website_url=forms.URLField(label='Enter the url' ,required=True)
