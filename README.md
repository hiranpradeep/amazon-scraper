# Amazon scraper

Amazon scraper using selenium

`out.json` contains the scraped result

## Time taken to run
- count: 100, time: 177.97274804115295
- count: 200, time: 354.79835414886475
- count: 300, time: 531.6713311672211
- count: 400, time: 679.279803276062
- count: 500, time: 830.731198310852
- count: 600, time: 1002.3870940208435
- count: 700, time: 1180.146145105362
- count: 800, time: 1333.9409341812134
- count: 900, time: 1489.7782871723175
- count: 1000, time: 1636.5317420959473

## Approach
- Used python csv reader to read the contents, and create a list of urls as described in the question.
- Used selenium to open a browser session
- A main for loop to iterate through each url, open it in the selenium browser and scrape the required data
- Went through some of the site elements (via inspect elements) and found id/classname/tags to find the required contents like product title, image url, price and details.
- Used json to dump data into out.json