import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialized a dictionary with regions and corresponding codes used in the Search filter on the website
regional_codes = {"East": '3741', "East Midlands": '3981', "London": '4186', "North East": '4356', "North West": '4421',
                  "South East": '4621', "South West": '4961', "West Midlands": '5151', "Yorkshire & the Humber": "5306"}

internal_links = []
organization_name = []
prefix = "https://www.homeless.org.uk/"
websites = []

# Organised search results by regions
for j in regional_codes:
    # Created an overshoot in the case the number of subpages for a particular region would increase
    for i in range(0, 50):

        page = requests.get(
            f'https://www.homeless.org.uk/search-services?field_geofield_latlon=&field_geofield_latlon_op=5'
            f'&field_homeless_england_type=All&field_region_and_local_authority='
            f'{regional_codes[j]}&field_homeless_england_type_1=All&page=0%2C{i}')

        soup = BeautifulSoup(page.content, 'html5lib')

        name_list = soup.find_all('h3')

        for organization in name_list:
            if organization.find('a'):
                # Internal link points to an internal page with more information on a particular organization
                internal_links.append(prefix + organization.find('a')['href'])
                organization_name.append(organization.find('a').get_text())
    # Here an external link to the organization's website is extracted
    for a in internal_links:
        site = requests.get(a)
        soup = BeautifulSoup(site.content, 'html5lib')
        link = soup.find("div", class_="large-8 columns").find("a", target="_blank")
        if link:
            websites.append(link.get_text())
        else:
            websites.append("Website not found")
    # In the final step the relevant information about a particular organization is stored into a csv. file
    df = pd.DataFrame.from_dict(
        {"Organization name": organization_name, "Internal Links": internal_links, "Website links": websites, "Region": j,
         "Region code": regional_codes[j]})
    df.to_csv(f'{j}_table.csv')
    organization_name = []
    internal_links = []
    websites = []
