from __future__ import print_function
from bs4 import BeautifulSoup
from urllib import urlopen
import pandas as pd
import multiprocessing

def grab_data(url):
	try:
		html_doc = urlopen(url).read()
			# connection might break and we need to restart, 
			# need to come up with a way to support broken connection and continue from what we left behind
		soup = BeautifulSoup(html_doc, "html.parser")
	
		title_num = soup.find("head").find("title").get_text().replace("Problem - ","").replace(" - Codeforces", "")
		
		if title_num == "Codeforces":
			return
		print (title_num)
		ps = soup.find('div', class_= "problem-statement")

		title = ps.find('div',class_= 'title').get_text()

		time_limit = (ps.find('div', class_ = 'time-limit').get_text().split("test",1)[1]).split()[0]

		memory_limit = (ps.find('div', class_ = 'memory-limit').get_text().split("test",1)[1]).split()[0]

		word  = ps.find('div', class_="").get_text()+"\n"

		input_spec = ps.find('div', class_ = "input-specification").get_text().split("Input",1)[1]
		output_spec = ps.find('div', class_ = "output-specification").get_text().split("Output",1)[1]

		label = []
		tags = soup.find('div', id="sidebar").find_all('span', class_="tag-box")
		for k  in tags:
			label.append(k.get_text().replace("\r\n", "").encode("utf-8").replace(" ",""))


		title = title.split(" ",1)[1]
		labels = ', '.join(label)
		print(labels)
		entry = {"title-num" :title_num, "title": title, "time-limit": time_limit, "memory-limit": memory_limit,
		"word":word, "input-spec": input_spec, "output-spec": output_spec, "labels": labels}
			
		
		dff = pd.DataFrame.from_dict(entry, orient='index')
		return dff
	except AttributeError:
		print("error occured")
		return

problems = map(chr, range(65,80))
ID = list(range(1,910))

headers = ['title-num', 'title', 'time-limit','memory-limit', 'problem-statement', 'input-spec','output-spec', 'labels']
df = pd.DataFrame(columns=headers)
url = []

for i in ID:
 for j in problems:
  url.append("http://codeforces.com/problemset/problem/"+str(i)+"/"+j)

pool = multiprocessing.Pool()
dfs = pool.map(grab_data,url)

for  i in dfs:
	df.append(i)

df.to_csv("data.csv")




