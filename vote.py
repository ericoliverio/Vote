import requests
import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np

url = 'https://elections.erie.gov/Early-Voting'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]

df['Address'] = df[1] +' '+ df[2]+' '+df[3]+' '+df[4].astype(str)

df_a = df['Address']

geolocator = Nominatim(user_agent="vote_app")
df_coor = []

for i in df_a:
    #print(i)
    
    location = geolocator.geocode(i)
    
    if location is None:
        #print('Error: '+str(i))
        #print('')
        df_coor.append([0,0])
    else:
        #print(location.address)
        #error for 1 Town Hall Place Clarence NY 14031
        df_coor.append((location.latitude, location.longitude))
        #print('')

df2 = pd.DataFrame(np.array(df_coor), columns=['lat', 'long'])

df_concat = pd.concat([df, df2], axis=1)

df_concat.rename(columns={0: "Name"},inplace=True)
df_concat.drop([1, 2,3,4], axis=1,inplace=True)

df_concat.to_csv('vote.csv',index=False)