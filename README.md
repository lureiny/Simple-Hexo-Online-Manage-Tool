# 简单Hexo在线管理工具（Simple-Hexo-Online-Manage-Tool）

- [简单Hexo在线管理工具（Simple-Hexo-Online-Manage-Tool）](#%e7%ae%80%e5%8d%95hexo%e5%9c%a8%e7%ba%bf%e7%ae%a1%e7%90%86%e5%b7%a5%e5%85%b7simple-hexo-online-manage-tool)
  - [1. Hexo](#1-hexo)
  - [2. 项目简介](#2-%e9%a1%b9%e7%9b%ae%e7%ae%80%e4%bb%8b)
    - [2.1 功能需求](#21-%e5%8a%9f%e8%83%bd%e9%9c%80%e6%b1%82)
    - [2.2 HTTP API](#22-http-api)
      - [2.2.1 /](#221)
      - [2.2.2 upload](#222-upload)
      - [2.2.3 webhook](#223-webhook)
      - [2.2.4 getfiles](#224-getfiles)
      - [2.2.5 download](#225-download)
      - [2.2.6 delete](#226-delete)
      - [2.2.7 flush](#227-flush)
  - [3. 配置文件](#3-%e9%85%8d%e7%bd%ae%e6%96%87%e4%bb%b6)
  - [4. 使用方法](#4-%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95)
    - [4.1 准备工作](#41-%e5%87%86%e5%a4%87%e5%b7%a5%e4%bd%9c)
    - [4.2 环境配置](#42-%e7%8e%af%e5%a2%83%e9%85%8d%e7%bd%ae)
      - [4.2.1 不使用docker](#421-%e4%b8%8d%e4%bd%bf%e7%94%a8docker)
        - [4.2.1.1 Hexo](#4211-hexo)
        - [4.2.1.2 配置git-ssh](#4212-%e9%85%8d%e7%bd%aegit-ssh)
        - [4.2.1.3 创建并拉取git备份仓库](#4213-%e5%88%9b%e5%bb%ba%e5%b9%b6%e6%8b%89%e5%8f%96git%e5%a4%87%e4%bb%bd%e4%bb%93%e5%ba%93)
        - [4.2.1.4 配置python环境](#4214-%e9%85%8d%e7%bd%aepython%e7%8e%af%e5%a2%83)
        - [4.2.1.5 安装screen](#4215-%e5%ae%89%e8%a3%85screen)
        - [4.2.1.6 使用Simple-Hexo-Online-Manage-Tool](#4216-%e4%bd%bf%e7%94%a8simple-hexo-online-manage-tool)
        - [4.2.1.7 访问](#4217-%e8%ae%bf%e9%97%ae)
        - [4.2.1.8 配置webhook](#4218-%e9%85%8d%e7%bd%aewebhook)
      - [4.2.2 使用docker（推荐）](#422-%e4%bd%bf%e7%94%a8docker%e6%8e%a8%e8%8d%90)
        - [4.2.2.1 配置git-ssh](#4221-%e9%85%8d%e7%bd%aegit-ssh)
        - [4.2.2.2 文件目录准备工作](#4222-%e6%96%87%e4%bb%b6%e7%9b%ae%e5%bd%95%e5%87%86%e5%a4%87%e5%b7%a5%e4%bd%9c)
        - [4.2.2.3 配置docker](#4223-%e9%85%8d%e7%bd%aedocker)
        - [4.2.2.4 修改docker-compose配置文件](#4224-%e4%bf%ae%e6%94%b9docker-compose%e9%85%8d%e7%bd%ae%e6%96%87%e4%bb%b6)
        - [4.2.2.5 修改shomt配置文件](#4225-%e4%bf%ae%e6%94%b9shomt%e9%85%8d%e7%bd%ae%e6%96%87%e4%bb%b6)
        - [4.2.2.6 启动docker](#4226-%e5%90%af%e5%8a%a8docker)
        - [4.2.2.7 访问](#4227-%e8%ae%bf%e9%97%ae)
        - [4.2.2.8 配置webhook](#4228-%e9%85%8d%e7%bd%aewebhook)
    - [4.3 在网页上管理](#43-%e5%9c%a8%e7%bd%91%e9%a1%b5%e4%b8%8a%e7%ae%a1%e7%90%86)
      - [4.3.1 查看文件列表](#431-%e6%9f%a5%e7%9c%8b%e6%96%87%e4%bb%b6%e5%88%97%e8%a1%a8)
      - [4.3.2 上传](#432-%e4%b8%8a%e4%bc%a0)
      - [4.3.3 下载](#433-%e4%b8%8b%e8%bd%bd)
      - [4.3.4 删除](#434-%e5%88%a0%e9%99%a4)
      - [4.3.5 强制生成静态文件](#435-%e5%bc%ba%e5%88%b6%e7%94%9f%e6%88%90%e9%9d%99%e6%80%81%e6%96%87%e4%bb%b6)
    - [4.4 通过git管理](#44-%e9%80%9a%e8%bf%87git%e7%ae%a1%e7%90%86)
      - [4.4.1 新增](#441-%e6%96%b0%e5%a2%9e)
      - [4.4.2 更新](#442-%e6%9b%b4%e6%96%b0)
      - [4.4.3 删除](#443-%e5%88%a0%e9%99%a4)
      - [4.4.4 备份](#444-%e5%a4%87%e4%bb%bd)
  - [5. 扩展/自定义](#5-%e6%89%a9%e5%b1%95%e8%87%aa%e5%ae%9a%e4%b9%89)

## 1. Hexo
[Hexo][4]作为一款优秀的静态博客广受好评。网上大多数的教程都是基于Hexo+Github Page来写的。这种模式有很多优点，但对我来说也有一些缺点。

优点：

1. 成本低：拥有一个Github账号+本地一台电脑就可以实现
2. 高效：你只需要懂Markdown语法就可以写出一篇排版优美的文章
3. 美观且扩展性强：Hexo拥有大量的主题和插件

缺点（对我而言）：

1. 不适合移动端：这里主要指平板端
2. 分布式配置麻烦：想在多个终端间同步文件会比较麻烦，需要配置多个Hexo环境
3. 没有备份功能（使用Github Page可以备份生成的静态文件）

网上找了一圈，也没找到适合我的解决方案（可能是姿势不对，如果有哪位知道有，欢迎留言）。本着没轮子就只能造轮子的想法，我基于Python Flask+Github写了一个简单的框架来实现我的需求。

## 2. 项目简介
### 2.1 功能需求
本项目基于Python Flask框架进行开发，功能需求如下：

  - [x] 基于[Github][15]实现备份、同步管理（偶尔会因为网络问题webhook失败，非大陆VPS可以考虑使用）
  - [x] 基于[码云][16]实现备份、同步管理（大陆环境使用码云时整体延迟很低，且不会出现push时系统无响应的情况，大陆VPS建议考虑使用）
  - [x] 基于网页进行新增、更新、删除、下载、查看 
  - [x] 身份验证，防止接口被恶意调用
  - [x] 自定义文件处理方法
  - [x] 自动补全`Front-matter`信息
  - [x] 支持多样主题

### 2.2 HTTP API
对于每一个涉及到系统文件的接口，都限制只能使用POST的方法，并且需要传输身份验证所需的Token（详见[配置文件](#3-配置文件)）。

#### 2.2.1 /

> URL = http(s)://{host}/
> 
> Method = GET

系统的根目录，返回一个简单的页面辅助进行上传、查看、删除、下载等操作。

#### 2.2.2 upload

> URL = http(s)://{host}/upload
> 
> Method = POST
> 
> 请求参数：
> 
> 1. file：上传的文件
> 2. token：用户自行设定的token
> 
> return：返回文件上传的结果 

文件上传接口，新增和更新操作使用的接口。

1. Hexo _post目录下已经存在新上传的文件时，系统执行更新操作
2. Hexo _post目录下不存在新上传的文件时，系统执行新增操作

#### 2.2.3 webhook

> URL = http(s)://{host}/webhook
> 
> Method = POST


此接口为Github回调接口（[官方文档][1]）。通过此接口，当设置的远程仓库有新的push时，github会请求该接口，系统会根据请求配置信息来对文章进行更新，其中涉及的参数会在[配置文件](#3-配置文件) 配置文件)部分进行详细说明。

#### 2.2.4 getfiles

> URL = http(s)://{host}/getfiles
> 
> Method = POST
> 
> 请求参数：
> 
> 1. token：用户自行设定的token
> 
> return：当前状态下文件列表

获取文件列表的接口，通过该接口可以查看当前状态下全部文件信息，包含文件名、title、发布日期、更新日期。请求该接口后，系统会在页面生成文件列表，列表中除包含文件信息外，还包含删除和下载操作按钮。

#### 2.2.5 download

> URL = http(s)://{host}/download
> 
> Method = POST
> 
> 请求参数：
> 
> 1. token：用户自行设定的token
> 2. filename: 下载的文件名
> 
> return：下载对应文件

文件下载接口，通过点击下载按钮，就会请求该接口，身份验证成功后开始下载文件。

#### 2.2.6 delete

> URL = http(s)://{host}/delete
> 
> Method = POST
> 
> 请求参数：
> 
> 1. token：用户自行设定的token
> 2. filename: 删除的文件名
> 
> return：下载对应文件

文件删除接口，身份验证成功，系统会删除该文件，同时删除git中相应文件。

#### 2.2.7 flush

> URL = http(s)://{host}/flush
> 
> Method = POST
> 
> 请求参数：
> 
> 1. token：用户自行设定的token
> 
> return：

静态文件生成接口，用来解决在某些情况下更新文件后但静态文件没有自动生成的问题。通过请求该接口，强制重新生成静态文件。

## 3. 配置文件
配置文件为`config.json`，默认内容如下：
``` json
{   
    "post_path": "post_path",
    "deploy_cmd": "command",
    "front_matters": ["date", "tags", "comments", "title", "categories", "layout", "updated", "permalink", "keywords"],
    "remote_git": "https://github.com",
    "local_git_path": "local_git_path",
    "timer": 60.0,
    "webhook_used": true,
    "webhook_secret": "key",
    "request_log": "./log/request.log",
    "custom_log": "./log/custom.log",
    "system_log":  "./log/system.log",
    "extends": {},
    "markdown_file_class": "Markdown_File",
    "token": "pwd",
    "bind": "0.0.0.0",
    "port": 5000,
    "blog_url": "",
    "git": "github"
}
```

| 参数名 | 参数含义 | 参数类型 | 默认值 |
| :---- | :---- | :---- | :---- |
| post_path | hexo目录下md文件所在目录，默认为`/{hexo目录}/source/_posts/` | `str` | 需要用户配置 |
| deploy_cmd | hexo生成静态文件的命令，一般为`hexo g`，具体需要根据实际环境部署情况来定 | `str` | 需要用户配置 |
| front_matters | hexo文件头部信息列表，详见[官网][5] | `list` | 默认值如上所示  |
| remote_git | git库地址 | `str` | 需要用户配置 |
| local_git_path | git clone后本地git目录，使用git clone时需要使用ssh的链接，否则会无法push | str | 需要用户配置 |
| timer | 不使用github回调的方式就会定时执行git操作来检查是否有文件更新 | `float` | `60.0` |
| webhook_used | 是否使用github回调 | `bool` | `true` |
| webhook_secret | 使用github回调的方法时，在github上设置的密钥 | `str` | 需要用户配置 |
| request_log | 网络请求日志文件 | `str` | 默认值如上 |
| custom_log | 自定义输出日志文件 | `str` | 默认值如上 |
| system_log | 系统输出日志文件 | `str` | 默认值如上 |
| extends | 自定义Markdown_File方法时需要的额外参数，详见[扩展/自定义](#5-%e6%89%a9%e5%b1%95%e8%87%aa%e5%ae%9a%e4%b9%89) | `dict` | 默认值如上 |
| markdown_file_class | 处理markdown文件使用的类，可自定义，详见[扩展/自定义](#5-%e6%89%a9%e5%b1%95%e8%87%aa%e5%ae%9a%e4%b9%89) | `str` | `Markdown_File` |
| token | 在线管理文件：上传、查看、下载、删除时的身份验证信息 | `str` | 默认值如上，强烈建议修改 |
| bind | flask监听地址 | `str` | `0.0.0.0` |
| port | flask监听端口 | `int` | `5000` |
| blog_url | 显示在管理页面上的个人博客跳转地址，为空时则管理页面不显示跳转链接 | `str` | 默认为空 |
| git | 所使用的git系统，目前支持`github`和`gitee(码云)` | `str` | 默认`github` |

## 4. 使用方法
### 4.1 准备工作

1. 一台vps，操作系统为Ubuntu 16.04，其他操作系统上的相关命令可以参考给出的官方文档链接
2. 一个空的git仓库（可以含有README），国外的vps可以选择[Github][15]，国内的vps可以选择[Gitee][16]

### 4.2 环境配置
环境配置部分分为两种方法：

1. 不使用docker
2. 使用docker

#### 4.2.1 不使用docker
##### 4.2.1.1 Hexo
这部分是按照[官方][6]的教程进行安装：
安装Node.js环境，可以参考：[nodesource][7]
```shell
    # 这里如果安装最新的14.x会导致hexo出错，所以选择了相对稳定无错的12.x版本，如果本身为root用户则可删除"sudo -E"
    curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
    sudo apt install -y nodejs
    # 默认nodejs使用的源在国内下载会比较慢，如果vps是所在地是国内，可以使用以下命令更换为淘宝镜像
    # npm config set registry https://registry.npm.taobao.org
    sudo npm install -g hexo-cli
    # 配置git环境
    sudo apt install -y git
```
至此，hexo所需要的基本环境已经搭建完毕。接下来需要初始化一个目录作为blog目录。此处以`/home/blog`为例，初始化的目录需要为空，否则会报错。
```shell
    sudo mkdir /home/blog && cd /home/blog
    hexo init
    npm install hexo-server --save
```

##### 4.2.1.2 配置git-ssh
配置git-ssh是为了在与git系统交互的过程中无需手动输入密码，这部分可以参考[掘金][8]上的帖子。使用[码云][16]参见[官方文档][17]。

##### 4.2.1.3 创建并拉取git备份仓库
拉取远程备份仓库，例如我这里创建的为`https://github.com/lureiny/test_blog`，其中仅包含一个README.md文件。
```shell
    # 这里clone时一定要使用ssh的链接，否则git push时会需要输入用户名，这在上述的帖子中有提到
    cd /home/ && git clone git@github.com:lureiny/test_blog.git "blog_bak"
```

##### 4.2.1.4 配置python环境
这里使用miniconda进行配置
```shell
    cd /home && wget "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" -O "miniconda.sh"
    bash miniconda.sh
    source ~/.bashrc
    # 这两步是创建并切换虚拟环境，如果机器上只有这么一个项目使用了python，那此步可以选择省略
    # conda create -n hexo python=3.6
    # conda activate hexo
```
至此python环境搭建完

##### 4.2.1.5 安装screen
screen是用来解决终端断开时进程自动终止问题的一个程序，因为无论是`python`进程还是`hexo server`都不是后台进程，这就导致我们退出终端时进程会自动中断，因此使用screen来解决这个问题
```shell
    sudo apt install screen
```
screen简单入门参考：[菜鸟教程][9]

##### 4.2.1.6 使用Simple-Hexo-Online-Manage-Tool
```shell 
    cd /home && git clone git@github.com:lureiny/Simple-Hexo-Online-Manage-Tool.git "shomt" && cd shomt
    pip install -i requestments.txt
    # 修改配置文件
    vim config.json
```
针对此用例的配置如下

> post_path: "/home/blog/source/_posts"
> 
> deploy_command: "cd /home/blog/ && hexo g"
> 
> remote_git: "git@github.com:lureiny/test_blog.git"
> 
> local_git_path: "/home/blog_bak"
> 
> webhook_secret: "test"
> 
> token: "token"
> 
> 其他参数默认

```shell
    # 新建一个screen窗口并启动hexo进程
    screen -S hexo 
    cd /home/blog/ 
    hexo server -s
    # 退出当前screen窗口 ctrl+A+D，之后我们想重新进入窗口，我们只需要执行screen -r hexo
    # 建一个screen窗口并启动Simple-Hexo-Online-Manage-Tool进程
    screen -S shomt
    cd /home/shomt
    python3 hexo.py
    # 退出当前screen ctrl+A+D
```

##### 4.2.1.7 访问
至此，访问http(s)://{host}:5000可以看到管理页面，访问http(s)://{host}:4000可以看到博客页面，这里我建议使用Nginx作为网络服务器反向代理本地的4000和5000端口

##### 4.2.1.8 配置webhook
在github备份项目页面（本例中: `https://github.com/lureiny/test_blog`），webhook设置在`Settings`->`Webhooks`->`Add webhook`。
在`Payload URL`中填入回调链接：`http(s)://{host}:5000/webhook`，`Content type`选择`application/json`，`Secret`中填入[配置文件](#3-配置文件)中`webhook_secret`对应的值。使用[码云][16]参见[官方文档][18]。图文说明可参考[简书上的文章][12]中的步骤一。


#### 4.2.2 使用docker（推荐）
##### 4.2.2.1 配置git-ssh
参见[4.2.1.2 配置git-ssh](#4212-配置git-ssh)

##### 4.2.2.2 文件目录准备工作
需要将备份仓库本地目录、shmot本地目录、hexo blog目录放在同一个目录下，然后将这个目录挂载到容器的`/home`目录下，例如本例中将三个目录均放到宿主机的`/home`目录下。

* 备份仓库本地目录: `/home/blog_bak`
* shmot本地目录: `/home/shomt`
* hexo blog目录: `/home/blog`

对应的命令如下:
```shell
    cd /home
    git clone {备份仓库远程地址，一定要使用`ssh`的地址} "blog_bak"
    git clone git@github.com:lureiny/Simple-Hexo-Online-Manage-Tool.git "shomt"
    mkdir /home/blog                               # 如果是新的blog才需要创建这个目录，如果已经有hexo init初始化后的blog目录，则跳过此步
```

##### 4.2.2.3 配置docker
这里给出的是基于ubuntu16.04的安装命令，其他操作系统可以参考：[官方文档][10]
```shell
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
```
因为这里要使用到`docker-compose`命令，因此还需要安装`docker-compose`：[官方文档][11]

> 国内vps的下载的速度可能会有一些慢，可以本地下载文件之后上传到/usr/local/bin目录下

```shell
    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
```

##### 4.2.2.4 修改docker-compose配置文件
docker-compse的配置文件在`shomt/docker`目录下，可以按照注释说明进行修改，其他保持默认即可。docker配置文件（docker-compose.yml）默认如下：

```yml
    version: "3"

    services:
    hexo:
        build: ./
        ports:                                       # 冒号前数字为宿主机端口，冒号后为容器内端口
        - "4000:4000"                                # 这里是Hexo server的端口，容器内端口为4000，如果宿主机4000端口没有被占用，则不需要修改
        - "5000:5000"                                # 这里是Flask的端口，容器内端口默认为5000，这个端口和配置文件(shomt/config.json)中的port相同，如果宿主机5000端口没有被占用，则不需要修改
        tty: true
        command: /bin/sh /root/start.sh
        container_name: hexo
        environment:
        - GIT_CONFIG_EMAIL=""                        # git的全局email设置，建议改成github注册用的邮箱
        - GIT_CONFIG_NAME=""                         # git的全局name设置，建议改成github用户名
        - HEXO_BLOG=/home/blog                       # 容器内对应的hexo blog目录                     # 如果目录结构和示例的目录结构相同，则这里可以不改
        - SHOMT=/home/shomt                          # 容器内对应的shmot目录                         # 如果目录结构和示例的目录结构相同，则这里可以不改
        volumes:
        - /root/.ssh:/root/.ssh:ro                   # ssh密钥的目录，如果是root账户，这里可以不改；如果不是root账户，则应该修改第一个冒号前的路径为操作用户的根目录
        - /home:/home                                # 备份仓库本地目录、shmot本地目录、hexo blog目录所在目录      # 如果目录结构和示例的目录结构相同，则这里可以不改
        - /etc/localtime:/etc/localtime:ro
        - ./start.sh:/root/start.sh                           
```

##### 4.2.2.5 修改shomt配置文件
参考[配置文件](#3-配置文件)和[使用Simple-Hexo-Online-Manage-Tool](#4216-使用simple-hexo-online-manage-tool)

##### 4.2.2.6 启动docker
```shell
    cd /home/shomt/docker
    sudo docker-compose up -d
```
如果是初始化一个空目录，这里需要等待一段时间对应的4000端口才能访问，等待时间视网络情况而定。

##### 4.2.2.7 访问
至此，访问http(s)://{host}:5000可以看到管理页面，访问http(s)://{host}:4000可以看到博客页面，这里我建议使用Nginx作为网络服务器反向代理本地的4000和5000端口。

##### 4.2.2.8 配置webhook
参见[配置webhook](#4218-配置webhook)

### 4.3 在网页上管理
管理页面链接：`http(s)://{host}:5000/`，打开后显示如下。在token输入框中输入[配置文件](#3-配置文件)中设置的`token`。如果token不正确，则无法在页面上进行任何操作。
![管理页面][13]
#### 4.3.1 查看文件列表
输入好token后，点击`显示文件列表`，页面会动态加载出当前博客目录下的文件信息，效果如下。列表中包含文件名、title、发布时间、更新时间、以及提供了下载和删除的操作。
![查看文件列表][14]

#### 4.3.2 上传
`输入token`->`选择文件`->`上传文件`，文件名可带空格，系统会自动处理这类文件名。上传成功后系统会自动刷新出文件列表。因为上传和删除时后台系统需要与远端git服务器进行沟通，如果使用github的话，需要等待的时间略久，并不是提交不成功。

#### 4.3.3 下载
`输入token`->点击对应的`下载`按钮

#### 4.3.4 删除
`输入token`->点击对应的`删除`按钮

#### 4.3.5 强制生成静态文件
`输入token`->`生成静态文件`按钮，系统会强制重新生成静态文件

### 4.4 通过git管理
`git clone`备份仓库到本地。直接在本地进行修改、提交、推送即可。使用github会有一定的延迟，需要耐心等待，一般3-5s后刷新页面即可。

#### 4.4.1 新增
在根目录下创建新的`markdown`文件，`编辑`->`commit`->`push`即可。

#### 4.4.2 更新
`git pull`拉取最新的版本后，`编辑`->`commit`->`push`即可。

> 更新`Front-matter`时，新增的`Front-matter`仅需要直接添加即可，对于需要删除的项，在标签前面加上`#`后上传即可

#### 4.4.3 删除
`git pull`拉取最新的版本后，`删除文件`->`commit`->`push`即可。

#### 4.4.4 备份
通过引入blog备份仓库，实现了版本管理与博客的备份。全部发布过的博客都可以通过git系统进行备份和版本管理。

## 5. 扩展/自定义
不同主题的`Front-matters`可能会略有不同。比如`ButterFly`主题与[Heox官方][4]默认主题相比，`Front-matters`中可选的多了`top_img`和`cover_img`等，在[markdown.py](/markdown.py)中的`Markdown_File_ButterFly`类继承了`Markdown_File`类，并通过配置文件中`extends`来配置额外所需要的参数`{"img_path": "/img/background_img", "imgs_path": "/home/blog/themes/Butterfly/source/img/background_img"}`，重写了`_generate_front_matter`方法，该方法主要功能就是生成默认`Front-matters`信息。通过这种形式，实现自定义，按照自己的需求来重新设计文件默认`Front-matters`格式。



[1]: https://developer.github.com/webhooks/     "Webhook官方文档"
[2]: https://dash.lureiny.top/images/2020/04/28/Hexo_-12550ac30386e6250.png      "上传接口流程图"
[3]: https://dash.lureiny.top/images/2020/04/28/1779d53c11e8a14a9.png            "git push流程图"
[4]: https://hexo.io/zh-cn/
[5]: https://hexo.io/zh-cn/docs/front-matter
[6]: https://hexo.io/zh-cn/docs/
[7]: https://github.com/nodesource/distributions
[8]: https://juejin.im/post/5e491df96fb9a07caf4451f5
[9]: https://www.runoob.com/linux/linux-comm-screen.html
[10]: https://docs.docker.com/engine/install/ubuntu/           "Docker Engine"
[11]: https://docs.docker.com/compose/install/            "docker-compose"
[12]: https://www.jianshu.com/p/55209f1031e8              "webhook参考"
[13]: https://dash.lureiny.top/images/2020/05/04/ebec7926ee11d6709f90bc5a8fd2d462.png
[14]: https://dash.lureiny.top/images/2020/05/04/5dba907ee1635017282d0367857cc0a2.png
[15]: https://github.com
[16]: https://gitee.com/
[17]: https://gitee.com/help/articles/4238
[18]: https://gitee.com/help/categories/40