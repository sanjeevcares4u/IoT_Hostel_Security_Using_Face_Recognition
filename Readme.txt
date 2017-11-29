1. install raspnien os (eg:- raspbien jessie)   for help visit raspberry website or youtube.

2. connect via HDMI to monitor.
		OR
	download MOBAXTERM and vnc viewer on windows  to connect via laptop
	a.  right click on network icon on taskbar
	b.  click on open network and sharing center
	c.  click on achange adapter setting present on the lft tab bar.
	d.  now right click on wifi and and then click on properties.
	e.  click on sharing tab and enable both option click apply then ok.

	f.  open MobaXTrem and click on session icon
	g.  under session click SSH and and in remote host text box enter raspberrypi.mshome.net  and click ok.
	h.  now on tab present on left side of the screen our ssh opetion appers . click on  it.
	i.  Now out terminal appers asking for   login id:  
				login id: pi
				password: raspberry
	j.  our pi terminal appears. 
	k.  For getting the UI interface enter vncserver in terminal. it will give us a ipaddress. copy It. open VNCVIEWER paste the ip address and it's done.
	l.  For help visit youtube.

3. Installing Opencv and it's contrib package Please visit : https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html   . and follow all the steps correctly.
Note:- It will take some time to complete

4. copy project folder to any location.


Note :

  # ### Training Data

  # The more images used in training the better. Normally a lot of images are used for training a face recognizer so that it can learn different looks of the same person, for example with glasses, without glasses, laughing, sad, happy, crying, with beard, without beard etc. To keep our tutorial simple we are going to use only 12 images for each person. 
  # 
  # So our training data consists of total 2 persons with 12 images of each person. All training data is inside _`training-data`_ folder. _`training-data`_ folder contains one folder for each person and **each folder is named with format `sLabel (e.g. s1, s2)` where label is actually the integer label assigned to that person**. For example folder named s1 means that this folder contains images for person 1. The directory structure tree for training data is as follows:
  # 
  # ```
  # training-data
  # |-------------- s1
  # |               |-- 1.jpg
  # |               |-- ...
  # |               |-- 12.jpg
  # |-------------- s2
  # |               |-- 1.jpg
  # |               |-- ...
  # |               |-- 12.jpg
  # ```
  # 
  # The _`test-data`_ folder contains images that we will use to test our face recognizer after it has been successfully trained.

  # As OpenCV face recognizer accepts labels as integers so we need to define a mapping between integer labels and persons actual names so below I am defining a mapping of persons integer labels and their respective names. 
  # 
  # **Note:** As we have not assigned `label 0` to any person so **the mapping for label 0 is empty**. 

  # In[2]:

  #there is no label 0 in our training data so subject name for index/label 0 is empty      


5. For connecting buzzer sensor i have included a photograph how to connect. Note:- connect when pi is off 

6. As our program needs data for the training purpose. I have included a script for clicking image. Face_detect.py . It will click the image when a face is detected.
	Try to click more number of photo with differnt emotions,  angle and also from differnt situations.
	Rename the image in serial number from 1 to n. Copy the image and paste in any blank directory inside the training-data directory.

7. Run the program



for query contact :- sanjeev.sps.2009@gmail.com  , sanjeev1@live.in
