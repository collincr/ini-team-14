import datetime as dt
import collections
import operator
from shortest_path import internal_get_spt_from_stat_name
import shortest_path as sp
import json
import time
import itertools

distance_dct = {}
road_network_dic = None
station_info_dic = None
stations_shortest_path_dic = None
stat_name_dic = None

'''
def main():
	station_list = {"B-15", "DOR64", "DOR65", "DOR66", "CS1", "B-14", "DOR68"}
	#print(station_list)

	stat_dic = sp.get_station_dic()
	stat_name_dic = sp.create_stat_name_id_mapping(stat_dic)
	for stat in station_list:
		print(stat, stat_name_dic[stat])
#	stat_id_list = {'6', '37', '38', '39', '47', '4', '40'}
#	time, visit_path = get_visit_path_by_id(stat_id_list, [], [])
	#print(str(dt.timedelta(seconds = time.time())))
	#station_list = ["DOR37", "DOR38", "DOR39", "CS8", "CS9", "CS34", "CS35"]
        #get_permutation_with_mini_time(station_list)
	#visit_path, times = get_visit_path_by_name(station_list, [], [])
	#print(visit_path)
	#print(times)
	#print(str(dt.timedelta(seconds = time.time())))
        station_list = ["DOR37", "DOR38", "DOR39", "CS8", "CS9", "CS34", "CS35"]
        get_permutation_with_mini_time(station_list)
'''
def main():
    #station_list =  ["CS11", "CS12", "CS13", "CS36", "CS37", "CS38", "RE33"]
    with open("../app_data/cluster_info.json") as file:
        cluster_dic = json.load(file)

    #get_permutation_with_mini_time(station_list)
    visit_path, times = get_visit_path_by_name(cluster_dic["19"]["stations"], [], [])
    #print(visit_path)
    #print(times)


def get_visit_path(stat_id_list, visit, visit_time):

	#print(str(dt.timedelta(seconds = time.time())))
	# Initialize the station dict
	road_network_dic, station_info_dic = sp.preprocess()
	stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()

	station_list = []
	for stat_id in stat_id_list:
		station_list.append(str(station_info_dic[stat_id]['name']))
	
	permutation_list = get_permutation_with_mini_time(station_list)

	visit_path, visit_time = simulate_visit_station(permutation_list, visit, visit_time)
	#print(str(dt.timedelta(seconds = time.time())))
	
#	id_path = []
#	stat_name_dic = sp.create_stat_name_id_mapping(station_info_dic)
#	print(visit_path)
#	for stat in visit_path:
#		id_path.append(stat_name_dic[stat])
#	visit_path = id_path

	return visit_path, visit_time

def preprocess():
    global station_info_dic
    global stat_name_dic
    if station_info_dic is None:
        road_network_dic, station_info_dic = sp.preprocess()
    if stat_name_dic is None:
        stat_name_dic = sp.create_stat_name_id_mapping(station_info_dic)

def get_visit_path_by_id(stat_id_list, visit_path, visit_time):
    #print("get_visit_path_by_id",visit_path)
    global station_info_dic
    road_network_dic, station_info_dic = sp.preprocess()
    station_name_list = []
    visit_name_path = []
    visit_name_time = visit_time.copy()
    for stat_id in stat_id_list:
        station_name_list.append(str(station_info_dic[stat_id]['name']))
    for stat_id in visit_path:
        visit_name_path.append(station_info_dic[stat_id]['name'])

    #original_path = visit_path.copy()
    #oritinal_time = visit_time.copy()
    oritinal_len = len(visit_path)
    #visited_path, visited_time = get_visit_path_by_name(station_name_list, visit_name_path, visit_time)
    get_visit_path_by_name(station_name_list, visit_name_path, visit_name_time)
    #print("After get_visit_path_by_name", visit_name_path)
    tmp_id_path = []
    stat_name_dic = sp.create_stat_name_id_mapping(station_info_dic)
    for stat in visit_name_path[oritinal_len:len(visit_name_path)]:
        if stat in stat_name_dic:
            tmp_id_path.append(stat_name_dic[stat])
        else:
            print("stat not found in name-id mapping")
    '''
    id_path = []
    stat_name_dic = sp.create_stat_name_id_mapping(station_info_dic)
    for stat in visit_path:
        if stat in stat_name_dic
        id_path.append(stat_name_dic[stat])
    '''
    #print("tmp_id_path", tmp_id_path)
    #print(visited_time)
    return tmp_id_path, visit_name_time[oritinal_len:len(visit_name_path)]

