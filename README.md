# Scrape-Data
Scrape Data from Grocery Portals

This is part of my project Vegetable Price Comparison Website -
1. Currently the data is being fetched from Big Basket, AtCost & JioMart.
2. The code selects the name, quantity & price of each item and stores it in a CSV file.
3. The data is fetched from multiple pages dynamically. If a portal has 5 pages of vegetable items today which increases to a total of 7 pages after a week, then   this code will automatically scrape data from all the 7 pages.
4. The data is cleaned before inserting into the CSV file. 
    For eg - a) cleaning the &nbsp; spaces 
             b) extracting the quantity out of the name field using regex
