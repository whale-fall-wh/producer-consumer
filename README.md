# producer-consumer
###### 开发环境-python3.8

## docker运行

```
docker-compose up -d
```

## 直接运行

```
安装包
pip install -r requirements.txt
查看所有命令
python main.py -h
运行生产消费任务
python main.py
```

## 项目目录结构

```
├─ app
│  ├─ consumers                 消费者目录
│  ├─ crawlers                  爬虫
│  │  ├─ elements               解析页面元素
│  ├─ entities                  
│  ├─ enums                     枚举类型
│  ├─ exceptions                异常
│  ├─ producers                 生产者目录
│  ├─ proxies                   代理插件目录
│  ├─ repositories              数据仓库
│  ├─ services                  service
│  ├─ translates                国家翻译
│  ├─ BaseJob.py                生产消费基类
│  ├─ models.py                 模型
├─ storage                      storage
│  ├─ imgs
│  ├─ logs
│  ├─ proies
├─ test                         测试目录
├─ utils                        工具
├─ .dep.yml                     部署文件
├─ .drone.yml                   drone钩子文件
├─ .env                         环境变量
├─ common.py                    常用的方法
├─ docker-compose.yaml          docker-compose
├─ Dockerfile                   dockerfile
├─ main.py                      入口文件
├─ requirements.txt             依赖包
└─ settings.py                  配置文件
```
