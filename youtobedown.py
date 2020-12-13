# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 9:00
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : youtobedown.py
# @Software: PyCharm

import http_util
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4146.4 Safari/537.36',
    'Cookie': "VISITOR_INFO1_LIVE=z1n-WAZNoLk; PREF=f4=4000000; GPS=1; YSC=UjIX2KuRfOg"
}
url = "https://www.youtube.com/browse_ajax" \
      "?ctoken=4qmFsgJUEhhVQ3FXM21FUWVQYzNMd3l1bURuenY0c0EaOEVnWjJhV1JsYjNNWUF5QUFNQUU0QWVvREYwTm5Ua1JTUld0VFEyZHFUWGhOTnpNMFduRTFaME5S" \
      "&continuation=4qmFsgJUEhhVQ3FXM21FUWVQYzNMd3l1bURuenY0c0EaOEVnWjJhV1JsYjNNWUF5QUFNQUU0QWVvREYwTm5Ua1JTUld0VFEyZHFUWGhOTnpNMFduRTFaME5S" \
      "&itct=CAIQybcCIhMImeD42NKr7QIVwhuPCh1B6wdX"
http_util.do_get(url,None,headers=headers)

# from pytube import YouTube
# video = YouTube("http://www.youtube.com/watch?v=Ik-RsDGPI5Y")
# vs = video.streams.filter(file_extension="mp4", resolution="360p", progressive=True).all()
# if len(vs) > 0:
#     print("开始下载视频{}".format(vs[0]))
#     try:
#         vs[0].download("youtobe")
#     except Exception as e:
#         print("异常，开始重试")
#         vs[0].download("youtobe")
#     print("完成视频下载{}".format(vs[0]))

import requests
import os
# headers = {
#     'Accept': 'application/vnd.vimeo.*; version=3.4.2',
#     'Accept-Language': 'en',
#     'Origin':'https://vimeo.com',
#     "Referer": "https://vimeo.com",
#     'Content-Type': 'application/json',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
#     'Authorization':'jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDY3ODg1NDAsInVzZXJfaWQiOm51bGwsImFwcF9pZCI6NTg0NzksInNjb3BlcyI6InB1YmxpYyIsInRlYW1fdXNlcl9pZCI6bnVsbH0.qUvzE2k6W8_7bpHKx7Z3LidDQQwuFAlfX5oHrJs22rM'
# }
#
# url='https://api.vimeo.com/users/108340029/profile_sections?autopause=0&autoplay=0&controls=1&like=1&logo=1&loop=0&share=1&watch_later=1&info_on_pause=1&badge=1&playbar=1&default_to_hd=1&volume=1&include_videos=1&fields=uri%2Ctitle%2CuserUri%2Curi%2Cunbounded%2Cposition%2Cclip_uris%2Cvideos.total%2Cvideos.data.video_details%2Cvideos.data.profile_section_uri%2Cvideos.data.is_staff_pick%2Cvideos.data.show_featured_comment%2Cvideos.data.featured_comment%2Cvideos.data.column_width%2Cvideos.data.clip.uri%2Cvideos.data.clip.name%2Cvideos.data.clip.type%2Cvideos.data.clip.categories.name%2Cvideos.data.clip.categories.uri%2Cvideos.data.clip.config_url%2Cvideos.data.clip.pictures%2Cvideos.data.clip.height%2Cvideos.data.clip.width%2Cvideos.data.clip.duration%2Cvideos.data.clip.description%2Cvideos.data.clip.created_time%2Cvideos.data.clip.user.uri%2Cvideos.data.clip.user.name%2Cvideos.data.clip.user.link%2Cvideos.data.clip.user.location%2Cvideos.data.clip.user.bio%2Cvideos.data.clip.user.membership.badge%2Cvideos.data.clip.user.skills%2Cvideos.data.clip.user.background_video%2Cvideos.data.clip.user.available_for_hire%2Cvideos.data.clip.user.pictures.sizes%2Cvideos.data.clip.badge.type%2Cvideos.data.clip.metadata.connections.comments.total%2Cvideos.data.clip.live.scheduled_start_time%2Cvideos.data.clip.live.status&videos_count_per_section=10&page=1&per_page=4'

video_url = "https://vod-progressive.akamaized.net/exp=1606795636~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F2144%2F19%2F485721370%2F2175404961.mp4~hmac=14fb21d5857099476a3a3463daa0092cf96a35df154e9a48733a08cdf2aa7ea8/vimeo-prod-skyfire-std-us/01/2144/19/485721370/2175404961.mp4"
# body = requests.get(url,headers=headers)
# video_url = 'https://v3-tt.ixigua.com/2ac37b2743e03c40f2925e20cf5bcef4/5c3320e9/video/m/22008c65f827a974d5da5af9f958847c36f11611bf2e000019ecbad7ae9b/?rc=M3V0Nmc6aW9najMzMzczM0ApQHRAbzQ3NDk6MzQzMzY3NDMzNDVvQGgzdSlAZjN1KWRzcmd5a3VyZ3lybHh3Zjc2QDBqajQ0Y3NjXl8tLWEtL3NzLW8jbyM2LTQtLzEtLjU0MzQuNi06I28jOmEtcSM6YHZpXGJmK2BeYmYrXnFsOiMzLl4%3D&vfrom=xgplayer'


def do_load_media(url, path):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36'}
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
            res = requests.get(url, stream=True, headers=headers)

            content_length = int(res.headers['content-length'])
            print("content_length===",content_length)
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length) or content_length == 0:
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('下载成功,file size : %d   total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print(e)


def load_media():
    url = video_url
    path = 'test3.mp4'
    do_load_media(url, path)
    # download_file(url,path)

def download_file(url, file_pname, chunk_size=1024*4):
    """
    url: file url
    file_pname: file save path
    chunk_size: chunk size
    """
    # 第一种
    response_data_file = requests.get(url, stream=True)
    with open(file_pname, 'wb') as f:
        for chunk in response_data_file.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)

    # # 第二种
    # with requests.get(url, stream=True) as req:
    #     with open(file_pname, 'wb') as f:
    #         for chunk in req.iter_content(chunk_size=chunk_size):
    #             if chunk:
    #                 f.write(chunk)

# if __name__ == '__main__':
    # load_media()
