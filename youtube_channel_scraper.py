from pymaybe import maybe
from bs4 import BeautifulSoup as bs
import requests
import urllib.parse

not_available = 'N/A'

youtube_domain = 'https://www.youtube.com'
youtube_query_string = '/results?search_query='
channel_filter_param = '&sp=EgIQAg%253D%253D'
selector_channel_divs = 'div.yt-lockup-content'
selector_next_page = 'div.branded-page-box a:last-child'
sub_selector_channel = 'a.yt-uix-tile-link'
sub_selector_channel_subscribers = 'span.yt-subscription-button-subscriber-count-branded-horizontal'
sub_selector_channel_total_views = 'div.about-stats b'
sub_selector_channel_join_date = 'div.about-stats span:nth-of-type(2)'
sub_selector_channel_location = 'div.country-container span:nth-of-type(2)'


search_term = input('Enter search URL: ')
no_of_result_pages = int(input('Enter the no. of search result pages(a page has 20 records): '))
print('*** Search term: ', search_term, ' | No. of results to be retrieved: <=', no_of_result_pages*20, ' ***')
youtube_params = youtube_query_string + urllib.parse.quote_plus(search_term) + channel_filter_param # URL encode the search term
channel_count = 1
for page in range(0, no_of_result_pages):
    url = youtube_domain + youtube_params
    source = requests.get(url).text
    soup = bs(source,'lxml')
    results = soup.select(selector_channel_divs)
    next_page_node = soup.select_one(selector_next_page)
    if next_page_node is None:
        break
    youtube_params = next_page_node['href']

    for result in results:
        channel_url = youtube_domain + result.select_one(sub_selector_channel)['href']
        channel_source = requests.get(channel_url + '/about').text
        inner_soup = bs(channel_source,'lxml')
        print()
        print('Page #', (page + 1), ' | Channel #', channel_count)
        print('Channel URL: ', channel_url)
        print('Channel name: ' + result.select_one(sub_selector_channel).text)
        print('Channel subscribers: ' + maybe(maybe(inner_soup.select_one(sub_selector_channel_subscribers)).text).or_else(not_available))
        print('Channel total views: ' + maybe(maybe(inner_soup.select_one(sub_selector_channel_total_views)).text).or_else(not_available))
        print('Channel join date: ' + maybe(maybe(inner_soup.select_one(sub_selector_channel_join_date)).text[len('Joined '):]).or_else(not_available))
        print('Channel location: ' + maybe(maybe(inner_soup.select_one(sub_selector_channel_location)).text.strip()).or_else(not_available))
        channel_count += 1
print('*** Retrieved ', channel_count, ' results in total ***')    
    
