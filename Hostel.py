import urllib.request
import csv
import os
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/60.0.3112.113 Safari/537.36'}

# get html of a speficif websity by url
def url_request(url):
    try:
        req = urllib.request.Request(url=url, headers=headers)
        content = res = urllib.request.urlopen(req).read()
        content = content.decode()
        return content
    except:
        print('invalid url: ' + url)
        return ''

# take the url of a specific hostel and print all the reviews of the hostel
def get_review(url):
    beginning_url = url + '/reviews?showOlderReviews=1&page=2#reviewFilters'
    content = url_request(beginning_url)
    # get the total number of pages
    review_page = ''
    if '<li class="arrow-last"><a href=' in content:
        last_page =  content[content.find('<li class="arrow-last"><a href='):]
        last_page = last_page[last_page.find('page=') + 5:]
        while last_page[0].isdigit():
            review_page += last_page[0]
            last_page = last_page[1:]
    else:
        review_page = '1'
    # go to each review page, and get the review detail
    review_page = int(review_page)
    review = []
    for i in range(review_page):
        page_num = i + 1
        page_url = url + '/reviews?showOlderReviews=1&page=' + str(page_num) + '#reviewFilters'
        content = url_request(page_url)
        # take the review pages' html, print the review detail
        review += get_detail(content)
    return review

# take the review pages' html, print the review detail
def get_detail(content):
    # find the place of useful information
    begin = content.find('<div class="reviewlisting clearfix">') + 5
    end = content.find('<div class="pagination-centered clearfix small-12-columns">')
    # make content a list of pieces of review
    content = content[begin:end].split('<div class="reviewlisting clearfix">')
    # in each piece of review, get the nationality, gender, textrating, ratings for individual items, and textreview
    returnReview = []
    for i in content:
        i = i[i.find('<li class="reviewerdetails">') + 28:]
        # avoid error
        try:
            country, gender, age = i[:i.find('</li>')].replace(' ','').split(',')
            i = i[i.find('"textrating'):]
            text_rating = i[i.find('">') + 2:i.find('</div>')]
            i = i[i.find('"reviewtext translate"'):]
            review_text = i[i.find('<p>') + 3:i.find('</p>')].replace('\r',' ').replace('\n', ' ').replace('&#039;', "'").lower().replace('&quot;', '"')
            rating = []
            num = 0
            while '<span>' in i and num < 7:
                rating.append(i[i.find('<span>') + 6:i.find('</span>')])
                i = i[i.find('</span>') + 2:]
                num += 1
            review = [country[1:], gender, age, text_rating] + rating + [review_text]
            print(review)
            returnReview.append(review)
        except:
            continue
    return returnReview

# get a list of hostel website from HostelWorld
def get_list(url):
    menu = []
    req = urllib.request.Request(url= url, headers=headers)
    content = urllib.request.urlopen(req).read()
    content = content.decode()
    content = content[content.find('"@type": "ItemList"') + 9:]
    content = content[:content.find('</script>')]
    hostel_list = []
    while("url" in content):
        content = content[content.find('https://www.hostelworld.com/hosteldetails.php'):]
        hostel_list.append(content[:content.find('"')])
        content = content[2:]
    return hostel_list

# this function will generation a csv file according to the name and review data provided
def export_csv(name, review):
    if os.path.exists(name + '.csv'):
        os.remove(name + '.csv')
    with open(name + '.csv', 'w', encoding='utf-8', newline='\n') as csvfile:
        fieldnames = ['nationality', 'gender', 'age', 'overall rating', 'value for money rating', 'security rating', 'location rating', 'facilities rating', 'staff rating', 'atmosphere rating', 'cleanliness rating', 'text review']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in review:
            writer.writerow({'nationality': i[0], 'gender': i[1], 'age' :i[2], 'overall rating':i[3], 'value for money rating':i[4], 'security rating':i[5], 'location rating':i[6], 'facilities rating':i[7], 'staff rating':i[8], 'atmosphere rating':i[9], 'cleanliness rating':i[10], 'text review':i[11]})


# enter a city name, and the program will print all the reviews of the hostels in that city
def city_based_search():
    city = input('Enter city: ').replace(' ', '-')
    url = 'https://www.hostelworld.com/findabed.php/ChosenCity.' + city +'/ChosenCountry.USA'
    hostel_list = get_list(url)
    print(hostel_list)
    review = []
    for i in hostel_list:
        review += get_review(i)
    print('exporting csv file...')
    export_csv(city, review)
    print('complete!')

# you need to go to HostelWorld to find the specific hostel website
# this function will prompt you to enter that website, and will print out all the reviews of that hostels
def hostel_based_search():
    url = input('Copy HostelWorld website: ').replace(' ','')
    hostel_name = input('Hostel Name: ')
    review = get_review(url)
    print('exporting csv file...')
    export_csv(hostel_name, review)
    print('complete!')


# instruction:
#   for city based search, you only need to put a city's name, not case sensitive
#       example: austin
#   for hostel based search, you need to go to HestelWorld and find the website of the hostel you are interested
#       and enter the website after prompt (you can press space key after the website if you are having trouble)
#       website example: https://www.hostelworld.com/hosteldetails.php/Hostel-Fish/Denver/98583
#   the program will generate a csv file in the root folder, the name will be cityname.csv or hostelname.csv

#city_based_search()
hostel_based_search()

# result example from the Anderson Estates in Los Angeles:
# ['NewZealand', 'Male', '18-24', '9.1'         , '10.0'                , '8.0'          , '8.0'          , '10.0'           , '10.0'      , '8.0'            , '10.0'            , 'the anderson estates provides value for money. for $25 per night i was able to get a free breakfast, free lunch, and access to an outdoor pool. the staff are friendly and nice and the place is tidy.']
# [Nationality , gender,   age  , overall rating, value for money rating, security rating, location rating, facilities rating, staff rating, atmosphere rating, cleanliness rating, text review]
