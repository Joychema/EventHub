from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .import views
from .views import CustomLoginView
urlpatterns=[

    path('',views.home,name='home'),

    path('event_list/',views.event_list,name='event_list'),  # Home page - List of events

    path('event_detail/<int:event_id>',views.event_detail,name='event_detail'),  # Event detail page

    path('book_event/<int:event_id>',views.book_event,name='book_event'), # Booking page

    path('login/',views.login1,name='login'),

    path('register/',views.register,name='register'),

    path('logout/',views.logout1,name='logout'),

    path("login/", CustomLoginView.as_view(), name="login"),

    # path('messages/',views.test_messages,name='test_messages'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)