Why I developed this program:
	Recently I am doing a marketing research about hostel in Denver, and I need the
	data to find out what customer care about.

	In this project, I conducted a word frequency analysis in hope to find out whether
	different groups of people care about different things about a hostel. If the 
	answer is yes, I can further tailor different messages delivered to different 
	groups of people via Facebook ads. However, after gathering and processing data,
	I found that all groups caring about very similar attributes of a hostel.

In this folder, there are:
	Hostel.py	A webcrawler that gets the review data from HostelWorld website
	denver.csv	The review data for all the hostels in Denver
	los-angeles.csv	The review data for all the hostels in Los Angeles (for demonstration)
	The Anderson 	The review data for Anderson Estates Hostel (for demonstration)
	Estates.csv
	TextToDummy.py	A program that categorizes the words in reviews, turns
			these words into dummy variables, and stores them in a csv file

Major Update 02/15/2018:
	Added function to automatically generate csv file to store the data collected
	Added two examples (one for city search, one for hostel search) in the root folder

Update 02/23/2018:
	Add TextToDummy.py and GeneralModelBuilder.py