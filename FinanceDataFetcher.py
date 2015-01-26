# This program is used to fetch Chinese listed companies data from quotes.money.163.companies
# @Author: Yongtao Chen
# @Date: 2015-01-21

from bs4 import BeautifulSoup
import re, urllib.request
import csv

class GetStockDataUtils:
	def __init__(self):
		pass
		
	@staticmethod
	def getDataMap(stockCode, requiredData):
		# 公司资料URL
		url1 = 'http://quotes.money.163.com/f10/gszl_' + stockCode + '.html#01f01'
		try:
			req1 = urllib.request.urlopen(url1)
		except:
			return None
		soup = BeautifulSoup(req1.read())
		
		if (GetStockDataUtils.judge404(soup) or GetStockDataUtils.judgeStockClosed(soup)):
			return None
		
		allDataDictionary = {}
		allDataDictionary['股票代码'] = stockCode
		#获取股票名称
		name = soup.find('h1',class_='name').contents[1].contents[0]
		allDataDictionary["股票名称"] = name
		
		fields1 = soup.findAll('td',class_='td_label')
		for field in fields1:
			allDataDictionary[field.contents[0]] = '' if len(field.nextSibling.nextSibling.contents) == 0 else field.nextSibling.nextSibling.contents[0]

		fields2 = soup.findAll('td',class_='td_label keep_line')
		for field in fields2:
			allDataDictionary[field.contents[0]] = '' if len(field.nextSibling.nextSibling.contents) == 0 else field.nextSibling.nextSibling.contents[0]
		
		#行业对比URL
		url2 = 'http://quotes.money.163.com/f10/hydb_' + stockCode + '.html#01g01'
		try:
			req2 = urllib.request.urlopen(url2)
		except:
			return None
		soup = BeautifulSoup(req2.read())
		
		if (GetStockDataUtils.judge404(soup)):
			return None
		#获取所属行业
		allDataDictionary["所属行业"] = soup.find('div',class_='inner_box industry_info').find('a').contents[0]
		
		requiredDataDictionary = {}
		for requiredField in requiredData:
			requiredDataDictionary[requiredField] = allDataDictionary[requiredField]
		
		return requiredDataDictionary
	
	@staticmethod
	def judge404(soup):
		h2Field = soup.find('h2')
		if (h2Field != None ):
			if (h2Field.contents[0] == '对不起!您所访问的页面不存在或者已删除。'):
				return True
		return False
	
	@staticmethod
	def judgeStockClosed(soup):
		stockClosedField = soup.find('span',class_='sotck_closed')
		if (stockClosedField != None):
			stockClosed = stockClosedField.contents[0]
			if (stockClosed == '已退市'):
				return True
		return False
	
	@staticmethod
	def writeDataDictionary(writer, stockCode, requiredData):
		print(stockCode)
		requiredDataDictionary = GetStockDataUtils.getDataMap(stockCode, requiredData)
		if (requiredDataDictionary != None):
			sortedRequiredData = []
			for dataField in requiredData:
				sortedRequiredData.append(requiredDataDictionary[dataField])
			writer.writerow(sortedRequiredData)
		
if __name__ == '__main__':
	requiredData = ['股票代码', '股票名称', '组织形式', '公司全称', '英文名称', '所属行业', '注册资本', '董事长', '地域', '办公地址', '公司网址', '董事会秘书', '董秘电话', '董秘邮箱', '成立日期', '上市日期', '募资资金总额', '发行价格', '发行市盈率']
	
	with open('D:/Study/Fetch_Finance_data/data.csv', 'w', newline='\n') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(requiredData)
		
		#主板
		for i in range(600000, 602500):
			stockCode = str(i)
			GetStockDataUtils.writeDataDictionary(writer, stockCode, requiredData)
		#中小板
		for i in range(1,3000):
			stockCode = '{0:06}'.format(i)
			GetStockDataUtils.writeDataDictionary(writer, stockCode, requiredData)
		
		#创业板
		for i in range(300000, 301000):
			stockCode = str(i)
			GetStockDataUtils.writeDataDictionary(writer, stockCode, requiredData)