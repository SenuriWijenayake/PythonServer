from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from pymongo import MongoClient

# create the database connection
client = MongoClient("localhost", 27017)
db = client.script

locationPosts = db.locationPosts
locationData = list(locationPosts.find())
sid = SentimentIntensityAnalyzer()

# extract the post details and identify post status and comments separately
def extractPostDataForUser(user_id):
        postDetails = []
        commentDetails = []

        userDetails = db.locationPosts.find_one({'user_id':user_id},{'_id':0})
        locationDetails = userDetails['locations']
        for location in locationDetails:
                # append the status data
                if('message' in location):
                        postDetails.append({"user_id": userDetails['user_id'], "locationName": location['place']['name'],
                                              "message": location['message'], "post_id":location['post_id'], "location" : location['place']})
                if('comments' in location):
                        # append the comment data
                        comments = location['comments']
                        for comment in comments:
                                commented_by = comment['from']
                                if (commented_by['id'] == user_id):
                                        commentDetails.append({"user_id": user_id,"locationName": location['place']['name'],
                                              "comments": comment['message'], "post_id":location['post_id'], "location" : location['place']})


        return(postDetails,commentDetails)


#Function to analyse the sentiment of status and emojis
def extractPostStatusAndEmoji(postDetails):
        # preprocess the extracted status and split the status into words
        scored_status_emoji = []
        for item in postDetails:

                result = []
                hashresults = []
                userid = item['user_id']
                postid = item['post_id']
                location = item['location']
                messages = item['message']

                # Identify the hash words in status
                hashwords = re.compile(r'#[A-Z]{2,}(?![a-z])|[A-Z][a-z]+')
                hashwords_in_messages = hashwords.findall(messages)
                hashresult = ''

                # Correct the hash words
                for hashword in hashwords_in_messages:
                        hashresult += hashword + ' '

                # split both hash words and non hash words
                result = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",messages).split()
                hashresults = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",hashresult).split()

                # extract emoji
                emoji = re.findall(r'[^\w\s,]', messages)
                emoji_count = 0
                total_emoji_probability = 0
                for emo in emoji:
                        emoji_totalstatus = 0

                        emoji_list = emo.encode('unicode_escape')
                        emoji_listfinal = emoji_list.decode('utf-8').strip("\\\:\#\.")

                        # check the available emoji and get the probabilities
                        if emoji_listfinal == 'u2764':
                                emoji_count += 1
                                positive = 0.922
                                neutral = 0.049
                                negative = 0.03
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f602':
                                emoji_count += 1
                                positive = 0.608
                                neutral = 0.206
                                negative = 0.186
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u2665':
                                emoji_count += 1
                                positive = 0.336
                                neutral = 0.347
                                negative = 0.316
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f60d':
                                emoji_count += 1
                                positive = 0.902
                                neutral = 0.088
                                negative = 0.01
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f62d':
                                emoji_count += 1
                                positive = 0.373
                                neutral = 0.118
                                negative = 0.510
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f618':
                                emoji_count += 1
                                positive = 0.892
                                neutral = 0.089
                                negative = 0.02
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f60a':
                                emoji_count += 1
                                positive = 0.762
                                neutral = 0.198
                                negative = 0.03
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f44c':
                                emoji_count += 1
                                positive = 0.650
                                neutral = 0.270
                                negative = 0.08
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f44f':
                                emoji_count += 1
                                positive = 0.574
                                neutral = 0.317
                                negative = 0.109
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f629':
                                emoji_count += 1
                                positive = 0.161
                                neutral = 0.293
                                negative = 0.546
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f604':
                                emoji_count += 1
                                positive = 0.832
                                neutral = 0.129
                                negative = 0.04
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f603':
                                emoji_count += 1
                                positive = 0.784
                                neutral = 0.167
                                negative = 0.049
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus

                        elif emoji_listfinal == 'u1f61c':
                                emoji_count += 1
                                positive = 0.696
                                neutral = 0.255
                                negative = 0.049
                                emoji_totalstatus = positive - negative
                                total_emoji_probability += emoji_totalstatus


                countStatusWords = len(result)
                countHashStatusWords = len(hashresults)

                sumStatus = 0
                sumHashStatus = 0

                # perform the Vader sentiment analysis for the texts
                for wordresult in result:

                        sentiment_score = sid.polarity_scores(wordresult)
                        # for score in sorted(sentiment_score):
                        #         #print('{0}: {1}, '.format(score, sentiment_score[score]), end='')
                        compoundstatus = sentiment_score['compound']

                        if (compoundstatus == 0.0):
                                countStatusWords -= 1
                        sumStatus += compoundstatus

                if (countStatusWords == 0):
                        finalStatusCompound = 0
                else:
                        finalStatusCompound = (sumStatus / countStatusWords)

                # Perform Vader analysis for hash tag removed texts
                for wordhashresult in hashresults:

                        sentiment_score = sid.polarity_scores(wordhashresult)
                        # for score in sorted(sentiment_score):
                        #         #print('{0}: {1}, '.format(score, sentiment_score[score]), end='')
                        compoundhashstatus = sentiment_score['compound']

                        if (compoundhashstatus == 0.0):
                                countHashStatusWords -= 1
                        sumHashStatus += compoundhashstatus

                if (countHashStatusWords == 0):
                        finalHashStatusCompound = 0
                else:
                        finalHashStatusCompound = (sumHashStatus / countHashStatusWords)

                # Combine the text sentiment polarities of status with the emoji sentiment polarities of status
                emojiStatusProbability = total_emoji_probability

                if (emojiStatusProbability == 0):
                        finalStatusProbability = finalStatusCompound + finalHashStatusCompound
                else:
                        finalStatusProbability = (finalStatusCompound + finalHashStatusCompound) * emojiStatusProbability

                scored_status_emoji.append({"user_id":userid, "post_id":postid, "location":location, "final_status_probability":finalStatusProbability})
        return (scored_status_emoji)