def get_visit_path_by_id_tmp(stat_id_list, visit_path, visit_time):
    global station_info_dic
    road_network_dic, station_info_dic = sp.preprocess()
    station_name_list = []
    visit_name_path = []
    for stat_id in stat_id_list:
        station_name_list.append(str(station_info_dic[stat_id]['name']))
    for stat_id in visit_path:
        visit_name_path.append(station_info_dic[stat_id]['name'])

    #visited_path, visited_time = get_visit_path_by_name(station_name_list, visit_name_path, visit_time)
    get_visit_path_by_name(station_name_list, visit_name_path, visit_time)
    #print("After get_visit_path_by_name", visit_name_path)
    tmp_id_path = []
    stat_name_dic = sp.create_stat_name_id_mapping(station_info_dic)
    for stat in visit_name_path:
        if stat in stat_name_dic:
            tmp_id_path.append(stat_name_dic[stat])
        else:
            print("stat not found in name-id mapping")
    '''
    id_path = []
    stat_name_dic = sp.create_stat_name_id_mapping(station_info_dic)
    for stat in visit_path:
        if stat in stat_name_dic
        id_path.append(stat_name_dic[stat])
    '''
    #print("tmp_id_path", tmp_id_path)
    #print(visited_time)
    return tmp_id_path, visit_time

def get_visit_path_by_name(stat_name_list, visit_path, visit_time):
    #print("get_visit_path_by_name", visit_path)
    global stations_shortest_path_dic
    stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()
    permutation_list = get_permutation_with_mini_time(stat_name_list)
    #visited_path, visited_time = simulate_visit_station(permutation_list, visit_path, visit_time)
    #print("before")
    #print(visit_path)
    #print(visit_time)
    simulate_visit_station(permutation_list, visit_path, visit_time)
    #print("after")
    #print(visit_path)
    #print(visit_time)
    return visit_path, visit_time
    #return visited_path, visited_time

def getTime(timestr):
	minute = timestr / 60
	second = (timestr % 60) * 60
	return str(minute) + ":" + str(second)

def get_travel_time_from_id(stat_id1, stat_id2):
    global station_info_dic
    preprocess()
    if stat_id1 not in station_info_dic or stat_id2 not in station_info_dic:
        print("Stations id not found")
        return -1
    name1 = station_info_dic[stat_id1]['name']
    name2 = station_info_dic[stat_id2]['name']
    return getTravelTime(name1, name2)

def getTravelTime(station1, station2):
	if station1 == station2:
		return 0
	if station1 in distance_dct and station2 in distance_dct[station1]:
		#print("cache")
		return distance_dct[station1][station2]

	if station2 in distance_dct and station1 in distance_dct[station2]:
		#print("cache")
		return distance_dct[station2][station1]
	
	if station1 not in distance_dct:
		distance_dct[station1] = {}
	
	time_station = json.load(open("time.json"))
	#print(station1, station2)
	distance_dct[station1][station2] = time_station[station1][station2]

	return distance_dct[station1][station2]

def getDistance(station1, station2):
	if station1 in distance_dct and station2 in distance_dct[station1]:
		#print("cache")
		return None, distance_dct[station1][station2]

	if station2 in distance_dct and station1 in distance_dct[station2]:
		#print("cache")
		return None, distance_dct[station2][station1]

	distance = 0
	'''
	if stations_shortest_path_dic is not None:
		stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()
		distance, path = sp.get_shortest_path(station1, station2,
			 station_info_dic,stations_shortest_path_dic)
	if distance is None or path is None:
		path, distance = internal_get_spt_from_stat_name(station1, station2)
	'''
	global stations_shortest_path_dic
	if stations_shortest_path_dic is not None:
		distance, path = sp.get_shortest_path(station1, station2, station_info_dic,
				stations_shortest_path_dic)
	else:
		print("stations_shortest_path_dic is None")
		path, distance = internal_get_spt_from_stat_name(station1, station2)
	if station1 not in distance_dct:
		distance_dct[station1] = {}

	distance_dct[station1][station2] = distance
	return None, distance

def get_permutation_with_mini_time(station_list):
        #permutations = permute(station_list)
        curr = time.time()
        permutations = list(itertools.permutations(station_list))
        min_time = 0
        #print("Possible permutations number:")
        #print(len(permutations))
        #print("Time spent: " + str(dt.timedelta(seconds = time.time() - curr)))
        #print("Calculating the permutation with minimum time spent...")
        curr = time.time()
        permutation_list = []
        for stations in permutations:
                times, res = add_visit_timestamp(stations)
                if min_time == 0 or times < min_time:
                        min_time = times
                        permutation_list = res
        #print("Permuation with minimum time found")
        #print("Time spent: " + str(dt.timedelta(seconds = time.time() - curr)))
        #print("get_permutation_with_mini_time")
        #print(permutation_list)
        #print(min_time)
        return permutation_list

