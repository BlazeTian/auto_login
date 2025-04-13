import time
import pywifi
from pywifi import const
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webbrowser
import requests
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

def scan_wifi():
    """扫描可用的WiFi网络并打印列表"""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # 获取第一个无线网卡
    
    print("正在扫描WiFi网络...")
    iface.scan()  # 扫描网络
    time.sleep(5)  # 等待扫描完成
    
    scan_results = iface.scan_results()
    
    print(f"找到{len(scan_results)}个WiFi网络:")
    for i, result in enumerate(scan_results):
        print(f"{i+1}. {result.ssid} (信号强度: {result.signal})")
    
    return scan_results

def connect_to_wifi(ssid, password=""):
    """连接到指定的WiFi网络"""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    
    # 断开当前连接
    if iface.status() == const.IFACE_CONNECTED:
        print("断开当前WiFi连接...")
        iface.disconnect()
        time.sleep(1)
    
    # 创建WiFi连接配置
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    
    if password:
        profile.akm = [const.AKM_TYPE_WPA2PSK]
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
    else:
        profile.akm = [const.AKM_TYPE_NONE]
    
    # 添加新的连接配置
    temp_profile = iface.add_network_profile(profile)
    
    # 尝试连接
    print(f"正在连接到 {ssid}...")
    iface.connect(temp_profile)
    
    # 等待连接完成
    time.sleep(5)
    
    # 检查连接状态
    if iface.status() == const.IFACE_CONNECTED:
        print(f"成功连接到 {ssid}")
        return True
    else:
        print(f"连接到 {ssid} 失败")
        return False

def find_and_connect_cmcc_edu():
    """查找并连接到信号最强的xxxx网络"""
    wifi_list = scan_wifi()
    
    # 查找所有CMCC-EDU网络
    cmcc_edu_networks = []
    for result in wifi_list:
        if result.ssid == "xxxxxxx": #xxxxxxx为你的WiFi名称
            cmcc_edu_networks.append(result)
    
    if cmcc_edu_networks:
        # 按信号强度排序（信号强度是负值，数值越大越强）
        cmcc_edu_networks.sort(key=lambda x: x.signal, reverse=True)
        strongest_network = cmcc_edu_networks[0]
        
        print(f"找到{len(cmcc_edu_networks)}个CMCC-EDU网络，选择信号最强的一个（信号强度：{strongest_network.signal}）")
        connect_result = connect_to_wifi("CMCC-EDU")
        return connect_result
    else:
        print("未找到CMCC-EDU网络")
        return False

