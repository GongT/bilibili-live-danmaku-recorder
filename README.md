## B站（bilibili）直播弹幕收集脚本

可以把弹幕、礼物等数据记录到mysql数据库

## 总体结构
* 多个collector运行在多个网络中，防止中断丢失数据
* 每个collector监听一定量的直播间（blivedm），把弹幕原始数据（JSON）发送到RabbitMQ中
* mapper把从MQ收到的原始数据去重，然后分解成列数据，写入数据库（Mariadb）中
* reducer定时从数据库读取新来的数据，进行一些统计工作（通过自己编写py文件实现）

## 使用方法
### 第一步：运行并设置 RabbitMQ、
// TODO: 怎么做？

### 第二步：启动mapper
```bash
podman run -d docker.io/gongt/bilibili-live-danmu-mapper \
	"--server=用户名:密码@服务器:端口" \       # 之前设置的RabbitMQ连接方式，端口即使默认也必须写明
	"--cacert=/config/server.crt" \          # 如果使用自签名证书，则需要cacert，否则不需要
	"--database=$CONNECTION"                 # 保存数据库的连接方式
```

数据库连接URL格式：    
`mariadb+mysqldb://用户名:密码@服务器地址:端口号/数据库名`

例如：    
`mariadb+mysqldb://bilibili-danmaku-record:bilibili-danmaku-record@127.0.0.1:3306/bilibili-danmaku-record`

使用unix sock连接：    
`mariadb+mysqldb://xxxxxx/yyyyy?unix_socket=/var/run/mysql.sock`

### 第三步：确定collector的参数并运行
```bash
podman run -d docker.io/gongt/bilibili-live-danmu-collector \
	"--server=用户名:密码@服务器:端口" \       # 之前设置的RabbitMQ连接方式，端口即使默认也必须写明
	"--cacert=/config/server.crt" \          # 如果使用自签名证书，则需要cacert，否则不需要
	"--filter=/config/filter.py" \           # 设置弹幕过滤器的文件名，默认不过滤
	"--verbose" \                            # 如果设置，则每个弹幕都会显示出来（将输出大量日志，正常使用不要加这个参数）
	1111 2222 3333                           # 这些是要监听的直播间ID，也就是URL中的数字
```

## reducer逻辑实现
// TODO
