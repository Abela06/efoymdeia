from rest_framework import generics, viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from client.models import Video
from client.serializers import VideoSerializer, MyTokenObtainPairSerializer
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json
from django.http import JsonResponse, HttpResponse
import youtube_search
from django.conf import settings  # correct way
from datetime import datetime, timedelta


def video(category, request):
    print(category)
    video_list = Video.objects.filter(
        Q(channel__channelCategory=category) & (Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by(
        '?')
    # .order_by('-publishedAt')
    page = request.GET.get('page', 1)
    paginator = Paginator(video_list, 24)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return videos


date = datetime.today()
start_week = date - timedelta(date.weekday())
end_week = start_week + timedelta(7)

now = datetime.now()
now = now.replace(hour=0, minute=0, second=0, microsecond=0)


def auto_complete(request):
    query = request.GET.get('search')

    inp = requests.get(
        "http://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q=" + query)

    whileset = set("()")
    tmp = ""
    for i in inp.text[18:]:
        if i not in whileset:
            tmp += i

    resp = json.loads(tmp)
    vals = []
    for val in resp[1]:
        vals.append(val[0])
    return JsonResponse({"result": vals})


def search_youtube(request):
    query = request.GET.get('search')

    b = {}
    if query:
        b = youtube_search.YoutubeSearch(
            settings.CREDENTIALS_PATH, query, 50, '', '', 'date').response

    top_list = Video.objects.filter(Q(publishedAt__gte=now - timedelta(days=datetime.today().weekday())) & (
            Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-view_count')

    # context = {
    #     'video_list': b,
    #     'top_list': top_list[:10],
    # }
    # template = loader.get_template('search.html')
    return HttpResponse([b], content_type="application/json")


class VideoList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    # def get_queryset(self):
    #     category = self.request.query_params.get('category')
    #     video_list = Video.objects.filter(
    #         Q(channel__channelCategory=category) & (
    #                 Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('?')
    #     return video_list


class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    filter_fields = (
        'category',
    )

    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category:
            video_list = Video.objects.filter(
                Q(channel__channelCategory=category) & (
                        Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('?')
            return video_list
        else:
            return Video.objects.all()
    # serializer_class = VideoSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
