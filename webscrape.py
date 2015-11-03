from bs4 import BeautifulSoup
import json
import requests

# I considered trying to use the URL as an argument in a later function
# I decided it wasn't worth the time as the url patterns won't
# necessarily be consistent across different scrape targets
# and custom solutions are probably often necesary.
root_url = "http://data-interview.enigmalabs.org"

# Each business will have its info placed in a dict
# After each business' HTML is scraped, that dict is appended to business_list
business_list = []


all_business_urls = []


# This function is not particularly time-saving in this case
# But If I were hardcoding tons and tons of different requests
# It would be nice to use this to avoid having to
# repeat request/beautiful soup item
# every time I wanted to use this
def get_beautiful_object(input_url):
    requested_item = requests.get(input_url)
    beautiful_object = BeautifulSoup(requested_item.text)
    return beautiful_object


def get_all_urls():
    for x in range(1, 11):
        # Here I am hitting each page in Edgar's list to build a list of URLs.
        this_url = root_url + '/companies/?page=' + str(x)
        list_Page = get_beautiful_object(this_url)
        # All business links are in anchor elements within TD element.
        links = list_Page.findAll("td")
        for link in links:
            if link.a:
                    # Not all the TD elements have an anchor child.
                    # If a TD has an anchor child, get the HREF and append it
                    # to the all_business_urls list
                all_business_urls.append(link.a.attrs['href'])


def get_business_info():
    for url in all_business_urls:
        business_dict = {}
        # This dict will be rewritten with a
        # particular business' information each time throuth this loop
        business_url = root_url + url
        business_obj = get_beautiful_object(business_url)
        table_rows = business_obj.select('td[id]')
        # The only TD elements with an ID attribute
        # are the ones that contain the data we want.
        for row in table_rows:
                # Keying the id attr to the value.
                # the ID contains no spaces and is good key for JSON.
            business_dict[row.attrs['id']] = row.getText()

        # adding dict to list at the end of each scrape
        business_list.append(business_dict)

# dump the business_list to JSON after all scrapes are done.


def write_to_json(file_name):
    with open(file_name, 'w') as outfile:
        json.dump(business_list, outfile)


def scrape(file_name):
    get_all_urls()
    get_business_info()
    write_to_json(file_name)

if __name__ == "__main__":
    scrape("solution.json")
