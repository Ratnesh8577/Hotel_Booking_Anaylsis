#!/usr/bin/env python
# coding: utf-8

# Data Analysis Project Steps:
# 1. Create a Problem Statement.
# 2. Identify the data you want to analyze.
# 3. Explore and Clean the data.
# 4. Analyze the data to get useful insights.
# 5. Present the data in terms of reports or dashboards using visualization.
# 

# Business Problem
# 
# In recent years, City Hotel and Resort Hotel have seen high cancellation rates. 
# Each hotel is now dealing with a number of issues as a result, including fewer 
# revenues and less than ideal hotel room use. Consequently, lowering cancellation 
# rates is both hotels primary goal in order to increase their efficiency in 
# generating revenue, and for us to offer thorough business advice to address this
# problem.
# 
# The analysis of hotel booking cancellations as well as other factors that have no 
# bearing on their business and yearly revenue generation are the main topics of 
# this report.

# Assumptions
# 
# 1. No unusual occurrences between 2015 and 2017 will have a substantial impact on the data used.
# 
# 2. The information is still current and can be used to analyze a hotel's possible plans in an efficient manner.
# 
# 3. There are no unanticipated negatives to the hotel employing any advised technique.
# 
# 4. The hotels are not currently using any of the suggested solutions
# 
# 5. The biggest factor affecting the effectiveness of earning income is booking cancellations.
# 
# 6. Cancellations result in vacant rooms for the booked length of time.
# 
# 7. Clients make hotel reservations the same year they make cancellations

# Research Question
# 
# 1. What are the variables that affect hotel reservation cancellations?
# 
# 2. How can we make hotel reservations cancellations better?
# 
# 3. How will hotels be assisted in making pricing and promotional decisions?

# Hypothesis
# 
# 1. More cancellations occur when prices are higher.
# 
# 2. When there is a longer waiting list, customers tend to cancel more frequently.
# 
# 3. The majority of clients are coming from offline travel agents to make their 
# reservations.

# #importing Libraries

# In[2]:


import pandas as pd # Data handle
import matplotlib.pyplot as plt #
import seaborn as sns
import warnings 
warnings.filterwarnings("ignore")


# #Loading the datasets

# In[3]:


df = pd.read_csv("/Users/ratneshchauhan/Downloads/Project/Hotel_bookings.csv")


# # Exploratory Data Analysis and Cleaning
# 

# In[6]:


df.head(10)


# In[7]:


df.tail(10)


# In[8]:


df.shape #Find the total (Row & Columns)


# In[9]:


df.columns


# In[10]:


df.info()


# In[11]:


# convert the date time (reservation_status_date )


# In[16]:


df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"], format="%d/%m/%Y")


# In[17]:


df.info()


# In[19]:


df.describe(include = "object") #Describe function use numerical only-include me object summary


# In[22]:


# object type columns so use for loop

for col in df.describe(include = "object").columns:
    print(col)
    print(df[col].unique())
    print("-"*50)
          
    


# # check missing value

# In[23]:


df.isnull().sum()


# # Drop the repeat value(agent,company  )

# In[24]:


df.drop(["company","agent"],axis = 1,inplace = True) #axis=1(columns changes)
df.dropna(inplace = True)


# In[25]:


df.isnull().sum()


# In[26]:


df.describe()


# In[27]:


# adr = rate of hotels


# In[29]:


df['adr'].plot(kind = "box")


# In[31]:


df = df[df["adr"]<5000]


# In[32]:


df.describe()


# # Data Analysis and Visualizations

# In[47]:


cancelled_perc = df["is_canceled"].value_counts(normalize = True)
# 0.628653 not cancelled
#0.371347  cancelled
cancelled_perc
print(cancelled_perc)
plt.figure(figsize = (5,4))
plt.title("Reservation Status Count")
plt.bar(["Not canceled","Canceled"],df["is_canceled"].value_counts(),edgecolor = "k",width = 0.7)
plt.show()


# In[50]:


plt.figure(figsize = (5,4))
ax1 = sns.countplot(x ="hotel",hue = "is_canceled",data = df,palette = "Blues")
legend_labels,_ = ax1.get_legend_handles_labels()
#ax1.legend(bbox_to_anchor(1,1))
plt.title("Reservation Status in Different Hotels",size = 20)
plt.xlabel("hotel")
plt.ylabel("number of reservations")
plt.show()


# The accompanying bar graph shows the percentage of reservations that are 
# canceled and those that are not. It is obvious that there are still a 
# significant number of reservations that have not been canceled. 
# There are still 37% of clients who canceled their reservation, 
# which has a significant impact on the hotels' earnings

# In[52]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)
#0.72025 not canceled


# In[54]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# In[55]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[56]:


