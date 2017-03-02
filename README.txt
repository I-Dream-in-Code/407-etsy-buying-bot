REQUIREMNENTS:
	Python2
	pip
	java
	selenium(installed via pip)
	.txt with login info and store URL
INSTALL PYTHON2:
	run PYTHON-2.7.10.AMD4.MSI
	!!!!!!!!!!!IMPORTANT!!!!!!!!!!!!
	BE SURE TO CHECK THE BOX TO ADD TO SYSTEM FILE PATH

INSTALL SELENIUM:
	pip install selenium

TEXT FILE FORMAT(seperate by new line):
	username
	password
	store URL

RUNNING ETSY.PY:
	java -jar selenium-server-standalone-2.48.2.jar
	python etsy.py [text file] [integer]
	[integer] is number of required purchases needed for script to end

