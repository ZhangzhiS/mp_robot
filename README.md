# 找谱机器人

## 部署

### 1. 输入环境变量

```bash
export WECHATY_LOG="verbose"                                                                  
export WECHATY_PUPPET="wechaty-puppet-wechat"
export WECHATY_PUPPET_SERVER_PORT="8080"
export WECHATY_TOKEN="python-wechaty-uos-token"
export WECHATY_PUPPET_SERVICE_NO_TLS_INSECURE_SERVER="false"
```

### 2. 启动wechaty容器

```bash
docker run -tid --name wechaty_puppet_service_token_gateway \
--rm \
-e WECHATY_LOG="verbose" \
-e WECHATY_PUPPET="wechaty-puppet-wechat" \
-e WECHATY_PUPPET_SERVER_PORT="8080" \
-e WECHATY_TOKEN="python-wechaty-uos-token" \
-p "8080:8080" \
-v /root/project/score-robot/wechaty:/wechaty \
wechaty/wechaty:0.65
```

由于登录信息保存在容器中，所以最好把容器中的`/wechaty`路径复制出来，挂载在硬盘中，避免每次重启容器都得重新登录

从容器中复制出来
```
docker cp c511d28b2005:/wechaty ./wechaty
```

启动容器的时候增加挂载路径
```bash
-v /root/wechaty:/wechaty
```

### 3. 安装python依赖

```bash
pip install -r requirements.txt
```

### 4. 增加supervisor配置

```
[program:score-robot]
process_name=%(program_name)s
numprocs=1
directory = /root/project/score-robot/score-robot-master
command = /root/.miniconda3/envs/score-robot/bin/python /root/project/score-robot/score-robot-master/main.py
autostart = true
startsecs = 3
autorestart = true
startretries = 3000
stopasgroup=true
user = root
redirect_stderr = true
stdout_logfile_maxbytes = 100MB
stdout_logfile_backups = 3
stdout_logfile = /root/logs/score_robot.log
stderr_logfile = /root/logs/score_robot.log
```

启动增加的这个服务

### 5. 增加定时任务

由于此项目使用的微信桥接容器一直在保存聊天记录到内存中，所以会导致占用内存越来越大，所以每日定时重启容器服务以及python
脚本。

增加crontab定时任务

```crontab
00 01 * * * docker  restart  wechaty_puppet_service_token_gateway
01 01 * * * /root/miniconda3/envs/resource/bin/supervisorctl reload
```

## 注意

由于调用了dss的相关接口，所以需要有那边的token，token的有效时间为30天，注意替换。

获取token的方式(修改里面的手机号码为可接收到验证码的手机)：

```bash
python login.py
```

获取到新的token之后会写入到token.json中，替换服务器中的文件即可
