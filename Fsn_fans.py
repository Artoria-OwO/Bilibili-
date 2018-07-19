#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import requests
from bs4 import BeautifulSoup
 
 
def get_data():
	end_num = get_end_page()
	for num in range(1, end_num+1):
		url = 'https://search.bilibili.com/api/search?search_type=all&keyword=Fate/stay night&page=%d' % num
		data_s = get_page_url(url)
		print('第%d页' % num)
		for key, value in data_s.items():
			get_up_data(value)
		print()
 
 
def get_end_page():
	# 返回搜索页的最大页数
	url = 'https://search.bilibili.com/api/search?search_type=all&keyword=Fate/stay night'
	header = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
	
	response = requests.get(url, headers=header)
	response.encoding = 'utf-8'
	html = response.json()
	end_num = html['numPages']
	time.sleep(2)
	return int(end_num)
 
 
def get_page_url(url='https://search.bilibili.com/api/search?search_type=all&keyword=Fate/stay night&page=1'):
	# 以字典形式返回当前搜索页的视频标题与视频网址
	header = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
	page_data = {}
	
	response = requests.get(url, headers=header)
	response.encoding = 'utf-8'
	html = response.json()
	data_s = html['result']['video']
	for data in data_s:
		page_data[data['title']] = data['arcurl']
	time.sleep(2)
	return page_data
 
 
def get_up_data(url=''):
	# 获取视频页面的up部分信息
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
	
	response = requests.get(url, headers=header)
	response.encoding = 'utf-8'
	html = response.text
	soup = BeautifulSoup(html, "html.parser")
	up_name = soup.find('a', class_='name').string
	up_url = 'https:' + soup.find('a', class_='name')['href']
	up_code = str(soup.find('a', class_='name')['href']).split('/')[-1]
	up_data_url = 'https://api.bilibili.com/x/web-interface/card?mid=%s&jsonp=jsonp' % up_code
	# print(up_data_url)
	response = requests.get(up_data_url, headers=header)
	response.encoding = 'utf-8'
	html = response.json()
	up_fans = html['data']['card']['fans']
	up_contribute = html['data']['archive_count']
	print('up主"%s" \t 投稿数:%s \t 粉丝数:%s \t 空间地址:%s' % (up_name, up_contribute, up_fans, up_url))
	filename='FSN_fans.txt'
	with open(filename,'a+') as f:
		f.write(str(up_name)+"\t"+str(up_contribute)+"\t"+str(up_fans)+"\n")
		f.close()
		
 
get_data()

# get_end_page()
# get_page_url()
# url = 'http://www.bilibili.com/video/av20140552?from=search&seid=3219209606912113739'
# get_up_data(url)
 
'''
视频里的一些信息
https://api.bilibili.com/x/web-interface/card?mid=170759885&jsonp=jsonp
'''
'''
https://search.bilibili.com/all?keyword=Fate/stay night&page=1
'''
'''
搜索页面
https://search.bilibili.com/api/search?search_type=all&keyword=Fate/stay night&from_source=banner_search
粉丝数API
http://api.bilibili.com/x/relation/stat?vmid=3646740&jsonp=jsonp&callback=__jp3
'''
