from django.urls import path
from .views import HomeView, SumarizeView


urlpatterns= [
    # path("inicio/", HomeView.as_view()),
    path("", HomeView.as_view()),
    path("summarize-docs/", SumarizeView.as_view())
]
