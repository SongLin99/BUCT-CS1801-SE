import re

import requests
from bs4 import BeautifulSoup
from openpyxl import workbook
from openpyxl import load_workbook


headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
        'Host': 'www.baidu.com'
    }
headers1 =  {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
        'Host': 'baijiahao.baidu.com'
    }


# 获取百家号文章链接
def get_connect(link):
    try:
        r = requests.get(link, headers=headers, timeout=10)
        if 200 != r.status_code:
            return None
        url_list = []
        soup = BeautifulSoup(r.text, "lxml")
        div_list = soup.find_all('div', class_='result-op c-container xpath-log new-pmd')
        for div in div_list:
            mu = div['mu'].strip()
            url_list.append(mu)
            print(mu)
        return get_content(url_list)

    except Exception as e:
        print('e.message:\t', e)
    finally:
        print(u'go ahead!\n\n')


# 获取百家号内容
def get_content(url):
    try:
        clist = []  # 空列表存储文章内容
        r1 = requests.get(url, headers=headers1, timeout=10)
        soup1 = BeautifulSoup(r1.text, "lxml")

        s1 = soup1.find_all('h2', {'class':'index-module_articleTitle_28fPT'})
        #标题
        print("111111111",s1)

        timediv = str(soup1.find_all('meta', {'itemprop': 'dateUpdate'}))
        rtime = re.compile(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
        s2 = rtime.findall(timediv)
        print("2222222222",s2)
        s3 = soup1.find_all('span', class_='bjh-p')
        #内容
        print("44444444", s3)

        title = s1[0].get_text().strip()
        date = s2[0].get_text().strip()

        for t3 in s3:
            para = t3.get_text().strip()  # 获取文本后剔除两侧空格
            content = para.replace('\n', '')  # 剔除段落前后的换行符
            clist.append(content)
        content = ''.join('%s' % c for c in clist)
        ws.append([title, date,  content])
        print([title, date])

    except Exception as e:
        print("错误: ", e)
    finally:
        wb.save('XXX.xlsx')  # 保存已爬取的数据到excel
        print(u'OK!\n\n')

if __name__ == '__main__':

    raw_url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=老龄智能&medium=2&x_bfe_rqs=20001&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn='
    wb = workbook.Workbook()  # 创建Excel对象
    ws = wb.active  # 获取当前正在操作的表对象
    # 往表中写入标题行,以列表形式写入！
    ws.append(['title', 'dt', 'source', 'content'])

    # 通过循环完成url翻页
    for i in range(3):
        link = raw_url + str(i * 10)
        get_connect(link)
        print('page', i + 1)
        # time.sleep(5)

    wb.save('996.xlsx')
    print('finished')
    wb.close()
