import pandas as pd
import numpy as np
import re

#My one function purging extraneous information from scores
def numbers_only(score):
      regexp=re.compile(r'\([^)]*\)') #Needed because there were digits in Overtime annotation.
      score=regexp.sub("",score)
      temp=filter(str.isdigit,score)
      return "".join(temp)

#Read the second table on the web page
data=pd.read_html('https://en.wikipedia.org/wiki/NBA_All-Star_Game')[2]
df=pd.DataFrame (data)
df1=df.dropna(how='any')
df1=df1.drop(columns=['Host arena','Game MVP'] )

#The result column: seems odd it should be an attribute. Is 'Result' a key word or something special? I need to read more.
df1[['East', 'West']]=df1.Result.str.split(',', expand=True)
#The three series: east, west, and host city
sereast=pd.Series(df1['East'])
serwest=pd.Series(df1['West'])
sercity=pd.Series(df1['Host city'])

#Purge state names and get differences
index=0
score_difference=[]
for itemE in sereast:
      if 'West' in itemE:
            temp=serwest[index]
            serwest[index]=itemE
            sereast[index]=temp
      serwest[index]=numbers_only(serwest[index])
      sereast[index]=numbers_only(sereast[index])
      if len(serwest[index])!=0 and len(sereast[index])!=0:
            score_difference.append(int(abs(int(serwest[index])-int(sereast[index]))))
      else:
            score_difference.append(None)
      #Indices are the same so we can add this to the same loop
      citysplit=str(sercity[index]).split(',') #Remove the state
      sercity[index]=citysplit[0]
      index+=1

df1['Difference']=score_difference

#Printing the frequency of the differences
score_group=df1.groupby('Difference')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#Unsure why the column titles aren't here so I'm adding them
print("Difference...Frequency ")
print(df1['Difference'].value_counts())



#THe grand kluge. Create a column of booleans showing if a city has appeared more than once....
city_group=df1.groupby('Host city')

mult_cities=[]#i.e. cities with multiple games
for city in city_group["Host city"]:
      if str(city[1]).count(str(city[0]))>1:
            mult_cities.append(city[0])

allowed=[]
for city in df1["Host city"]:
      allowed.append(city in mult_cities) #Boolean value: tag for multiple appearances
#Add the allowed column to the dataframe and then filter out rows not allowed
df1["allowed"]=allowed
df2=df1[df1["allowed"]]
df2=df2.dropna(how='any')#Get rid of the cancelled one
df2=df2.drop(columns=['allowed'] )
df2.rename(columns={'Difference':'Average Difference'},inplace=True)
mean_group=df2.groupby('Host city').mean()

print(mean_group)