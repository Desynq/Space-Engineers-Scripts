import gspread
import re
import workshop_api

gc = gspread.service_account()

spreadsheet = gc.open("Space Engineers Modlist")
worksheet = spreadsheet.get_worksheet(0)
all_values = worksheet.get_all_values()

batch_updates = []

for i, row in enumerate(all_values[1:], start=2):
	if not row[0]:
		break

	steamid = re.sub(r'^Steam:', '', row[0])
	print(f'Processing Steam:{steamid}')
	
	try:
		mod_size = workshop_api.get_mod_size(steamid)
		print(f'Steam:{steamid} = {mod_size}')
		batch_updates.append({
			"range": f"D{i}",
			"values": [[mod_size]]
		})
	except Exception as e:
		print(f"Error fetching mod size for Steam:{steamid}: {e}")

	# Calculate percentage completion
	percentage_complete = (i - 1) / (len(all_values) - 1) * 100
	print(f'{percentage_complete:.1f}% complete')

if batch_updates:
	try:
		worksheet.batch_update(batch_updates)
		print('Successfully submitted to worksheet!')
	except Exception as e:
		print(f"Error updating worksheet: {e}")