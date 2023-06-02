import re
import requests
import os
from webdriver_manager.core.utils import get_browser_version_from_os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests,re,time,os
import subprocess
import zipfile

def checkDriver():
    browserVersion = get_browser_version_from_os("google-chrome")  # 获取当前系统chrome浏览器的版本号
    mainBrowserVersion = browserVersion.split(".")[0]  # 获取浏览器的主版本号
    resp = requests.get(url="https://chromedriver.storage.googleapis.com/")
    content = resp.text
    availableVersionList = re.search(
        f"<Contents><Key>({mainBrowserVersion}\.\d+\.\d+\.\d+)/chromedriver_win32\.zip</Key>.*?", content, re.S)
    if availableVersionList == None:
        print(f"镜像网站上没有找到主版本号为{mainBrowserVersion}的chromedriver文件，请核实！")
        time.sleep(10)
        os._exit(0)
    else:
        availableVersion = availableVersionList.group(1)
    driver_path = ChromeDriverManager(version=availableVersion).install()  # 找到镜像网站中主版本号与chrome主版本一致的，将匹配到的第一个完整版本号的chromedriver下载使用



def unzip_file(zip_src, dst_dir):
    '''将zip数据解压到workspace/image文件夹'''
    # zip_src源文件夹
    # dst_dir目标文件夹
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')

def downinfo(tarpath,url):
    req = requests.get(url)
    filename = url.split('/')[-1]
    if req.status_code != 200:
        print('下载异常')
        return
    try:
        with open(os.path.join(tarpath,filename), 'wb') as f:
            # req.content为获取html的内容
            f.write(req.content)
            print('下载成功')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    soururl = "https://chromedriver.storage.googleapis.com/"
    browserVersion = get_browser_version_from_os("google-chrome")  # 获取当前系统chrome浏览器的版本号
    mainBrowserVersion = '.'.join(browserVersion.split(".")[0:3])  # 获取浏览器的主版本号
    print('当前浏览器主版本号\t%s'%(mainBrowserVersion))
    resp = requests.get(url=soururl)
    content = resp.text
    BrowserVersion = (mainBrowserVersion+re.findall('<Contents><Key>'+mainBrowserVersion+'(\.\d+)/chromedriver_win32.zip</Key>',content)[-1])
    url = soururl+BrowserVersion+'/chromedriver_win32.zip'
    wherepy = (str(subprocess.check_output('where python', shell=True).decode('UTF-8', 'strict')).split('\n')[0])
    downinfo('./',url)


    name = "chromedriver_win32.zip"  # 在这里修改需要解压的文件夹
    tarpath = os.path.dirname(wherepy)
    unzip_file(zip_src="./" + name, dst_dir=tarpath)




