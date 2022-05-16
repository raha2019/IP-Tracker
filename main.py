import os
import pandas as pd
import plotly.express as px

import ipinfo
import requests

output_stream = os.popen('lsof -i | grep -E "(ESTABLISHED)"')
print("-------------------------------------------------------")

output = output_stream.read().splitlines()

final = []

for line in output:
    new_line = ' '.join(line.split())
    my_list = new_line.split(" ")
    temp = my_list[8].split("->")[1]
    my_list[8] = temp.split(":")[0]
    final.append(my_list)

df = pd.DataFrame(final, columns =['Name', 'Port', 'User', 'FD', 'Type', 'Device', 'size','Node', 'Connection', 'status' ])
print(df)

access_token = 'Your_TOKEN_HERE'
handler = ipinfo.getHandler(access_token)

# data
city = []
country = []
latitude = []
longitude = []


for index, row in df.iterrows():

    ip_address = row['Connection']

    try:
        details = handler.getDetails(ip_address)
        city.append(details.city)
        country.append(details.country)

        locations = details.loc.split(",")
        latitude.append(locations[0])
        longitude.append(locations[1])

    except requests.exceptions.HTTPError:
        print("Alternate IP")
        command = 'nslookup ' + ip_address
        command_output = os.popen(command)
        output = command_output.read().splitlines()
        print(output[5])
        address = output[5].split("Address: ")[1].replace(" ", "")
        print('------------------------------------------------')
        print(address)


        details = handler.getDetails(address)

        city.append(details.city)
        country.append(details.country)

        locations = details.loc.split(",")
        latitude.append(locations[0])
        longitude.append(locations[1])

df['city'] = city
df['country'] = country
df['latitude'] = latitude
df['longitude'] = longitude

print(df)

fig = px.scatter_geo(df,lat='latitude',lon='longitude', hover_name="city")
fig.update_layout(title = 'World map', title_x=0.5)
fig.show()