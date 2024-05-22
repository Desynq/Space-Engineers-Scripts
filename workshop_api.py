import requests
from bs4 import BeautifulSoup


def convert_to_bytes(size_str):
	# Define unit multipliers
	unit_multipliers = {
		'B': 1,
		'KB': 1024,
		'MB': 1024**2,
		'GB': 1024**3,
		'TB': 1024**4,
	}
	
	# Extract the numeric part and the unit part from the input string
	size_parts = size_str.split()
	value = float(size_parts[0])
	unit = size_parts[1].upper()  # Ensure the unit is in uppercase
	
	# Convert the value to bytes
	return int(value * unit_multipliers[unit])



def get_mod_size(workshop_id: int, default_value=0):

	mod_url = f'https://steamcommunity.com/sharedfiles/filedetails/?id={workshop_id}'

	# Make the HTTP request
	response = requests.get(mod_url)

	# Check if the request was successful
	if response.status_code != 200:
		return default_value

	# Parse the content with BeautifulSoup
	soup = BeautifulSoup(response.text, 'html.parser')
	
	# Find the div with class 'detailsStatsContainerRight'
	details_container = soup.find('div', class_='detailsStatsContainerRight')
	if not details_container:
		return default_value

	# Find all 'div' tags within the 'detailsStatsContainerRight' div
	details_stats = details_container.find_all('div', class_='detailsStatRight')
	if not (details_stats and len(details_stats) > 0):
		return default_value

	file_size = details_stats[0].text
	return convert_to_bytes(file_size)


def get_mod_tags(workshop_id: int, default_value=''):

	mod_url = f'https://steamcommunity.com/sharedfiles/filedetails/?id={workshop_id}'
	response = requests.get(mod_url)
	if response.status_code != 200:
		return default_value
	
	soup = BeautifulSoup(response.text, 'html.parser')

	workshop_tags_divs = soup.find_all('div', class_='workshopTags')

	if len(workshop_tags_divs) < 2:
		return default_value
	
	second_workshop_tags_div = workshop_tags_divs[1]
	tag_links = second_workshop_tags_div.find_all('a')

	tags = [tag.text for tag in tag_links]
	for i, tag in enumerate(tags):
		if tag == 'hud':
			tags[i] = 'HUD'

	return ', '.join(tags)
