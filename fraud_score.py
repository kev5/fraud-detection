from geopy.distance import vincenty
import requests
import sys
import time


def get_results(params):
	"""Return the IP info"""
	access_token = "18d4e7386b66b4"
	header = {'Authorization': 'Bearer %s' % access_token}
	resp = requests.get(url="http://ipinfo.io/" + str(params), headers=header)

	# Transforms the JSON API response into a Python dictionary
	data = resp.json()
	return data


def get_distance(lat1, lat2, long1, long2):
	"""Return the distance between 2 IP addresses"""
	coords_1 = (lat1, long1)
	coords_2 = (lat2, long2)
	return vincenty(coords_1, coords_2).miles


def reverse_index(alist, value):
	"""Finding the index of last occurence of an element"""
	return len(alist) - alist[-1::-1].index(value) -1


def main():
	"""Driver Function"""
	try:
		curr_ip = sys.argv[1]
		records = sys.argv[2]
	except IndexError:
		print("Please enter 2 arguments- IP address followed by a records.txt file.")
		sys.exit.exit(0)

	# Getting coordinates of current IP
	ans = get_results(curr_ip)
	loc = ans["loc"].split(",")
	lat1 = loc[0]
	long1 = loc[1]

	# Reading the past records
	lines = open(records, 'r').read().split('\n')

	res = []

	for line in lines:
		info = line.split(" ")
		status = info[0] 
		ip = info[1]

		# Getting coordinates of the IP in the records
		ans = get_results(ip)
		loc2 = ans["loc"].split(",")
		lat2 = loc2[0]
		long2 = loc2[1]

		res.append(get_distance(lat1, lat2, long1, long2))

		# Not abusing the API calls
		time.sleep(1.0)


	# Closest IP address by distance
	closest_ip_distance = min(res)

	# If we go by the first occurence of the closest IP
	closest_ip = lines[res.index(closest_ip_distance)]

	# If we go by the last occurence of the closest IP
	# closest_ip = lines[reverse_index(res, closest_ip_distance)]

	status = closest_ip.split(" ")[0]
	if status == "FRAUD":
		print("Score: " + str(round(2 * closest_ip_distance, 3)) + " (Last closest Login was FRAUD)")
	else:
		print("Score: " + str(round(closest_ip_distance, 3)))


if __name__=="__main__":
	main()
