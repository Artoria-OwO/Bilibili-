#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import time
import json

filename = 'bilibili_fans.txt'
i = 0
header = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}



def get_up_fans(uid):
	url='https://api.bilibili.com/x/web-interface/card?mid=%d&jsonp=jsonp' % uid
	r=requests.get(url,headers=header)
	r.encoding='utf-8'
	json_response=r.content.decode()
	dict_json=json.loads(json_response)
	dict1=dict_json.get("data",{})
	follower=dict1.get("follower")
	name=(dict1.get("card",{})).get("name")
	_id=(dict1.get("card",{})).get("mid")
	time.sleep(2)
	if(follower<10000):
		return
	print(_id,name,follower)
	with open(filename,'a+') as f:
		f.write(str('uid:')+"\t"+str(_id)+"\t"+str(name)+"\t"+str(follower)+"\n")
		f.close()
	get_up_attentions(uid)

def get_up_attentions(uid):
	url='https://api.bilibili.com/x/web-interface/card?mid=%d&jsonp=jsonp' % uid
	r=requests.get(url,headers=header)
	r.encoding='utf-8'
	json_response=r.content.decode()
	dict_json=json.loads(json_response)
	dict1=dict_json.get("data",{})
	attentions=(dict1.get("card",{})).get("attentions")
	time.sleep(2)
	for attention in attentions:
		get_up_fans(attention)


while i<100000000 :
	get_up_fans(i)
	i = i + 1

