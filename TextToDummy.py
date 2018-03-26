import csv
import wordfreq

useless_words = ['i', 'we', 'our', 'loved', 'felt', 'is', 'in', 'the', 'were', 'place', 'never', 'good', 'was',
                 'definitely', 'but', 'had', 'not', 'great', 'of', 'really', 'to', 's' , 'easy', 'also', 'or', 'and',
                 't', 're', 'hot', 'my', 'you', 'there', 'very', 'hostel', 'a', 'with', 'it', 'definitely', 'for',
                 'some', 'at', 'that','so', 'guests', 'few', 'more', 'stayed', 'an', 'it', 'out', 'hostels',
                 'from', 'would', 'am', 'than', 'would', 'stay', 'get', 'got', 'as', 'this', 'like', 'all', 'are',
                 'beautiful', 'too', 'up', 'could', 'if', 'here', 'on', 'don', 'be', 'no', 'amazing', 'nice', 'bad',
                 'time', 'have', 'night', 'us', 'lovely', 'want', 'meet', 'will', 'they', 'one', 'awesome', 'people',
                 'after', 'venice', 'super', 'only', 'excellent', 'who', 'made', 'hollywood', 'ever', 'just', 'best',
                 'perfect', 'beach', 'much', 'bit', 'which', 'lot', 'me', 'two', 'them', 'thanks', 'ok', 'again',
                 'make', 'again', 'common', 'feel', 'denver', 'little', 'even', 'because', 'can', 'recommend', 'your',
                 'experience', 'about', 'do', 'staying', 'first', 'well', 'however', 'high', 'though', 'old', 'overall',
                 'most', 'many', 'hotel', 'extremely', 'she', 'he', 'kind', 'wasn', 'chinese', 'highly', 'house', 've'
                 'has', 'by', 'didn', 'pretty', 'day', 'lots', 'amp', 'outside', 'fun', 'close', 'back', 'fish', 'over'
                 'other']

def main(fileName, age, gender):
    field = []
    data = []
    with open(fileName, encoding='utf-8', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for review in reader:
            review_detail = {}
            if review['age'] == age and review['gender'] == gender:
                text_review = review['text review']
                words = set(wordfreq.tokenize(text_review, 'en'))
                for i in words:
                    if i in ['housekeeping', 'professional', 'friendliness', 'staff', 'friendly', 'helpful', 'manager',
                             'management', 'service']:
                        i = 'staff'
                    elif i in ['cleanest', 'smelled','disgusting', 'clean', 'cleaning', 'cleaner', 'cleanliness', 'smelly',
                               'cleaned', 'dirty']:
                        i = 'clean'
                    elif i in ['room', 'rooms']:
                        i = 'room'
                    elif i in ['mattresses', 'slept', 'unfortunately', 'uncomfortable', 'bed', 'beds', 'comfortable',
                               'mattress', 'comfy', 'sleep', 'sleeping']:
                        i = 'bed'
                    elif i in ['towel', 'restrooms', 'restroom', 'door', 'doors', 'towels', 'showering', 'bathroom',
                               'shower', 'washroom', 'bath', 'toilet']:
                        i = 'bathroom'
                    elif i in ['nightclubs', 'cinema', 'adjacent', 'karaoke', 'locations', 'theatre', 'distance', 'far',
                               'located', 'shops', 'zoo', 'stadium', 'bar', 'bars', 'downtown', 'restaurant',
                               'restaurants', 'stores', 'location', 'areas']:
                        i = 'location'
                    elif i in ['music', 'quiet', 'loud', 'atmosphere', 'noise', 'noisy', 'earplugs']:
                        i = 'atmosphere'
                    elif i in ['window', 'laundry', 'kitchens', 'sofas', 'facility', 'light', 'pool', 'ac', 'air', 'locker',
                               'internet', 'backyard', 'fans', 'sofa', 'curtains', 'walls', 'tv', 'wifi', 'microwave',
                               'fan', 'lockers', 'kitchen', 'cooking', 'facilities', 'parking', 'desk']:
                        i = 'facilities'
                    elif i in ['walk', 'walking', 'taxi', 'transportation', 'road', 'train', 'buses', 'uber', 'bus',
                               'station', 'convenient', 'traffic', 'highway', 'freeway', 'metro', 'shuttle', 'transport']:
                        i = 'transportation'
                    elif i in ['paid', 'affordable', 'price', 'free', 'value', 'worth', 'budget', 'cheap', 'cheaper',
                               'payment', 'dollars', 'purchase''money', 'save', 'expensive', 'pay', 'deal']:
                        i = 'value'
                    elif i in ['dangerous', 'stolen', 'guns', 'unsafe', 'safe', 'secure', 'safety', 'security', 'creepy' ]:
                        i = 'security'
                    elif i in ['private', 'privacy']:
                        i = 'private'
                    elif i in ['activities', 'tours', 'events', 'social', 'attractions', 'parties', 'drinking',
                               'attraction']:
                        i = 'activities'
                    if i not in useless_words and not i.isdigit():
                        if i not in field:
                            field.append(i)
                        review_detail[i] = 1
                data.append(review_detail)
        csvfile.close()

    with open(fileName.split('.')[0] + gender + age + '_dummy.csv', 'w', encoding='utf-8', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
        csvfile.close()
    print('finish')
# possible options:
#   age:        '18-24', '25-30', '31-40', '40+'
#   gender:     'Female', 'Male', 'Couple', 'MixedGroup', 'AllFemaleGroup', 'AllMaleGroup'

# you have to download the data first using hostel.py
main(fileName = 'denver.csv', age='18-24', gender='Female')

