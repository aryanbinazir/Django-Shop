from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = 'home'

bucket_url = [
    path('', views.BucketHomeView.as_view(), name='bucket'),
    path('delete_obj/<str:key>', views.DeleteBucketObjectView.as_view(), name='bucket_object_delete'),
    path('download_obj/<str:key>', views.DownloadBucketObjectView.as_view(), name='bucket_object_download')
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>', views.HomeView.as_view(), name='category_filter'),
    path('bucket/', include(bucket_url)),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/comments/<int:product_slug>', views.ProductDetailView.as_view(), name='add_comment')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)