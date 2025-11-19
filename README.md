# wxocr

提供微信OCR功能封装，HTTP接口调用。与[Fork的原项目](https://github.com/golangboy/wxocr)相比，区别如下：

1. 增加授权key验证，防止部署于互联网时被恶意调用。
2. OCR接口返回格式与微信原始数据一致。
3. 需要单独安装微信OCR引擎，即[微信（Linux）](https://linux.weixin.qq.com/)，默认路径在`/opt/wechat`）。

## 项目简介

wxocr 是一个基于Flask的微信OCR服务，提供HTTP API接口进行图像文字识别。项目包含以下特性：

- **OCR识别**：基于微信OCR引擎的图像文字识别
- **API密钥认证**：支持可选的API密钥验证机制
- **HTTP接口**：RESTful API设计，易于集成

## 基于以下条件开发

- Python 3.13+
- Flask
- PDM包管理器
- 微信OCR引擎（需安装[微信（Linux）](https://linux.weixin.qq.com/)，默认路径在`/opt/wechat`）


## 安装与运行

### 1. 安装依赖
```bash
# 克隆项目
git clone https://github.com/unclemcz/wxocr.git
cd wxocr

# 使用PDM安装依赖
pdm install
```

### 2. 初始化（清空测试数据）授权码
```bash
# 初始化数据库表结构
pdm run flask --app wxocr init-db
```

### 3. 运行服务
```bash
# 开发模式运行
pdm run flask --app wxocr run --debug
```

## API接口

### OCR识别接口

**接口地址：** `POST http://localhost:5000/ocr`

**请求参数：**
```json
{
    "key": "your_api_key",      // 可选：API密钥（如果启用了密钥验证）
    "image": "base64_image_data" // 必需：Base64编码的图像数据
}
```

**响应格式：**
wxocr原始返回格式
```json
{"imgpath": "temp/demo.png", "errcode": 0, "width": 173, "height": 46, "ocr_response": [{"text": "demodemo", "left": 8.379687309265137, "top": 11.623435020446777, "right": 168.67495727539062, "bottom": 40.00624084472656, "rate": 0.9961945414543152}]}
```

**使用示例：**

### 1. 基本调用（无API密钥）
```bash
curl -X POST http://localhost:5000/ocr \
     -H "Content-Type: application/json" \
     -d '{"image": "BASE64_ENCODED_IMAGE_DATA"}'
```

### 2. 带API密钥调用
```bash
curl -X POST http://localhost:5000/ocr \
     -H "Content-Type: application/json" \
     -d '{"key": "your_api_key", "image": "BASE64_ENCODED_IMAGE_DATA"}'
```

## API密钥管理

授权码功能用于对调用者进行授权，防止恶意调用。

### 授权逻辑

1. **公开访问模式**：如果授权码列表为空，则默认可以公开访问，不判断传入的授权码
2. **授权访问模式**：如果授权码列表不为空，则验证传入的授权码是否在列表中，不在则拒绝访问
3. **灵活配置**：可以随时切换公开/授权访问模式

### API密钥管理命令

#### 1. 添加API密钥
```bash
pdm run flask --app wxocr add-key --appname=your_app_name
```
示例：
```bash
pdm run flask --app wxocr add-key --appname=test_app
# 输出示例：Added a api key: a1b2c3d4e5f6789a1b2c3d4e5f6789a for app: test_app
```

#### 2. 删除API密钥
```bash
pdm run flask --app wxocr del-key --appname=your_app_name
```
示例：
```bash
pdm run flask --app wxocr del-key --appname=test_app
# 输出示例：Deleted a api key: test_app
```

#### 3. 列出所有API密钥
```bash
pdm run flask --app wxocr list-keys
```
输出示例：
```
ID    App Name             API Key
------------------------------------------------------------
1     test_app             a1b2c3d4e5f6789a1b2c3d4e5f6789a
2     demo_app             b2c3d4e5f6789a1b2c3d4e5f6789a1b
```

#### 4. 清空所有API密钥
⚠️ **警告**：清空后接口将允许公开访问，请谨慎操作！
```bash
pdm run flask --app wxocr clear-keys
# 输出示例：API keys cleared.
```

#### 5. 初始化（清空测试数据）授权码
```bash
pdm run flask --app wxocr init-db
# 输出示例：Initialized the database.
```
## 故障排除

### 常见问题

1. **微信OCR引擎初始化失败**
   - 确认微信已正确安装在  `/opt/wechat`

2. **数据库连接错误**
   - 确认已执行 `init-db` 命令初始化数据库

3. **API密钥验证失败**
   - 使用 `list-keys` 命令确认密钥是否存在