def extractPostCommentsandEmoji(commentDetails):
        # preprocess the extracted comments and split the status into words
        scored_comments = []
        for item in commentDetails:

                comments = item['comments']
                comment_results = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",comments).split()

                comment_emoji = re.findall(r'[^\w\s,]', comments)
                userid = item['user_id']
                postid = item['post_id']

                # extract emoji
                emoji_count = 0
                total_emoji_probability = 0

                for commentemo in comment_emoji:

                        comment_emojilist = commentemo.encode('unicode_escape')
                        comment_emojilist_final = comment_emojilist.decode('utf-8').strip("\\\:\#\.")

                        # check the available emoji and get the probabilities
                        if comment_emojilist_final == 'u2764':
                                emoji_count += 1
                                positive = 0.922
                                neutral = 0.049
                                negative = 0.03
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total


                        elif comment_emojilist_final == 'u1f602':
                                emoji_count += 1
                                positive = 0.608
                                neutral = 0.206
                                negative = 0.186
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u2665':
                                emoji_count += 1
                                positive = 0.336
                                neutral = 0.347
                                negative = 0.316
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f60d':
                                emoji_count += 1
                                positive = 0.902
                                neutral = 0.088
                                negative = 0.01
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f62d':
                                emoji_count += 1
                                positive = 0.373
                                neutral = 0.118
                                negative = 0.510
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f618':
                                emoji_count += 1
                                positive = 0.892
                                neutral = 0.089
                                negative = 0.02
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f60a':
                                emoji_count += 1
                                positive = 0.762
                                neutral = 0.198
                                negative = 0.03
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f44c':

                                emoji_count += 1
                                positive = 0.650
                                neutral = 0.270
                                negative = 0.08
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f44f':
                                emoji_count += 1
                                positive = 0.574
                                neutral = 0.317
                                negative = 0.109
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f629':
                                emoji_count += 1
                                positive = 0.161
                                neutral = 0.293
                                negative = 0.546
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f604':
                                emoji_count += 1
                                positive = 0.832
                                neutral = 0.129
                                negative = 0.04
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f603':
                                emoji_count += 1
                                positive = 0.784
                                neutral = 0.167
                                negative = 0.049
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total

                        elif comment_emojilist_final == 'u1f61c':
                                emoji_count += 1
                                positive = 0.696
                                neutral = 0.255
                                negative = 0.049
                                emoji_total = positive - negative
                                total_emoji_probability += emoji_total


                sumComment = 0
                countWords = len(comment_results)

                # perform the Vader sentiment analysis for the texts in comments
                for word in comment_results:

                                sentiment_score = sid.polarity_scores(word)
                                # for score in sorted(sentiment_score):
                                #         format = print('{0}: {1}, '.format(score, sentiment_score[score]), end='')
                                compoundValue = sentiment_score['compound']

                                if(compoundValue == 0.0):
                                        countWords -= 1

                                sumComment += compoundValue

                if(countWords == 0):
                        finalCommentCompound = 0
                else:
                        finalCommentCompound = (sumComment/countWords)

                # Combine the text sentiment polarities of status with the emoji sentiment polarities of comments
                emojiCommentProbability = total_emoji_probability
                if(emojiCommentProbability == 0):
                        finalCommentProbability = finalCommentCompound
                else:
                        finalCommentProbability = finalCommentCompound * emojiCommentProbability

                scored_comments.append({ "user_id":userid, "post_id":postid, "final_comment_probability":finalCommentProbability })

        return scored_comments


