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
def get_connect(name):
    img_list=[]
    url_list = []
    pagenum=1
    tot=3
    tnum=0
    while True:
        try:
            kv={
                'wd':name,
                'medium':(2),
                'x_bfe_rqs':20001,
                'x_bfe_tjscore':0.000000,
                'tngroupname':'organic_news',
                'newVideo':str(12),
                'rsv_dl':'news_b_pn',
                'pn':str(pagenum*10)
            }
            r = requests.get('https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&', headers=headers, params=kv, timeout=10)

            if 200 != r.status_code:
                return None
            soup = BeautifulSoup(r.text, "lxml")
            div_list = soup.find_all('div', class_='result-op c-container xpath-log new-pmd')
            for div in div_list:
                mu = div['mu'].strip()
                url_list.append(mu)  #添加链接
                tnum=tnum+1
            for img_div in soup.find_all('div', class_='result-op c-container xpath-log new-pmd'):
                oringe_links = img_div.find('img')
                links = oringe_links.get('src')
                img_list.append(links)
                tnum = tnum + 1
            pagenum=pagenum+1
            if pagenum > tot:
                break
        except Exception as e:
            print('e.message:\t', e)
        finally:
            print(u'go ahead!\n\n')
    print(tnum)
    print(pagenum,tot)
    return get_content(url_list)
def get_content(url_list):
    print(url_list)
    try:
        for url in url_list:
            clist = []  # 空列表存储文章内容
            r1 = requests.get(url, headers=headers1, timeout=10)
            soup1 = BeautifulSoup(r1.text, "lxml")
            s1 = soup1.select('.article-title > h2:nth-child(1)')
            s2 = soup1.select('.date')
            s3 = soup1.select('.author-name > a:nth-child(1)')
            s4 = soup1.find_all('span', class_='bjh-p')

            title = s1[0].get_text().strip()
            date = s2[0].get_text().strip()
            source = s3[0].get_text().strip()
            for t4 in s4:
                para = t4.get_text().strip()  # 获取文本后剔除两侧空格
                content = para.replace('\n', '')  # 剔除段落前后的换行符
                clist.append(content)
            content = ''.join('%s' % c for c in clist)
            ws.append([title, date, source, content])
            print([title, date])
        wb.save('XXX.xlsx')

    except Exception as e:
        print("Error: ", e)
    finally:
        wb.save('XXX.xlsx')  # 保存已爬取的数据到excel
        print(u'OK!\n\n')
if __name__ == '__main__':
    wb = workbook.Workbook()  # 创建Excel对象
    ws = wb.active  # 获取当前正在操作的表对象
    # 往表中写入标题行,以列表形式写入！
    ws.append(['title', 'dt', 'source', 'content'])
    a=get_connect('故宫博物馆')
    print(a)
    wb.save('XXX.xlsx')
    print('finished')
    wb.close()