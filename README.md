## 介绍：一个分享心情的网站：liveshare

 ...效果图详见目录： image

## 1.主要功能：

​	。文章，页面，分类目录，编辑，添加，删除文章，支持富文本编辑器。

​	。支持滑动验证码登录。

​	。支持QQ互联，扫码登录。（微信因为申请不了账号暂时不写）

​	。支持FastDFS文件分布式存储系统。

​	。集成celery发送邮件，手机短信。

​	。集成支付宝支付功能

​	。基于物品协同过滤推荐算法，推荐文章。   

## 2.安装

### 2.1 pip安装： 

`pip install -Ur requirements.txt`

### 2.2 修改配置

linux下配置都是在settings中的dev文件中，配置文件修改如下：

​		数据库创建：create  database charset=utf8mb4

​		数据库配置如下：

			  DATABASES = {
	"default": {
	    "ENGINE": "django.db.backends.mysql",
	    "HOST": "127.0.0.1",
	    "PORT": 3306,
	    "USER": "root",
	    "PASSWORD": "123",
	    "NAME": "liveShare",
	}
	}
### 2.3  安装Docker：

更新ubuntu的apt源索引:

```bash
sudo apt-get update
```

安装包允许apt通过HTTPS使用仓库

```
sudo dpkg --configure -a
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```

添加Docker官方GPG key

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

设置Docker稳定版仓库

```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

添加仓库后，更新apt源索引

```
sudo apt-get update
```

最新版Docker CE（社区版）

```
sudo apt-get install docker-ce
```



### 2.4 配置FastDFS：

到docker中使用search搜索已有的FastDFS Docker镜像来部署和运行

```
sudo docker search fastdfs
```

镜像下载

```
sudo docker pull season/fastdfs
```

开启运行FastDFS的tracker和storage

```
sudo docker image ls
```



### 2.5 运行tracker

查看fastdfs的端口是否被占用

```
netstat -aon | grep 22122
```

在家目录下创建tracker调度服务器器的运行目录tracker_data，

```
mkdir ~/tracker_data
```

并创建容器开启tracker服务

```
sudo docker run -itd --name tracker -v ~/tracker_data:/fastdfs/tracker/data --net=host season/fastdfs tracker
```

查看tracker是否运行起来

```
sudo docker container ls
```



### 2.6 运行storage

查看本机ip

```
ifconfig -a
```

本机创建目录

```
mkdir ~/storage_data  # 存储服务器的运行目录
mkdir ~/store_path    # 存储服务器保存文件目录
```

开启storage服务

```
sudo docker run -itd --network=host --name storage -v ~/storage_data:/fastdfs/storage/data -v ~/store_path:/fastdfs/store_path  -e TRACKER_SERVER:192.168.226.150:22122 season/fastdfs storage
```



### 2.7 调整配置

进入storage容器下，将fdfs_conf目录下的storage.conf文件拷贝到当前用户家目录下

```
 # 从本机复制指定文件到容器内部
sudo docker cp storage:/fdfs_conf/storage.conf ~/
```

找到tracker_server配置项，修改为本地IP地址

```
tracker_server=192.168.226.150:22122
```

将编辑好的文件再从本机拷贝到容器storage内部

```
sudo docker cp ~/storage.conf  storage:/fdfs_conf/
sudo docker cp ~/storage.conf  tracker:/fdfs_conf/
```

重启storage存储服务器

```
sudo docker container stop storage
sudo docker container start storage
```

进入tracker调度服务器容器中，查看调度服务器和存储服务器是否连接上了

```
sudo docker exec -it storage bash
cd /fdfs_conf/
fdfs_monitor storage.conf
```



## 3.运行

1.执行后端工程中的build.sh脚本，cd /usr/local/nginx/sbin中 启动FastDFS的nginx。

2.执行main.sh脚本



## 4.相关问题

有任何问题欢迎加QQ1980575315 进行交流沟通。