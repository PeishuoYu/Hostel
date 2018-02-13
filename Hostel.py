import urllib.request
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
    for i in range(review_page):
        page_num = i + 1
        page_url = url + '/reviews?showOlderReviews=1&page=' + str(page_num) + '#reviewFilters'
        content = url_request(page_url)
        # take the review pages' html, print the review detail
        get_detail(content)
    return

# take the review pages' html, print the review detail
def get_detail(content):
    # find the place of useful information
    begin = content.find('<div class="reviewlisting clearfix">') + 5
    end = content.find('<div class="pagination-centered clearfix small-12-columns">')
    # make content a list of pieces of review
    content = content[begin:end].split('<div class="reviewlisting clearfix">')
    # in each piece of review, get the nationality, gender, textrating, ratings for individual items, and textreview
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
            print(str([country[1:], gender, age, text_rating] + rating + [review_text]))
        except:
            continue
    return

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

# enter a city name, and the program will print all the reviews of the hostels in that city
def city_based_search():
    city = input('Enter city: ').replace(' ', '-')
    url = 'https://www.hostelworld.com/findabed.php/ChosenCity.' + city +'/ChosenCountry.USA'
    hostel_list = get_list(url)
    print(hostel_list)
    for i in hostel_list:
        get_review(i)

# you need to go to HostelWorld to find the specific hostel website
# this function will prompt you to enter that website, and will print out all the reviews of that hostels
def hostel_based_search():
    url = input('Copy HostelWorld website: ').replace(' ','')
    get_review(url)


# instruction:
#   for city based search, you only need to put a city's name, not case sensitive
#       example: austin
#   for hostel based search, you need to go to HestelWorld and find the website of the hostel you are interested
#       and enter the website after prompt (you can press space key after the website if you are having trouble)
#       website example: https://www.hostelworld.com/hosteldetails.php/Hostel-Fish/Denver/98583

city_based_search()
#hostel_based_search()