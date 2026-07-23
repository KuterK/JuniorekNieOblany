from django.urls import path

from . import views

urlpatterns = [
    path("", views.AnalysisListView.as_view(), name="analysis-list"),
    path("analyses/new/", views.AnalysisCreateView.as_view(), name="analysis-create"),
    path("analyses/<uuid:pk>/", views.AnalysisDetailView.as_view(), name="analysis-detail"),
    path("analyses/<uuid:pk>/status/", views.analysis_status, name="analysis-status"),
    path("analyses/<uuid:pk>/title/", views.update_title, name="analysis-title"),
    path("analyses/<uuid:pk>/rating/", views.rate_analysis, name="analysis-rating"),
    path("analyses/<uuid:pk>/regenerate/", views.regenerate_analysis, name="analysis-regenerate"),
    path("analyses/<uuid:pk>/delete/", views.delete_analysis, name="analysis-delete"),
]
