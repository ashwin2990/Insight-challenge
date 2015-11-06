import json
import unicodedata
import re
from datetime import datetime
from time import time
from dateutil.relativedelta import relativedelta
import sys

'''
Function name: read_tweets
Input: filename - filename to fetch the tweets
Description: This function reads in the json files and returns the twitter feeds. It reads the file line by
			line storing all the tweets in the tweet_feed array
Return type: tweet_feed - tweetcontaining all the tweets
'''

def read_tweets(filemame):
	tweet_feed=[]	# array to store all the tweets
	with open(filemame) as tweet_input:
		for line in tweet_input:
			if(len(line.split())>1):
				tweet_feed.append(json.loads(line))
	return tweet_feed


'''
Function name: extract_hash_tags
Input: s - string to find hashtags
Description: This function uses the regex library to find all hashtags in the string
Return type: Array containing all the hashtags in the string
'''

def extract_hash_tags(s):
    return re.findall(r"#(\w+)", s)


'''
Function name: average_vertex
Input: graph_vert: graph containing all the edge information
Description: This function calculates the average of all the node vertices
Return type: floating number containing the average
'''
def average_vertex(graph_vert):
	total_vert=0
	for key in graph_vert:
		total_vert+=len(graph_vert[key])

	if(len(graph_vert.keys())!=0):
		return float(total_vert)/len(graph_vert.keys())
	else:
		return 0	


'''
Function name: add_vertices
Input: graph_dict: dictionary containing the graph to be updated
		hashtags_graph_array:contains the ids of all the hashtags for which vertices need to be added
Description: This function adds edges by either creating a new node and adding edges or by updating existing nodes with new edge information
Return type: dictionary with updated values
'''
def add_vertices(graph_dict,hashtags_graph_array):	
		
	for hashtags in hashtags_graph_array: 
		temp_list=hashtags_graph_array[:]	# temperary list that will store original array when edges are created
		hashtags_graph_array.remove(hashtags)
		if hashtags in graph_dict.keys():
			old_list=list(graph_dict[hashtags])	#list of values already associated with the existing node
			graph_dict[hashtags]=list(set(old_list + hashtags_graph_array))					
		else:
			graph_dict[hashtags]=hashtags_graph_array	
		hashtags_graph_array=temp_list[:]
	return graph_dict

'''
Function name: remove_vertices
Input: graph_dict: dictionary containing the graph to be updated
		hashtags_graph_array:contains the ids of all the hashtags for which vertices need to be added
Description: This function removes edges by removing values associated with the id that needs to be deleted
Return type: dictionary with updated values
'''


def remove_vertices(graph_dict,hashtags_graph_array):	
		
	for hashtags in hashtags_graph_array: 
		temp_list=hashtags_graph_array[:]	# temperary list that will store original array when edges are created
		hashtags_graph_array.remove(hashtags)
		if hashtags in graph_dict.keys():
			old_list=list(graph_dict[hashtags])	#list of values already associated with the existing node
			graph_dict[hashtags]=list(old_list - hashtags_graph_array)						
		hashtags_graph_array=temp_list[:]
	return graph_dict

		
'''
Function name: update_nodes
Input: graph: dictionary containing the graph to be updated
		hashtags_id:contains the ids of all the hashtags for which vertices need to be added
		hashtag_feed: array containing all the hashtag info associated with each id
Description: This function finds the hashtags associated with a tweet so that the info can be given to add_vertices to create edges
Return type: dictionary with updated values
'''
def update_nodes(graph,hashtag_id,hashtag_feed):
	hashtags_graph_array=[]
	for item in hashtag_feed[hashtag_id]:
		hashtags_graph_array.append(item)
	graph=add_vertices(graph,hashtags_graph_array)
	return graph


'''
Function name: delete_nodes
Input: graph: dictionary containing the graph to be updated
		id_list:contains the ids of all the hashtags for which vertices need to be deleted
		hashtag_feed: array containing all the hashtag info associated with each id
Description: This function finds the hashtags associated with a tweet so that the info can be given to remove_vertices to remove edges
Return type: dictionary with updated values
'''
def delete_nodes(graph,id_list,hashtag_feed):
	hashtags_graph_array=[]
	for item in id_list:
		hashtags_graph_array.append(hashtag_feed[item])
	graph=remove_vertices(graph,hashtags_graph_array)
	return graph		


'''
Function name: write_averages
Input: filename: filename to which averages need to be written
		averages: array containing the averages at each tweet
Description: This function writes the averages obtained to a file
Return type: 
'''
def write_averages(filename,averages):
	with open(filename,"w") as f:
		for item in averages:
			f.write("%s\n" %str(item))







'''
Following lines of code parse the tweet input txt file and 
store all the relevant information into the arrays and dictionaries 
mentioned above. For time_dict, only hashtags that need updating are
stored along with their timestamp
'''

'''
Following lines of code find the tweets that need to be deleted by calculating
the timestamps that need deleting. It also build/updates nodes based on new feed 
information and finds the average of all the node vertices.
'''





def main():
	tweet_feed=[]		#feed information
	hashtag_feed={}		#dictionary containing the hashtags associated with each id
	hashtag_time={}		#dictionary containing the timestamp for each id
	time_dict={}		#dictionary to store the times (and the nodes/hashtags) which need to be updated i.e. blank and single hashtags are not stored
	hashtag_order=[]	#array to store the order of ids in which the tweets come in
	graph={}			#dictionary used as a graph
	temp_list=[]		#temporary list used to update values of time_dict
	averages=[]			#array containing all the averages
	input_filename=str(sys.argv[1])
	tweet_feed=read_tweets(input_filename)

	for item in tweet_feed:
		hashtags=extract_hash_tags(item['text'].encode('ascii','ignore'))
		hashtag_id=item['id']		
		hashtag_order.append(hashtag_id)		
		hashtag_feed[hashtag_id]=hashtags
		hashtag_time[hashtag_id]=str(item['created_at'])
		if(len(hashtags)>1):
			date_time=datetime.strptime(str(item['created_at']),'%a %b %d %H:%M:%S +0000 %Y')
			if(str(item['created_at']) in time_dict.keys()):
				temp_list=list(time_dict[date_time])
				time_dict[date_time]=temp_list+[hashtag_id]
			else:
				time_dict[date_time]=[hashtag_id]

	time_prev=datetime.strptime('Mon Jan 01 12:00:00 +0000 2000','%a %b %d %H:%M:%S +0000 %Y')
	for item in hashtag_order:
		time_current=datetime.strptime(hashtag_time[item],'%a %b %d %H:%M:%S +0000 %Y')
		min_time=datetime.strptime((hashtag_time[item]),'%a %b %d %H:%M:%S +0000 %Y')+relativedelta(seconds=-61)

		if((time_current-time_prev).total_seconds()>60):
			graph={}

		if(min_time in time_dict.keys()):
			graph=delete_nodes(graph,time_dict[min_time],hashtag_feed)
			last_id_index=hashtag_order.index(time_dict[min_time][len(time_dict[min_time])-1])
			current_id_index=hashtag_order.index(item)


		if(len(hashtag_feed[item])>1):
			graph=update_nodes(graph,item,hashtag_feed)


		averages.append(round(average_vertex(graph),2))

		time_prev=datetime.strptime(hashtag_time[item],'%a %b %d %H:%M:%S +0000 %Y')	
	output_filename=str(sys.argv[2])		
	write_averages(output_filename,averages)





main()			
