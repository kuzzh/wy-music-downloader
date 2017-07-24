# wy-music-downloader
从网易云音乐下载歌单里的歌曲

- 前提条件
  需要安装 `pycrypto` 模块，使用如下命令安装：
  `pip install pycrypto`

- 使用方法：
  `python wyMusicDownloader.py [-o local/save/path](可选) [-b bitrate](可选) [song list url]`
  
## 2017-07-05 更新
- 适配最新网易云音乐，又可以重新下载歌单里的歌曲啦
- 适配过程中发现网易云音乐对部分参数进行了加密，参考了其他大神的代码来进行模拟加密
  - [网易云下载](https://greasyfork.org/zh-CN/scripts/23222-%E7%BD%91%E6%98%93%E4%BA%91%E4%B8%8B%E8%BD%BD/code)
  - [如何爬网易云音乐的评论数？](https://www.zhihu.com/question/36081767) 中 [@洛克](https://www.zhihu.com/people/ClutchBear/answers) 的回答
