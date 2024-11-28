from django.urls import path

from users.views import ProtectedView, RegisterView, UserListView, UserNotificationsView, UserProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("protected/", ProtectedView.as_view(), name="protected_view"),
    path("list/", UserListView.as_view(), name="user_list"),
    path("notifications/", UserNotificationsView.as_view(), name="user_notifications"),
]
