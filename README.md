# BiliAudioBot
A python gui version of audio bot.

provided by Aynakeya(划水) & Nearl_Official(摸鱼)


# how to start (demo version)

`git clone https://github.com/LXG-Shadow/BiliAudioBot.git`

cd to the working directory

`pip install -r requirements.txt`

download **mpv-1.dll** into working directory

`python AudioBot.py`

# how to use (demo version)

**连接直播间:**

输入直播间号，按connect


**通用点歌:**

`点歌 关键字/id`

id

网易云: `点歌 wy1817437429`

bilibili `点歌 au2159832`

bilibili视频 `点歌 BV1Xv411Y7eW`

酷我 `点歌 kuwo142655450`

关键字 (默认使用网易云搜索)

`点歌 染 reol`

**切歌:**

`切歌` 目前仅允许切自己的歌

**来源点歌:**

网易云 `点w歌 关键字/1817437429/wy1817437429`

bilibili `点b歌 关键字/au2159832`

酷我 `点k歌 关键字/kuwo142655450/142655450`

**网易云vip匹配:**

匹配顺序是 bilibili -> 酷我 -> 网易云


# build

first build frontend

`cd fronend`

`npm run build`

second run python package

`pyi-makespec --onefile --windowed --icon=resource/favicon.ico --add-data "frontend/dist;frontend/dist" --add-data "resource;resource" --add-data "config;config" --add-binary "mpv-1.dll;." AudioBot.py`

`pyinstaller --onefile --windowed --icon=resource/favicon.ico --add-data "frontend/dist;frontend/dist" --add-data "resource;resource" --add-data "config;config" --add-binary "mpv-1.dll;." AudioBot.py`

`try not use onefile if you want start faster`

`pyinstaller --windowed --icon=resource/favicon.ico --add-data "frontend/dist;frontend/dist" --add-data "resource;resource" --add-data "config;config" --add-binary "mpv-1.dll;." AudioBot.py`

# todo list

- ~~config添加默认房间~~

- ~~tooltips~~

- ~~本地文本输出~~

- ~~本地文本输出自定义格式~~

- ~~音量写入配置文件~~

- ~~ui不显示滚动条?~~

- ~~翻译~~

- ~~歌词->文本 网页~~

- 黑名单

- 时间自定义

- 自动过滤翻唱

- 使用系统代理

- 点歌历史记录

- 修改点歌格式

- 本地曲库

- 具体时间->文本 网页

# 已知问题

先开加速器再开本软件可能会导致web无法正常工作

解决方式: 可以先开启本软件再打开加速器。


# change log

2021-03-11-demo0.7.4: translation update

2021-03-11-demo0.7.0: frontend&backend demo finish.

2021-03-11-demo0.6.5: rewrite event handling

2021-03-11-demo0.6.0: asynchronous loading

2021-03-11-demo0.5.5: build executable

2021-03-10-demo0.5.0: finish demo version