def web_login(username, password, login_url="在此处填上校园网登录页面的url即可"):
    """在网页上自动登录"""
    print("检查网络连接状态...")
    
    try:
        # 检查网络连接状态
        response = requests.get("https://www.baidu.com", timeout=5)
        if response.status_code == 200:
            print("已经可以访问互联网，无需登录")
            return True
    except requests.exceptions.RequestException:
        print("网络连接受限，需要登录认证")
    
    # 配置Chrome浏览器选项
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 无头模式（不显示浏览器窗口）
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁用日志
    chrome_options.add_argument("--start-maximized")  # 最大化窗口
    
    driver = None
    try:
        print("启动浏览器...")
        # 初始化WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # 尝试可能的登录URL
        possible_urls = [
            "http://www.msftconnecttest.com/redirect",  # 微软捕获页面，最可能的重定向
            login_url,                                 # 指定的登录URL
            "在此处填上校园网登录页面的url即可"                        # 直接IP
        ]
        
        login_page_found = False
        
        for url in possible_urls:
            try:
                print(f"尝试访问: {url}")
                driver.get(url)
                time.sleep(5)  # 增加等待时间，等待可能的重定向
                
                # 打印当前URL，帮助调试
                current_url = driver.current_url
                print(f"当前页面URL: {current_url}")
                
                # 截图记录当前页面
                try:
                    driver.save_screenshot(f"page_{possible_urls.index(url)}.png")
                except Exception:
                    pass
                
                # 尝试检测是否存在登录页面的特征
                page_source = driver.page_source
                if "DDDDD" in page_source and "upass" in page_source and "0MKKey" in page_source:
                    print("检测到登录页面特征")
                    login_page_found = True
                    break
            except Exception as e:
                print(f"访问 {url} 时出错: {e}")
                continue
        
        if not login_page_found:
            print("尝试截取当前页面截图以便调试...")
            try:
                screenshot_path = "login_page.png"
                driver.save_screenshot(screenshot_path)
                print(f"已保存页面截图到 {screenshot_path}")
            except Exception as e:
                print(f"截图失败: {e}")
            
            print("无法找到登录页面，放弃登录")
            if driver:
                driver.quit()
            return False
        
        # 使用JavaScript直接修改DOM并提交表单
        print("使用JavaScript直接填写表单并提交...")
        
        try:
            # 直接通过JavaScript设置输入框的值
            js_code = f"""
            (function() {{
                console.log('开始执行登录脚本');
                
                // 查找输入元素
                var usernameField = document.getElementsByName('DDDDD')[0];
                var passwordField = document.getElementsByName('upass')[0];
                var loginButton = document.getElementsByName('0MKKey')[0];
                
                if (!usernameField || !passwordField || !loginButton) {{
                    console.log('找不到登录表单元素');
                    return false;
                }}
                
                // 填写表单
                console.log('设置用户名和密码');
                usernameField.value = '{username}';
                passwordField.value = '{password}';
                
                // 等待一小段时间后提交
                setTimeout(function() {{
                    console.log('点击登录按钮');
                    loginButton.click();
                }}, 500);
                
                return true;
            }})();
            """
            
            # 执行JavaScript
            result = driver.execute_script(js_code)
            print(f"JavaScript执行结果: {result}")
            
            # 截图记录表单提交状态
            time.sleep(1)
            driver.save_screenshot("form_submitted.png")
            
            # 等待登录处理完成
            print("等待登录处理完成...")
            time.sleep(8)
            
            # 尝试另一种方法：使用原生JavaScript表单提交
            js_form_submit = """
            (function() {
                var form = document.getElementsByName('f3')[0];
                if (form) {
                    console.log('找到表单，准备提交');
                    form.submit();
                    return true;
                } else {
                    console.log('找不到表单');
                    return false;
                }
            })();
            """
            
            try:
                result = driver.execute_script(js_form_submit)
                print(f"表单提交脚本执行结果: {result}")
                time.sleep(5)
            except Exception as e:
                print(f"表单提交脚本执行失败: {e}")
            
            # 再一次尝试：直接用JavaScript注入表单并提交
            js_inject_form = f"""
            (function() {{
                // 创建并提交临时表单
                var tempForm = document.createElement('form');
                tempForm.method = 'post';
                tempForm.action = '';
                
                var userInput = document.createElement('input');
                userInput.type = 'hidden';
                userInput.name = 'DDDDD';
                userInput.value = '{username}';
                tempForm.appendChild(userInput);
                
                var passInput = document.createElement('input');
                passInput.type = 'hidden';
                passInput.name = 'upass';
                passInput.value = '{password}';
                tempForm.appendChild(passInput);
                
                var submitInput = document.createElement('input');
                submitInput.type = 'hidden';
                submitInput.name = '0MKKey';
                submitInput.value = '登录';
                tempForm.appendChild(submitInput);
                
                document.body.appendChild(tempForm);
                console.log('注入临时表单');
                tempForm.submit();
                console.log('提交临时表单');
                return true;
            }})();
            """
            
            try:
                result = driver.execute_script(js_inject_form)
                print(f"表单注入脚本执行结果: {result}")
                time.sleep(5)
            except Exception as e:
                print(f"表单注入脚本执行失败: {e}")
            
            # 截图记录最终状态
            driver.save_screenshot("final_state.png")
            
            # 检查登录结果
            print("验证网络连接...")
            try:
                # 尝试访问百度来验证是否已联网
                driver.get("https://www.baidu.com")
                WebDriverWait(driver, 15).until(
                    EC.title_contains("百度")
                )
                print("登录成功！能够访问互联网")
                logged_in = True
            except Exception as e:
                print(f"验证网络连接失败: {e}")
                
                # 最后一次尝试：模拟浏览器自动打开捕获门户的行为
                try:
                    print("尝试模拟浏览器自动重定向到捕获门户...")
                    driver.get("http://detectportal.firefox.com/success.txt")
                    time.sleep(3)
                    
                    # 检查是否被重定向到登录页面
                    current_url = driver.current_url
                    print(f"当前URL: {current_url}")
                    
                    if "10.11.1.3" in current_url or "login" in current_url.lower():
                        print("已重定向到登录页面，再次尝试登录")
                        
                        # 尝试再次登录
                        driver.execute_script(js_code)
                        time.sleep(8)
                        
                        # 再次验证
                        driver.get("https://www.baidu.com")
                        try:
                            WebDriverWait(driver, 15).until(
                                EC.title_contains("百度")
                            )
                            print("第二次尝试登录成功！")
                            logged_in = True
                        except:
                            print("第二次尝试登录失败")
                            logged_in = False
                    else:
                        logged_in = False
                except Exception as e:
                    print(f"模拟捕获门户重定向失败: {e}")
                    logged_in = False
            
            # 关闭浏览器
            if driver:
                driver.quit()
            return logged_in
            
        except Exception as e:
            print(f"JavaScript操作过程中出错: {e}")
            if driver:
                driver.quit()
            return False
        
    except Exception as e:
        print(f"浏览器自动化过程中出错: {e}")
        if driver:
            try:
                driver.quit()
            except:
                pass
        return False

if __name__ == "__main__":
    try:
        # 连接到WiFi
        wifi_connected = find_and_connect_cmcc_edu()
        
        if wifi_connected:
            # 进行网页登录
            username = "xxxxxxx"  # 替换为实际用户名
            password = "xxxxxxx"  # 替换为实际密码
            login_success = web_login(username, password)
            
            if login_success:
                print("自动登录完成！现在可以使用网络了。")
            else:
                print("自动登录失败，请检查账号密码或网络状况。")
        else:
            print("WiFi连接失败，无法进行登录。")
    except Exception as e:
        print(f"发生错误: {e}") 