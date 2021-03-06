# OCR识别服务

该服务为[我的词典](https://github.com/xxNull-lsk/my_dict) 的OCR识别后端服务，可以实现英语、中文的OCR识别。
## 项目地址
[https://github.com/xxNull-lsk/my_dict_ocr](https://github.com/xxNull-lsk/my_dict_ocr)

## docker镜像下载地址
[https://hub.docker.com/r/xxnull/my_dict_ocr](https://hub.docker.com/r/xxnull/my_dict_ocr)

## 离线镜像下载
[阿里云盘](https://www.aliyundrive.com/s/UeiT3bvffs1)  
[百度网盘](https://pan.baidu.com/s/1jYhvQNSqF-ghJbeeA0MSuw)  
    提取码:`ihbi`

# 安装方法
## 在线安装
```bash
# 安装docker
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
# 拉取镜像
docker pull xxnull/my_dict_ocr:latest
# 启动容器
docker run -d -p 12126:12126 xxnull/my_dict_ocr:latest
```

## 离线安装
```bash
# 下载离线镜像
# 加载镜像
docker load -i xxnull.my_dict_ocr.latest.tar.gz
# 启动容器
docker run -d -p 12126:12126 xxnull/my_dict_ocr:latest
```

**注意：**
`我的词典`启动时会自动拉起OCR服务，无需手动拉起。

# 接口

## 获取版本号

- 协议：`{zmq.REQ}`
- 协议格式： `{json}`
- 输入
```json
{
  "function": "/version"
}
```

| 字段  |  类型 | 含义 |
| ------------ | ------------ | ------ |
|  function |  string | 功能号 |


- 输出
```json
{
    "code": 0,
    "message": "succeed",
    "version":  "xxx"
}
```

| 字段  |  类型 | 含义 |
| ------------ | ------------ | ------ |
| code  |  int | 返回码  |
|  message | string  |  消息 |
|  version | string  |  版本号 |



## 心跳

- 协议：`{zmq.REQ}`
- 协议格式： `{json}`
- 输入
```json
{
  "function": "/tick"
}
```

| 字段  |  类型 | 含义 |
| ------------ | ------------ | ------ |
|  function |  string | 功能号 |


- 输出
```json
{
    "code": 0,
    "message": "succeed"
}
```

| 字段  |  类型 | 含义 |
| ------------ | ------------ | ------ |
| code  |  int | 返回码  |
|  message | string  |  消息 |



## 识别文本

- 协议：`{zmq.REQ}`
- 协议格式： `{json}`
- 输入
```json
{
    "function": "/ocr/get_text",
    "image": "......"
}
```

| 字段  |  类型 | 含义 |
| ------------ | ------------ | ------ |
|  function |  string | 功能号 |
|  image |  string | Base64编码的图片内容 |


- 输出
```json
{
    "code": 0,
    "message": "succeed",
    "data": [
        {
            "rect": [x, y, width, height],
            "text": "识别出来的文本",
            "score": 0.99
        }
    ]
}
```

| 字段  |  类型 | 含义 |
| ------------ | ------------ | ------ |
| code  |  int | 返回码  |
|  message | string  |  消息 |
|  data | arrary  |  识别结果数组 |
|  data[i].rect | array[float]  |  文字的矩形框 |
|  data[i].text | string  |  识别出来的文本 |
|  data[i].score | float  |  置信度 |

### 例子
```python
    import cv2
    import zmq
    import base64

    context = zmq.Context()
    socket: zmq.Socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:12126")

    mat = cv2.imread("./first.png")
    img = cv2.imencode('.jpg', mat)[1]
    data = {
        "function": "/ocr/get_text",
        "image": base64.b64encode(img).decode('utf8')
    }

    socket.send_string(json.dumps(data))
    response = socket.recv_string()
    print(response)
```

# 返回码


| code |  message | 说明 |
| ------------ | ------------ | ------ |
| 0  |  succeed | 成功  |
| -1  |  not support | 不支持的功能号  |

