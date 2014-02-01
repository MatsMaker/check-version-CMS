import sys
import urllib.request
import urllib.parse
import json
import os, sys
import fnmatch, re
import glob
import smtplib

class CvMain():
	#options
	mainDir = 'E:\worck\cvSMC\test\\'
	#max 9
	investments = 3

	def send_mail(self, txtparam):
		print("Send a report by email...")
		fromaddr = 'Yandex email'
		toaddr = 'mail where to send the report'
		subj = 'Notification from system'
		msg_txt = 'Notice:\n\n ' +  txtparam + '\n\nBye!' #
		msg = "From: %s\nTo: %s\nSubject: %s\n\n%s"  % ( fromaddr, toaddr, subj, msg_txt)
		username = 'mats-aerozol'
		password = 'your password'
		server = smtplib.SMTP('smtp.yandex.ru:587')
		server.set_debuglevel(1);
		server.starttls()
		server.login(username,password)
		server.sendmail(fromaddr, toaddr, msg)
		server.quit()
		print("Done.")

class Cvwp(CvMain):
	updateUrl = "http://api.wordpress.org/core/version-check/1.7/"

	def wp_get_currenst_version(self):
		response = urllib.request.urlopen(self.updateUrl)
		json = response.read().decode("utf-8")
		checVersion = json.loads(json)
		return(checVersion['offers'][0]["current"])

	def find_files(self, filename):
		print("Find files CMS...")
		listFiles = [];
		investmentsDir = "*\\"
		i=0

		while  self.investments > i:
			investmentsDir = investmentsDir + investmentsDir
			listFilesDir = glob.glob(self.mainDir+investmentsDir+filename+'.php')
			i +=1
			if (listFilesDir.__len__() > 0):
				listFiles += listFilesDir
		return listFiles

	def get_file_version(self, file):
		file = open(file, 'r')
		contentFile = file.read()
		version = re.findall('\$wp_version\s*=\s*([^;]*)', contentFile)
		file.close()
		version = version[0].replace("'","")
		return version

	def check_file_version(self, listFiles):
		print("Build a list of non-valid sites...")
		curent_version_wp = self.wp_get_currenst_version();
		print("Curent version CMS: " + curent_version_wp)
		viewString = ""
		i=0
		while f.__len__()>i:
			if (self.get_file_version(f[i]) != curent_version_wp):
				print(self.get_file_version(f[i])+"  "+ curent_version_wp)
				viewString = viewString + "\n" + listFiles[i].replace(self.mainDir, "") +" --> "+self.get_file_version(f[i])
			i+=1
		print("Done.")
		return viewString

class CvJM(CvMain):
	updateUrl = "http://update.joomla.org/core/list.xml"

	def wp_get_currenst_version(self):
		response = urllib.request.urlopen(self.updateUrl)
		xmldoc = response.read().decode("utf-8")
		print(xmldoc)
		


#
#	controller
#
# cvwp = Cvwp()

# f = cvwp.find_files("/wp-includes/version")
# print(f)
# novalide = cvwp.check_file_version(f)
# print(novalide)
# cvwp.send_mail(novalide)

cvjm = CvJM()

cvjm.wp_get_currenst_version();