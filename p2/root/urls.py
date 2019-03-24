from django.urls import include, path
# from p2.core.urls import ur

urlpatterns = [
    path('', include('p2.core.urls')),
    path('s3/', include('p2.s3.urls')),
]
