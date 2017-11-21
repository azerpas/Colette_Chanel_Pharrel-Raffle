import requests, json, time, random, datetime, threading, pickle, os
from termcolor import colored

sitekey = "6LdMmTkUAAAAABXe8KxK5NkZoXcwa1OCPx5XfRVf"


def log(event):
	d = datetime.datetime.now().strftime("%H:%M:%S")
	print("PW x CHANEL by Azerpas :: " + str(d) + " :: " + event)

def notify(title, subtitle, message, sound):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    so = '-sound {!r}'.format(sound) 
    os.system('terminal-notifier {}'.format(' '.join([m, t, s, so])))
		
class Raffle(object):
	def __init__(self):
		self.s = requests.session()
		self.shoes = [{"shoe_id":"1","shoe_name":"COLETTE x CHANEL x PHARREL WILLIAMS"}]
		self.url = "http://www.chanelatcolette.fr/en/mail-register"

	def register(self,identity,proxy):
			# register to each shoes.
			for dshoes in self.shoes:
				print('------------------------')
				print("Signin: "+identity['mail'])
				print("for: " + dshoes['shoe_name'])
				print('------------------------')

				d = datetime.datetime.now().strftime('%H:%M')
				log("Getting Captcha")
				flag = False
				while flag != True:
					d = datetime.datetime.now().strftime('%H:%M')
					try:
						file = open(str(d)+'.txt','r') #r as reading only
						flag = True
					except IOError:
						time.sleep(2)
						log("No captcha generated for this minute")
						flag = False
				flag2 = False
				while flag2 != True:
					try:
						d = datetime.datetime.now().strftime('%H:%M')
						file = open(str(d)+'.txt','r')
						FileList = pickle.load(file) #FileList the list where i want to pick out the captcharep
						flag2 = True
					except Exception as e:
						#log("Can't open file")
						#print(e)
						time.sleep(0.2)
				while len(FileList) == 0: #if len(FileList) it will wait for captcha scraper 
						d = datetime.datetime.now().strftime('%H:%M')
						try:
							file = open(str(d)+'.txt','r')
							print('debug 2')
							FileList = pickle.load(file)
							if FileList == []:
								log("No captcha available(2)")
								time.sleep(3)
						except IOError as e:
							log("No file, waiting...")
							print(e)
							time.sleep(3)
				captchaREP = random.choice(FileList) 
				FileList.remove(captchaREP)
				file  = open(str(d)+'.txt','w')
				pickle.dump(FileList,file)
				log("Captcha retrieved")

				headers = {
					"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
					"Accept-encoding":"gzip, deflate",
					"Accept-language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
					"Cache-Control":"max-age=0",
					"Connection":"keep-alive",
					"Content-length":"625",
					"Content-type":"application/x-www-form-urlencoded",
					"Host":"www.chanelatcolette.fr",
					"Origin":"http://www.chanelatcolette.fr",
					"Referer":"http://www.chanelatcolette.fr/fr/limited-edition",
					"Upgrade-Insecure-Requests":"1",
					"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
				}

				##################
				dates = identity['birthdate'].split('/')
				day = dates[0]
				month = dates[1]
				year = dates[2]

				print(str(day+month+year))

				if identity['shoesize'] == "":
					identity['shoesize'] = random.choice(['3.5','4','4.5','5','5.5','6','7','7.5','8','9','9.5','10.5'])
					log("Changed size to: " + identity['shoesize'])
				#################


				payload = {"firstname":identity['fname'],
							"lastname":identity['lname'],
							"email":identity['mail'],
							"phone":identity['phone'],
							"birthday":day,
							"birthmonth":month,
							"birthyear":year,
							"shoessize":identity['shoesize'],
							"g-recaptcha-response":captchaREP,
							"check":"1",
							"locale":"fr",
					}


				req = self.s.post(self.url,headers=headers,data=payload,proxies=proxy)
				print(req)
				jsonn = json.loads(req.text)
				if req.status_code == 200:
					if jsonn['result'] == "ok":
						print(colored('Successfully entered','red', attrs=['bold']))
				if req.status_code == 400:
					raise ValueError('ERROR 400')
				sleep = random.uniform(2.3,2.9)
				log("Sleeping: " + str(sleep) + " seconds")
				time.sleep(sleep)
				self.s.cookies.clear()

if __name__ == "__main__":
	ra = Raffle()
	accounts = [
		# FORMAT SIZE 8 or 8.5 ETC
]
	# catpcha 
	proxies = [
	]
	errors = []
	index = 0
	regis = 0
	for i in accounts:
		print("\n\n-------------------------")
		print('NEW TASK')
		print("-------------------------\n")

		p = random.choice(proxies)
		proxies.remove(p)
		if '@' in p:
			proxy = { 'https' : 'https://{}'.format(p) }
			log('Using proxy:')
			print(colored(proxy,'red', attrs=['bold']))
		else:
			proxy = {'http':p,
					'https':p}
			log('Using proxy:')
			print(colored(proxy['https'],'red', attrs=['bold']))
		try:
			ra.register(i,proxy)
			regis += 1
		except Exception as e:
			print(e)
			if e == "local variable 'FileList' referenced before assignment":
				try:
					ra.register(i,proxy)
				except:
					pass
			errors.append(i)
	print(errors)
	print("-------------------------")
	print("-------------------------")
	print("-------------------------")
	print(accounts)
	print("Nb of accounts registered: " + str(regis))
