from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User 
        # 장고가 만들어놓은 UserCreationForm에서 model만 우리가 만든 USer로 바꿈
        # fields = '__all__'
        fields = ('username', )


class CustomAuthenticationForm(AuthenticationForm):
    pass