## 消息队列连接
RMQ_SERVER = "localhost"
RMQ_PORT = 5672
RMQ_USER = "username"
RMQ_PASS = "password"
RMQ_SERVER_CERT = "/path/to/cert.pem"
## 直播间ID（URL中那个）
LIVEROOM_ID = "22637261"

## 各个弹幕类型保存的表名后缀
DM_TABLE_NORMAL = "danmaku"
DM_TABLE_GIFT = "gift"
DM_TABLE_GUARD = "guard"
DM_TABLE_SUPER_CHAT = "super_chat"

## 执行合并操作时数据库连接
SQL_CONNECTION = "mariadb+mysqldb://username:password@some-remote-host:23306/bilibili-danmaku-record"

## 表名分隔符
TABLE_SEP = "__"