plt.figure(figsize = (20,8))
plt.title("Average Daily Rate in City and Resort Hotel",fontsize =30)
plt.plot(resort_hotel.index,resort_hotel['adr'],label = "Resort Hotel")
plt.plot(city_hotel.index,city_hotel['adr'],label = "City Hotel")
plt.legend(fontsize = 20)
plt.show()


# In comparison to resort hotels, city hotels have more bookings.
# It's possible that resort hotels are more expensive than those in cities

# In[60]:


df['month'] =df['reservation_status_date'].dt.month
plt.figure(figsize = (16,8))
ax1=sns.countplot(x = 'month',hue = 'is_canceled',data = df,palette = 'bright')
#legend_label(bbox_to_anchor=(1,1))
plt.title("Reservation Status per Month",size = 20)
plt.xlabel("month")
plt.ylabel("number of reservations")
plt.legend(['not canceled','canceled'])
plt.show()
# blue(0)= not canceled
#(1)= canceled


# The line graph above shows that, on certain days, the average daily rate
#     for a city hotel is less than that of a resort hotel, and on other days,
# it is even less. It goes without saying that weekends at holidays may see a 
# rise in resort hotel rates

# In[66]:


plt.figure(figsize=(15, 8))
plt.title('ADR per month', fontsize=30)

# Fixing groupby and ensuring correct parameter names in sns.barplot
sns.barplot(
    x='month',
    y='adr',
    data=df[df['is_canceled'] == 1].groupby('month',as_index=False)[['adr']].sum()
,hue = 'month')

plt.legend(fontsize=20)
plt.show()


# We have developed the grouped bar graph to analyze the months with the
# highest and lowest reservation levels according to reservation status. 
# As can be seen, both the number of confirmed reservations and the number 
# of canceled reservations are largest in the month of August whereas January 
#  is the month with the most canceled reservations.

# In[68]:


cancelled_data = df [df['is_canceled'] == 1]
# canceled base at country
top_10_country= cancelled_data['country'].value_counts()[:10]

plt.figure(figsize = (8,8))

plt.title('Top 10 countries with reservation canceled')

plt.pie(top_10_country, autopct = '%.2f', labels = top_10_country.index)

plt.show()


# This bar graph demonstrates that cancellations are most common when prices 
# are greatest and are least common when they are lowest. Therefore, 
# the cost of the accommodation is solely responsible for the cancellation
# Now, let's see which country has the highest reservation canceled.
# The top country is Portugal with the highest number of cancellations
# 

# Let's check the area from where guests are visiting the hotels and making 
# reservations. Is it coming from Direct or Groups, Online or Offline 
# Travel Agents? Around 46% of the clients come from online travel agencies, 
# whereas 27% come from groups. Only 4% of clients book hotels directly by
# visiting them and making reservations.

# In[69]:


df['market_segment'].value_counts()
#TA =travel adjent


# In[70]:


df['market_segment'].value_counts(normalize = True)


# In[72]:


cancelled_data['market_segment'].value_counts(normalize = True)
#Maximum canceled by online


# In[83]:


cancelled_df_adr = cancelled_data.groupby('reservation_status_date') [['adr']].mean()

cancelled_df_adr.reset_index(inplace = True)

cancelled_df_adr.sort_values('reservation_status_date', inplace = True)
                            
not_cancelled_data =df[df['is_canceled'] == 0]

not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date') [['adr']].mean()

not_cancelled_df_adr.reset_index(inplace =  True)

not_cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

plt.figure(figsize = (20,6))

plt.title('Average Daily Rate')

plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label = 'not cancelled')

plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')

plt.legend()


# As seen in the graph, reservations are canceled when the average daily 
# rate is higher than when it is not canceled It clearly proves all the 
# above analysis, that the higher price leads to higher cancellation

# In[84]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016') & (cancelled_df_adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016') & (not_cancelled_df_adr['reservation_status_date']<'2017-09')]


# In[88]:


plt.figure(figsize = (20,6))

plt.title('Average Daily Rate',fontsize = 30)

plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label = 'not cancelled') 
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled') 
plt.legend(fontsize = 20)
plt.show()


# Suggestions
# 
# 1. Cancellation rates rise as the price does. In order to prevent 
#    cancellations of reservations, hotels could work on their pricing strategies
#    and try to lower the rates for specific hotels based on locations. 
#    They can also provide some discounts to the consumers.
# 
# 2. As the ratio of the cancellation and not cancellation of the resort hotel
#     is higher in the resort hotel than the city hotels. So the hotels 
#     should provide a reasonable discount on the room prices on weekends or 
#     on holidays.
# 
# 3. In the month of January, hotels can start campaigns or marketing with a
#     reasonable amount to increase their revenue as the cancellation is 
#     the highest in this month.
# 
# 4. They can also increase the quality of their hotels and their services 
#    mainly in Portugal to reduce the cancellation rate.

# In[90]:


df.to_csv("Data_Analysis_Hotel_Booking.csv", index=False)


# In[ ]:




