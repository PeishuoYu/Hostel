Why I developed this program:
	Recently I am doing a marketing research about hostel in Denver, and I need the
	data to find out what customer care about.

	After getting the data, I wanted to categorize the words in review, and make
	these words dummy variables. Then I hoped to apply the machine learning program
	to make a model. Finally, by looking at the model, I will be able to tell which
	group of customers care what. However, my program told me that the preferences
	of different groups were very similar, which means my plan did not work. Still
	a good try though :-)

In this folder, there are:
	Hostel.py	A webcrawler that gets the review data from HostelWorld website
	denver.csv	The review data for all the hostels in Denver
	los-angeles.csv	The review data for all the hostels in Los Angeles (for demonstration)
	The Anderson 	The review data for Anderson Estates Hostel (for demonstration)
	Estates.csv
	GeneralModel	The machine learning program that is used to build model to
	Builder.py	find out what different traveling groups care about
	TextToDummy.py	A program that categorizes the words in reviews, turns
			these words into dummy variables, and stores them in a csv file
	model.txt	A model generated my the machine learning program

Major Update 02/15/2018:
	Added function to automatically generate csv file to store the data collected
	Added two examples (one for city search, one for hostel search) in the root folder

Update 02/23/2018:
	Add TextToDummy.py and GeneralModelBuilder.py