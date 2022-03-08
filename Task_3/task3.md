# Task 3 Temporal Analysis

> Define a metric to capture one aspect of the pandemic. Calculate in Spark how the metric evolved over the weeks in the United States, the country most affected until November 2020.

In this task, I am going to analyze the trend of **users' sentiment towards stay-home** during the period covered by the dataset. I mean **stay-home** as the [global call](https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/steps-when-sick.html) for people to stay home except to get medical care during the coronavirus disease. Based on my observations and experiences, compared to eastern countries such as China and South Korea, western countries, especially the United States, have a larger voice against stay-home in society. To analyze Twitter users' sentiment towards stay-home, I decided to filter the tweets with stay-home related hashtags from the given dataset by the following code:

```python
tweet_home_df = all_json.filter(all_json.text.contains('stayhome' or 'stayhomestaysafe' or 'stayathome' or 'stayhomesavelives' or 'stayathomeandstaysafe' or 'workfromhome' or 'stayathomesavelives' or 'staysafestayhome' or 'workingfromhome' or 'healthyathome' or 'stayathomechallenge' or 'saferathome' or 'home' or 'homeoffice' or 'stayhomesavelifes' or 'oneworldtogetherathome' or 'homequarantine' or 'stayinghome'))
```

## Public Attention on Stay-home

After getting this subset of the tweets, I can estimate the trend in public attention on stay-home by tracking the number of tweets with stay-home related hashtags. The time series graph between the number of tweets with stay-home related hashtags and the date is shown below:

![1644524803571.png](image/task3/1644524803571.png)

However, we should be careful here because the high number of tweets in a particular day could be caused by the large total tweet number on that day. The graph of the total number of tweets with respect to the date is given by:
![1644524985584.png](image/task3/1644524985584.png)

Now, we can simply get the relative ratios of the tweets with stay-home related hashtags by diving the the number of tweets with stay-home related hashtags by the total number of tweets on each day. Here is the time series graph:
![1644525131844.png](image/task3/1644525131844.png)

## Public Sentiment Towards Stay-home

What to do next is to examine the public sentiment towards stay-home. Normally, sentiment analysis requires training a deep learning model using labelled data. However, since there is no such training data, I decided to use a open-source pre-training modeled from the [TextBlob](https://textblob.readthedocs.io/en/dev/) library. I implemented the sentiment analysis on the tweets text with stay-home related hashtags, which are categorized into three classes: positive, neutral, and negative. We can define the **metric** as **the percentage of tweets with different sentiments (positive, neutral, and negative)** by dividing the number of tweets with different sentiments (positive, neutral, and negative) by the number of tweets with stay-home related hashtags on each day. Here is the resulting time series graph:![1644525953133.png](image/task3/1644525953133.png)

## Notes on the CSV File

The resulting CSV file named `Task3.csv` is formatted as followed: a date following the ISO 8601 standard indicating a day, the value of percentage of positive tweets (named relative_pos) on that day, the value of percentage of neutral tweets (named relative_neu) on that day, and the value of percentage of negative tweets (named relative_neg) on that day.
