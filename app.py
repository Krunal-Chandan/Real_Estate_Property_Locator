import os, json, time, requests, folium
from functools import cache
import pandas as pd
import numpy as np
from folium.plugins import MarkerCluster
from flask import Flask, render_template

app = Flask(__name__)

df = pd.read_csv('Zillow_properties.csv')

@app.route('/')
def index():
    global df
    if os.path.exists('templates/property_map.html'):
        return render_template('property_map.html')
    else:
        df = df.dropna(subset=['longitude','latitude'])

        df['rentZestimate'] = pd.to_numeric(df['rentZestimate'], errors='coerce')
        df['zestimate'] = pd.to_numeric(df['zestimate'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        df['annual_rent'] = df['rentZestimate'] * 12
        df['gross_rental_yield'] = (df['annual_rent'] / df['zestimate']) * 100

        df['gross_rental-yield'] = df['gross_rental_yield'].replace([np.inf, -np.inf], np.nan)

        def getMarkerColor(grossYield, offMarket):
            if offMarket:
                return 'black'
            elif pd.isna(grossYield):
                return 'grey'
            elif grossYield < 5:
                return 'red'
            elif grossYield < 8:
                return 'orange'
            else:
                return 'green'

        mapCenter = [df['latitude'].mean(), df['longitude'].mean()]
        m = folium.Map(location=mapCenter, zoom_start=12)

        markerCluster = MarkerCluster().add_to(m)

        for idx, row in df.iterrows():
            price = row['price']
            address = row['address']
            bedrooms = row['bedrooms']
            bathrooms = row['bathrooms']
            livingArea = row['livingArea']
            grossYield = row['gross_rental_yield']
            zestimate = row['zestimate']
            rentZestimate = row['rentZestimate']
            propertyURL = row['url']
            zpid = row['zpid']

            if not pd.isna(row['price']):
                priceFormatted = f'${price:.2f}'
            else:
                priceFormatted = 'N/A'
            
            if not pd.isna(row['zestimate']):
                zestimateFormatted = f'${zestimate:.2f}'
            else:
                zestimateFormatted = 'N/A'
            
            if not pd.isna(row['rentZestimate']):
                rentZestimateFormatted = f'${rentZestimate:.2f}'
            else:
                rentZestimateFormatted = 'N/A'

            # if not pd.isna(row['grossYield']):
            #     grossYieldFormatted = f'${grossYield:.2f}'
            # else:
            #     grossYieldFormatted = 'N/A'

            bedrooms = int(bedrooms) if not pd.isna(bedrooms) else 'N/A'
            bathrooms = int(bathrooms) if not pd.isna(bathrooms) else 'N/A'
            livingArea = int(livingArea) if not pd.isna(livingArea) else 'N/A'

            addressDict = json.loads(address)
            streetAdress = addressDict['streetAddress']

            popupText = f"""
                <b>Address : </b> {streetAdress}<br>
                <b>Price : </b> {priceFormatted}<br>
                <b>Bedrooms : </b> {bedrooms}<br>
                <b>Bathrooms : </b> {bathrooms}<br>
                <b>Living Area : </b> {livingArea}<br>
                <b>Zestimate : </b> {zestimateFormatted}<br>
                <b>Rent Zestimate : </b> {rentZestimateFormatted}<br>
                <a href="{propertyURL}" target="_blank">
                <button id="button-{idx}" onclick="showLoadingAndRedirect({idx}, '{zpid})">Show Price History</button>
                <div id="loading-{idx}" style="display:none;">
                    <img src="https://upload.wikipedia.org/wikipedia/commons/3/3a/Gray_circles_rotate.gif" alt="loading..." width="50" height="50">
                </div>

                <script>
                    function showLoadingAndRedirect(idx, zpid){{
                        document.getElementById('button-' + idx).style.display='none';
                        document.getElementById('loading-'+ idx).style.display="block";
                        window.location.href = 'http://localhost:5000/priceHistory/' + zpid;
                    }}
                </script>
            """

            color = getMarkerColor(row['gross_rental_yield'], row['isOffMarket'])

            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(folium.IFrame(popupText, width=300, height=250)),
                icon=folium.Icon(color=color, icon='home', prefix='fa')
            ).add_to(markerCluster)

        m.save('templates/property_map.html')
        return render_template('property_map.html')

@app.route('/priceHistory/<int:zpid>')
@cache
def priceHistory(zpid):
    url = df[df.zpid == zpid].url.values[0]
    apiURL = "#"

    TOKEN = open('TOKEN', 'r').read()

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": 'application/json'
    }

    data = [{'url' : url}]

    response = requests.post(apiURL, headers=headers, json=data)
    snapshotID = response.json()['snapshotID']

    time.sleep(5)

    apiURL =  "#" # f"https://api.brightdata.com/datasets/v3/{snapshotID}?format=csv"

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(apiURL, headers=headers)

    if 'Snapshot is empty' in response.text:
        return 'No Historic Data'
    
    while 'Snapshot is not ready yet, try again in 10s' in response.text:
        time.sleep(10)
        response = requests.get(apiURL, headers=headers)
        if 'Snapshot is empty' in response.text:
            return 'No Historic Data'

    with open('temp.csv', 'wb') as f:
        f.write(response.content)

    priceHistoryDF = pd.read_csv('temp.csv')
    priceHistoryDF = priceHistoryDF[['date', 'price']]
    priceHistoryDF['date'] = pd.to_datetime(priceHistoryDF['date'])
    priceHistoryDF['date'] = priceHistoryDF['date'].dt.strftime('%Y-%m-%d')

    return render_template('priceHistory.html', priceHistoryDF=priceHistoryDF)


if __name__ == '__main__':
    app.run(debug=True) 

# New Real Estate Location Web page, for more real and accurate mapping of HOUSES, by Kuchinpotta
