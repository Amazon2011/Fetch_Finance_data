from bs4 import BeautifulSoup 
doc = ['<html><head><title>Page title</title></head>',
       '<body><p id="firstpara" align="center">This is paragraph <b>one</b>.',
	   '<tr class="dbrow"><td class="td_label">中文简称</td><td class="td_width160">浦发银行</td><td class="td_label keep_line">办公地址</td><td class="td_width160">上海市中山东一路12号</td></tr>'
       '<p id="secondpara" align="blah">This is paragraph <b>two</b>.',
       '</html>']
soup = BeautifulSoup(''.join(doc))

head = soup.find('head')
title = head.find('title')

print(title.name)