# Real Estate Scouting Tool
By Kuchinpotta
***
Tool that helps Estate Brokers as:
  * Trace Location of Properties
  * Beautiful Colors for more enhancement
      * Red - Sold
      * Green - Available
***
Due to very deep use of columns names, if some uses another dataset, then there are two ways: 
1. Change the column names of the Code
2. Change the column names of the Dataset
***
### Property according to the map:
![Alt text](https://github.com/Krunal-Chandan/Real_Estate_Scouting_Tool/blob/main/ss/REST_img2.png)
### Details of the property:
![Alt text](https://github.com/Krunal-Chandan/Real_Estate_Scouting_Tool/blob/main/ss/REST_img1.png)
### Precise upto Plot No of Property
![image](https://github.com/user-attachments/assets/555f1d93-b1c1-445d-bda5-9f1c7311e367)

***
Wanna implement this, __*Real Estate Scouting Tool*__

To get started with the Real Estate Scouting Tool, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Krunal-Chandan/Real_Estate_Scouting_Tool
   ```
2. Run the application:
   ```bash
   python app.py
   ```

## Libraries Used

This application utilizes several powerful libraries:

- **os**: Provides a way to interact with the operating system, allowing us to read environment variables and manage file paths.
- **json**: Enables easy parsing and generation of JSON data, which is crucial for handling data from APIs and configuration files.
- **time**: Used for tracking time intervals, which can help in performance monitoring and scheduling tasks.
- **requests**: A popular library for making HTTP requests, allowing us to fetch real estate data from various APIs.
- **folium**: Facilitates the creation of interactive maps using Leaflet.js, perfect for visualizing real estate locations.
- **pandas**: A powerful data manipulation library that allows us to efficiently handle and analyze data in tabular form.
- **numpy**: Used for numerical operations, making it easier to perform calculations on data arrays.
- **folium.plugins.MarkerCluster**: Helps in managing a large number of markers on maps, providing a cleaner visualization by clustering nearby markers.
- **Flask**: A lightweight web framework for building web applications in Python, enabling us to create a user-friendly interface for our scouting tool.

With these libraries, the Real Estate Scouting Tool can fetch data, process it, and visualize it on interactive maps, making it an essential resource for real estate scouting.
