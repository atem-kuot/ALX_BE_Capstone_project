from django.urls import path
from . import views

urlpatterns = [
    path('alerts/', views.AlertListView.as_view(), name='alert-list'),
    path('alerts/<int:pk>/', views.AlertDetailView.as_view(), name='alert-detail'),
    path('alerts/<int:pk>/resolve/', views.AlertResolveView.as_view(), name='alert-resolve'),
    path('alerts/preferences/', views.AlertPreferenceView.as_view(), name='alert-preferences'),
    path('alerts/unresolved/', views.UnresolvedAlertsView.as_view(), name='unresolved-alerts'),
    path('alerts/critical/', views.CriticalAlertsView.as_view(), name='critical-alerts'),
    path('alerts/stats/', views.alert_stats, name='alert-stats'),
    path('alerts/bulk-resolve/', views.bulk_resolve_alerts, name='bulk-resolve-alerts'),
    path('telegram-webhook/', views.telegram_webhook, name='telegram-webhook'),

]