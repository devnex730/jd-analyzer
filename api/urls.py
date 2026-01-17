from django.urls import path
from .views import index, get_jd, resume, build_resume, resume_preview

urlpatterns = [
    path("", index, name="home"),
    path("get_jd/", get_jd, name="get_jd"),          
    path("make_resume/", resume, name="resume"),
    path("build_resume/", build_resume, name="build_resume"),
    path("resume/preview/", resume_preview, name="preview"),
]
