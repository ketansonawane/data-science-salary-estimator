import glassdoor_scraper as gs
import pandas as pd

path = "D:/Ken Jee Data Science/Data Science Salary Prediction Glassdoor/chromedriver"

df = gs.get_jobs('data scientist',1000, True, path, 20)

df.to_csv('glassdoor_jobs.csv', index = False)