def get_permutation_start_with_station(station_list, station):
	#permutations = permute(station_list)
	permutations = list(itertools.permutations(station_list))
	min_time = 0
	permutation_list = []
	for stations in permutations:
		if not stations[0] == station:
			continue
		time, res = add_visit_timestamp(stations)
		if min_time == 0 or time < min_time:
			min_time = time
			permutation_list = res
	print("get_permutation_start_with_station done ", min_time)
	#print(permutation_list)
	return permutation_list

def simulate_visit_station(permutation_list, visit_path, visit_time):
	#print("!!!!!!")
	#print(permutation_list)
	#N = 30*60
	#N = 1*60*60
	#N = 1.5*60*60
	N = 2*60*60
	#N = 2.5*60*60
	M = 15*60
	#M = 30*60
	#M = 60*60
	test_time = 150*3
	speed = 3
	last_time_repeat = 0
	current_time = 0
	visited_stations = []
	index = 0
	left_stations = permutation_list.copy()
	previous_time = 0
	current_station = left_stations[0]

	if len(visit_path) != len(visit_time):
		print("visit path and timestamp not match!")

	# Update current_time
	if len(visit_path) > 0:
		#_, distance = getDistance(visit_path[-1], permutation_list[0])
		#current_time = visit_time[-1] + distance/speed
		current_time = visit_time[-1] + getTravelTime(visit_path[-1], permutation_list[0])
		last_time_repeat = current_time
		#print("Set current_time", current_time)
	
	while len(left_stations) > 0:
		if current_station in left_stations:
			left_stations.remove(current_station)
		
		#print("visit: "+str(current_station)+" at time: "+getTime(current_time))
		visit_path.append(current_station)
		visit_time.append(current_time)
		
		# Simulate the test time
		current_time = current_time + test_time

		if current_time - last_time_repeat > N:
			print("Making choice!!!!!!! ", current_station)
			#print(current_station)
			#print("N=", N, "timeout")
			if len(visit_path) == 0:
				print("Error!!!!!!!!!!!!!!!!!!!!!!!!!")
			else:
				station_travel_time = {}
				for i in range(0, len(visit_path)):
					if current_station == visit_path[i]:
						continue
					travel_time = getTravelTime(current_station, visit_path[i])
					#print(visit_path[i])
					# travel_time = distance // speed
					#print(getTime(travel_time))
					if current_time - visit_time[i] + travel_time > N and travel_time < M:
						station_travel_time[visit_path[i]] = travel_time
				# Choose the station with minimum travel time
				if len(station_travel_time) > 0:
					sorted_s = sorted(station_travel_time.items(), key=operator.itemgetter(1))
					sorted_station = collections.OrderedDict(sorted_s)
					first_station = next(iter(sorted_station))
					#print("Revisit", first_station)

					# Go back to visit the repeat station
					current_station = first_station
					current_time += station_travel_time[first_station]
					last_time_repeat = current_time

					# Update the new order
					new_list = []
					new_list.append(current_station)
					for station in left_stations:
						new_list.append(station)
					left_stations = get_permutation_start_with_station(new_list, current_station)
					print("New seq:", left_stations)
					if current_station in left_stations:
						#print("left_stations.remove", current_station)
						left_stations.remove(current_station)
					continue
				else:
					#print("No visited stations satisfy the repeat condition!!!!!!")
                                        pass

		if len(left_stations) > 0:
			next_station = left_stations[0]
			travel_time = getTravelTime(current_station, next_station)
			# travel_time = distance // speed
			current_time += travel_time
			current_station = next_station

	print("final path:")
	print(visit_path)
	print(visit_time)
	return visit_path, visit_time


''' Find all permutations of a station list.
'''
def permute(station_list):
	permutations = list()
	tmp_list = list()
	backtrack(permutations, tmp_list, station_list)
	return permutations


''' Helper function for permutation.
'''
def backtrack(permutations, tmp_list, station_list):
	if len(tmp_list) == len(station_list):
		permutations.append(list(tmp_list))
		return
	for station in station_list:
		if station in tmp_list:
			continue
		tmp_list.append(station)
		backtrack(permutations, tmp_list, station_list)
		del tmp_list[len(tmp_list) - 1]


''' Add time for each station in the list.
	All times are measured in secondes.
'''
def add_visit_timestamp(stations):
	last_station = None
	res = list()
	departure_time = 0
	for station in stations:

		if last_station == None:
			arrival_time = 0
		else:
			# 10m/s i.e. 36km/h Will be speed between actual station
			speed = 10
			road_time = getTravelTime(last_station, station)
			# road_time = distance // speed   # intra-station time (secs)
			arrival_time = departure_time + road_time

		measure_time = 150                  # inner-station time (secs)
		departure_time = arrival_time + measure_time
		last_station = station

		res.append(station)

	return departure_time, res


if __name__ == '__main__':
	main()
