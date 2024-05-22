import gspread
import re
import workshop_api

gc = gspread.service_account()

spreadsheet = gc.open("Space Engineers Modlist")
worksheet = spreadsheet.get_worksheet(0)



def update_mod_sizes():
	all_values = worksheet.get_all_values()

	batch_updates = []

	for i, row in enumerate(all_values[1:], start=2):
		if not row[0]:
			break

		steam_id = re.sub(r'^Steam:', '', row[0])
		print(f'Processing Steam:{steam_id}')
		
		try:
			mod_size = workshop_api.get_mod_size(steam_id)
			print(f'Steam:{steam_id} = {mod_size}')
			batch_updates.append({
				"range": f"D{i}",
				"values": [[mod_size]]
			})
		except Exception as e:
			print(f"Error fetching mod size for Steam:{steam_id}: {e}")

		# Calculate percentage completion
		percentage_complete = (i - 1) / (len(all_values) - 1) * 100
		print(f'{percentage_complete:.1f}% complete')

	if batch_updates:
		try:
			worksheet.batch_update(batch_updates)
			print('Successfully submitted to worksheet!')
		except Exception as e:
			print(f"Error updating worksheet: {e}")



def update_tags():
	all_values = worksheet.get_all_values()

	batch_updates = []

	for i, row in enumerate(all_values[1:], start=2):
		if not row[0]:
			break

		steam_id = re.sub(r'^Steam:', '', row[0])
		print(f'Processing Steam:{steam_id}')

		try:
			mod_tags = workshop_api.get_mod_tags(steam_id)
			print(f'Steam:{steam_id} = {mod_tags}')
			batch_updates.append({
				"range": f"C{i}",
				"values": [[mod_tags]]
			})
		except Exception as e:
			print(f"Error fetching mod tags for Steam:{steam_id}: {e}")

		# Calculate percentage completion
		percentage_complete = (i - 1) / (len(all_values) - 1) * 100
		print(f'{percentage_complete:.1f}% complete')

	if batch_updates:
		try:
			worksheet.batch_update(batch_updates)
			print('Successfully submitted to worksheet!')
		except Exception as e:
			print(f"Error updating worksheet: {e}")





def sort_data():
	all_values = worksheet.get_all_values()

	# Get the number of rows (excluding header)
	num_rows = len(all_values) - 1

	# Define the range to sort
	sort_range = f"A2:Z{num_rows + 1}"  # Assuming your data starts from row 2

	# Sort the worksheet based on column D
	worksheet.sort((4, 'des'), range=sort_range)

	print('Spreadsheet sorted successfully!')



if __name__ == '__main__':
	update_tags()