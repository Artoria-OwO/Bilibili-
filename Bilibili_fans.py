#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import time
import json

filename = 'bilibili_fans.txt'
i = 1
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False
header = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
uid_list =[]


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
	if uid not in uid_list:
		uid_list.append(uid)
	time.sleep(1)
	if(follower<100000):
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
	time.sleep(1)
	for attention in attentions:
		_url='https://api.bilibili.com/x/web-interface/card?mid=%d&jsonp=jsonp' % attention
		_r=requests.get(_url,headers=header)
		_r.encoding='utf-8'
		_json_response=_r.content.decode()
		_dict_json=json.loads(_json_response)
		_dict1=_dict_json.get("data",{})
		_attentions=(_dict1.get("card",{})).get("attentions")
		time.sleep(1)
		if uid not in _attentions:
			if attention not in uid_list:
				get_up_fans(attention)



while i<100000000 :
	get_up_fans(i)
	i = i + 1
