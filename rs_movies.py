# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import requests
from bs4 import BeautifulSoup
import xlwt

def Login():
    login_url = 'http://rs.xidian.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
    loginpage = urllib.urlopen('http://rs.xidian.edu.cn/member.php?mod=logging&action=login').read()
    login_soup = BeautifulSoup(loginpage)
    formhash_tag = login_soup.find('input',attrs={'name':'formhash'})
    formhash = formhash_tag['value']
    book = xlwt.Workbook(encoding = 'utf-8',style_compression=0)
    sheet = book.add_sheet('movie',cell_overwrite_ok = True)
    sheet.write(0,0,'movie')
    sheet.write(0,1,'rating-num')
    #print formhash
    params = {
            "answer":"",
            #"formhash":formhash,
            #"loginfield":"username",
            #"loginsubmit":"",
            "password":'password',
            "questionid":"0",
            "referer":"http://rs.xidian.edu.cn/",
            "username":'username',
            }
    jar = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(jar)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    req = urllib2.Request(login_url)
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Connection','keep-alive')
    req.add_header('User-Agent',"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0")
    req.add_header('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')
    #req.add_header('Accept-Encoding','gzip, deflate')
    #req.add_header('Referer',"http://rs.xidian.edu.cn/forum.php")
    enparams = urllib.urlencode(params)
    page = urllib2.urlopen(req,enparams)
    #print page
    data = page.read()
    #print data
    global g_cookie
    global g_formhash
    g_cookie = page.info()['set-cookie']
    t_cookie = re.sub(r'poK_formhash=deleted','',g_cookie)
    r_formhash = re.search(r"poK_formhash=[^;]+",t_cookie)
    #if r_formhash:
        #g_formhash = re.sub(r'poK_formhash=','',r_formhash.group())
    #return
    for num in range(1,6):
        murl = 'http://rs.xidian.edu.cn/bt.php?mod=browse&c=10&page='+str(num)
        treq = urllib2.Request(murl)
        treq.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        treq.add_header('Connection','keep-alive')
        treq.add_header('User-Agent',"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0")
        treq.add_header('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')    
        tpage = urllib2.urlopen(treq,enparams)
        #print tpage
        tdata = tpage.read().decode('utf-8')
        #print tdata
        movie = r'mod=viewthread&amp;tid=[_0-9_]{0,10}">(.*?)</a>'
        mlist = re.findall(movie,tdata)
        i = 1+10*(num-1)
        for each in mlist:
            a = each.split("[")[3].split(']')[0].split('/')[0]
            b = each.split("[")[4].split(']')[0].split('/')[0]
            #必须夸一下自己！太机智了！Awesome！
            if a.isdigit():
                #print b
                c = b
            else:
                #print a
                c = a
            print c,
            sheet.write(i,0,c)
            try:
                dburl = 'http://www.douban.com/search?q='+c
                s = requests.session()
                h = s.get(dburl)
                html = h.content.decode('utf-8')
                #print html
                soup = BeautifulSoup(html)
                votes = soup.select('.rating_nums')
                print votes[0].get_text()
                sheet.write(i,1,votes[0].get_text())
            except:
                print '未获取到评分'
                sheet.write(i,1,'未获取到评分')
            i = i+1
    book.save(r'd:\movie5.xls')

'''
def ReplyPost(url,params):
    req = urllib2.Request(url)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    req.add_header('User-Agent',user_agent)
    enparams = urllib.urlencode(params)
    page = urllib2.urlopen(req,enparams)
'''

Login()
