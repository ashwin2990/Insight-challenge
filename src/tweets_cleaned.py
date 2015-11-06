# example of program that calculates the number of tweets cleaned
import json
import unicodedata
import sys

'''
Function name: read_tweets
Input: filename - filename to fetch the tweets
Description: This function reads in the json files and returns the twitter feeds. It reads the file line by
			line storing all the tweets in the tweet_feed array
Return type: tweet_feed - tweetcontaining all the tweets
'''
def read_tweets(filemame):
	tweet_feed=[]
	with open(filemame) as tweet_input:
		for line in tweet_input:
			if(len(line.split())>1):
				tweet_feed.append(json.loads(line))
	return tweet_feed		

'''
Function name: write_clean_feed
Input: filename - filename to fetch the tweets
		tweet_feed- feed to be cleaned
		relevant_feed-feed dictionary for the timestamp
Description: This function writes clean feed information to the output file
Return type: tweet_feed - tweetcontaining all the tweets
'''

def write_clean_feed(filename,tweet_feed,relevant_feed):
	count_unicode=0		
	with open(filename,"w") as f:
		for item in tweet_feed:
			normalized_text=item['text'].encode('ascii','ignore')
			if(normalized_text!=item['text']):
				count_unicode+=1	
			f.write("%s (timestamp: %s)\n" %(normalized_text, relevant_feed[item['text']]))
		f.write("\n%s tweets contained unicode."% str(count_unicode))



def main():
	tweet_feed=[]
	relevant_feed={}		#dictionary containing timestamp information
	input_filename=str(sys.argv[1])
	output_filename=str(sys.argv[2])
	tweet_feed=read_tweets(input_filename)
	for item in tweet_feed:
		relevant_feed[item['text']]=item['created_at']


	write_clean_feed(output_filename,tweet_feed,relevant_feed)

			



		 


main()