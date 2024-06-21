## Summary

### This repo will go over a data scraper example that fetches data from an existing car ads classified website. Given a link to the website page, the script will parse the page for a list of accessible URL's pertaining to each Car Ad. 
### Then it will scrape each of those ads for data on the car and insert it into a dictionary for easy consumption. 
### This script is inherited from a larger project called PriceMyCar, which is located directly at http://23.21.205.72/ (previously known as pricemycar.io). The repo has been privated ever since it was close sourced as of recent.

## Prefect.io
### The introduced of Prefect in this data workflow pipeline can be seen in /pricemycar_data_workflow/scraper-prefect.py. The orchestration framework provided by Prefect is a Python-native syntax that allows you to organize your code in a reusable, observable and monitorable, fail-safe manner.
### Decorated with a series of Flows and Tasks, it allowed me to organize my code, and further integrate it with out of the box integrations and connectors into popular tools like Slack (webhook events) and PagerDuty (for displaying records). 
### The point of the revamped 'PriceMyCar with Prefect' repo is to explore the capabilities of Prefect.io -- to understand the meaningfulness of Flows, Tasks, how units of execution are compiled, how failure modes can be foolproofed using a proper data flow orchestration tool among other wonderful features - like running flows from a remote repository!
