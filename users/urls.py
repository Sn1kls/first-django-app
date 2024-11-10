from django.urls import path
from users.views import ProtectedView, RegisterView, UserProfileView, UserListView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("protected/", ProtectedView.as_view(), name="protected_view"),
    path("list/", UserListView.as_view(), name="user_list"),
]
