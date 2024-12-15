# 基于Django的在线电商平台

### 1.技术栈

`Django+RESTful Framework+Celery+MySQL+Redis+JWT`

`Celery`用来异步处理邮件发送等任务

`Redis`用来对商品列表和商品详细信息进行缓存

### 2.配置要求

`Python`包配置参照`requirements.txt`

数据库使用`MySQL`，在`market01/market01/settings`的`DATABASES`中进行配置

### 3.接口配置

接口相应请求通过`Postman`测试发送，需要在相应环境中设置变量

| Variables     | content               |
| ------------- | --------------------- |
| host          | http://127.0.0.1:8000 |
| token         | xxx                   |
| refresh_token | xxx                   |

并通过`Scripts/Post-res`配置刷新`token`的设置

```js
var jsonData = pm.response.json();
pm.environment.set("token", jsonData.token);
pm.environment.set("refresh_token", jsonData.refresh);
```

### 4.个人密钥配置

#### 4.1邮箱配置

将`market01/market01/settings`中的`EMAIL_HOST_PASSWORD`以及`EMAIL_HOST_USER`改为自己的邮箱和密码

#### 4.2支付宝沙箱配置

将`market01/market01/settings`中的`ALIPAY_APPID`改为自己申请的支付宝沙箱`ID`，同时在`static/key_file`中添加应用公钥、私钥以及相应的支付宝公钥



