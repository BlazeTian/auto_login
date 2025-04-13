# 校园网自动登录工具 v1.01

这个工具可以自动扫描WiFi网络、连接到指定的校园网WiFi，然后自动打开浏览器完成网页认证登录，无需人工干预即可完成全过程。

## 功能特点

- 自动扫描可用的WiFi网络并筛选指定的校园网WiFi
- 按信号强度排序，优先连接到信号最强的接入点
- 自动处理网络重定向和捕获页面
- 自动打开浏览器进行网页认证
- 多种方式自动填写账号密码并提交表单
- 验证登录结果以确保网络连接成功
- 详细的状态信息和错误处理

## 安装依赖

```bash
pip install -r requirements.txt
```

依赖项包括：
- pywifi==1.1.12 (WiFi连接功能)
- comtypes==1.1.14 (pywifi的依赖)
- selenium==4.13.0 (网页自动化)
- requests==2.31.0 (网络请求)
- webdriver-manager==4.0.1 (WebDriver管理)

此外，还需要安装Chrome浏览器和对应版本的ChromeDriver。使用webdriver-manager可以自动处理ChromeDriver的下载和安装。

## 使用前配置

使用前需要修改以下几个关键配置：

1. 设置校园网WiFi的名称：
```python
if result.ssid == "xxxxxxx": #xxxxxxx为你的WiFi名称
```

2. 设置校园网登录页面的URL：
```python
def web_login(username, password, login_url="在此处填上校园网登录页面的url即可"):
```

3. 设置您的账号和密码：
```python
username = "xxxxxxx"  # 替换为实际用户名
password = "xxxxxxx"  # 替换为实际密码
```

## 使用方法

1. 确保已安装所有依赖
2. 修改配置信息（WiFi名称、登录URL、账号密码）
3. 以管理员权限运行：

```bash
python wifi_connect.py
```

程序将自动完成以下步骤：
- 扫描并显示可用的WiFi网络
- 连接到指定的校园网WiFi
- 打开浏览器进行网页认证
- 填写账号密码并提交
- 验证连接状态并显示结果

## 调试功能

程序会在运行过程中自动保存多个截图文件，帮助诊断可能的问题：
- `page_*.png`：访问各个可能的登录URL时的页面截图
- `login_page.png`：找不到登录页面时的页面截图
- `form_submitted.png`：表单提交后的页面截图
- `final_state.png`：完成所有操作后的最终页面状态截图

## 工作原理

1. **WiFi扫描与连接**：使用pywifi库扫描可用WiFi网络并排序
2. **网页自动登录**：使用多种方法确保表单填写成功
   - 直接DOM操作
   - 表单注入
   - 捕获门户重定向处理

## 注意事项

- 该程序需要管理员权限才能正常运行
- 需要安装Chrome浏览器
- 首次运行时可能需要下载ChromeDriver（自动处理）
- 网页登录操作需要浏览器界面可见（非无头模式）
- 目前仅在Windows系统上测试通过
- 校园网可能会定期更改登录页面结构，届时可能需要更新代码

## 版本历史

- v1.01：当前版本，改进了表单填写和提交方式，增强了错误处理
- v1.00：初始版本，基本的WiFi连接和网页登录功能

## 后续计划

- 支持更多类型的校园网认证方式
- 添加图形用户界面
- 增加定时重连功能
- 支持配置文件
- 增加记住密码功能
- 添加多平台支持（Linux/MacOS）

## 许可

本项目使用开源许可证，可自由使用和修改。 
