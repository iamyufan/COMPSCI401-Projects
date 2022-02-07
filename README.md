# COMPSCI401-Cloud-Computing
Personal repo of DKU course COMPSCI 401 Cloud Computing for SP22 term

*Course Description*
> This course covers cloud infrastructures, virtualization, distributed file system, software defined networks and storage, cloud storage, and programming models such as MapReduce and Spark
## Project 1 - Big Data Programming Paradigms
In this project, students will get experience with MapReduce, one of the earliest Big Data frameworks that have been adopted for use in cloud systems, and with Spark, one of the most popular successor alternatives to date.
### Task 1 Twitter Hashtag Popularities and Relations
Using MapReduce, in a single application, compute the popularity of each hashtag h and create a list of its correlated hashtags. The popularity is simply the number of tweets in which a hashtag h appears. A hashtag c is correlated with another hashtag h if c and h appear in the same tweet. Prepare a CSV file where the first column is a hashtag, the second column is the popularity of the hashtag, and the last column represents a list of all hashtags correlated with h. Sort tags in decreasing popularity, and break ties by sorting tags lexicographically.
### Task 2 User Popularity Increase
There are many celebrities and telecommunications services that use Twitter as a way to spread their information more quickly and attract more followers. Twitter currently uses a verification seal to validate the authenticity of these profiles. In this exercise, we'll use the dataset to evaluate if verified users have benefited from the pandemic to increase their number of followers.

In this sense, using Spark, identify the 1000 verified users (marked in column verified) that grew the most in the number of followers in the period covered by the dataset. Among these users, are there users who are also in the top 1000 most active users, that is, the 1000 users with the highest number of tweets?

Prepare a CSV file with three columns: a user's screen_name, that user's relative increase in the number of followers during the period, and a boolean (either 0 or 1) indicating whether that user is in the top 1000 most active users. Use the data in the CSV file to write a short paragraph discussing the evolution of the follower base of verified users during the pandemic.
### Task 3 Temporal Analysis
The moving average, also called rolling average, has been one of the main indicators used in the pandemic for several metrics, for example, the number of new cases per week and hospital occupation.

Define a metric to capture one aspect of the pandemic. Calculate in Spark how the metric evolved over the weeks in the United States, the country most affected until November 2020.