def aggregateProbabilities(scored_comments,scored_status):
        postSet = []
        # combine and get the final probabilities in user status with the relevant user comments
        for status in scored_status:
                post_id = status['post_id']
                user_id = status['user_id']
                location = status['location']
                status_probability = status['final_status_probability']

                #Get the total comment sentiment
                total_comment_sentiment = 0
                for comment in scored_comments:
                        if (comment['post_id'] == post_id):
                                total_comment_sentiment += comment['final_comment_probability']

                if (status_probability == 0):
                        final_probability = total_comment_sentiment
                elif(total_comment_sentiment == 0):
                        final_probability = status_probability
                else:
                        final_probability = status_probability * total_comment_sentiment

                postSet.append({"post_id":post_id, "user_id":user_id, "location":location, "final_probability":final_probability})
        return postSet


def mapValues(aggregated_result):

        com_probability = []
        final_results = []
        database_result = {}
        #get all the combined probability values of user posts
        for post in aggregated_result:
                combined_probability = post['final_probability']
                com_probability.append(combined_probability)

        # Identify the maximun and minimum probabilties
        max_probability = max(com_probability)
        min_probability = min(com_probability)

        probability_difference = max_probability - min_probability

        # Identify the mapping ranges
        value1 = (probability_difference*0.0099) + min_probability
        value2 = (probability_difference*0.08663) + value1
        value3 = (probability_difference*0.26732) + value2
        value4 = (probability_difference*0.373762) + value3
        value5 = (probability_difference*0.26237) + value4

        for post in aggregated_result:
                combined_probability = post['final_probability']

                # Map the identified ranges with the 1-5 rating
                if (combined_probability == 0):
                        continue;

                if(combined_probability < value1):
                        location_rating = 1.0

                if (value1 < combined_probability <= value2):
                        location_rating = 2.0

                if (value2 < combined_probability <= value3):
                        location_rating = 3.0

                if (value3 < combined_probability <= value5):
                        location_rating = 4.0

                if (value5 < combined_probability):
                        location_rating = 5.0

                postId = post['post_id']
                userId = post['user_id']
                location = post['location']

                final_results.append({"post id": postId, "user id": userId, "location":location, "rating": location_rating })

        return final_results


def store_user_preferences(user_id):
        postDetails, commentDetails = extractPostDataForUser(user_id)
        scored_posts = extractPostStatusAndEmoji(postDetails)
        scored_comments = extractPostCommentsandEmoji(commentDetails)
        aggregated = aggregateProbabilities(scored_comments, scored_posts)
        final = mapValues(aggregated)
        prefs = []
        for item in final:
                query = db.locations.find_one({'name': item['location']['name']})
                google_id = query['id']
                obj = {
                        'name' : item['location']['name'],
                        'post_id' : item['post id'],
                        'rating' : float(item['rating']),
                        'place_id' : item['location']['id'],
                        'location' : {
                                'lat' : item['location']['location']['latitude'],
                                'lng' : item['location']['location']['longitude']
                        },
                        'google_place_id' : google_id
                }
                prefs.append(obj)

        user_object = {
                'user_id' : user_id,
                'prefs' : prefs
        }

        db.testing_one.insert(user_object)




