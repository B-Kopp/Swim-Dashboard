import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

wd = webdriver.Chrome()

events = ['50 1 1', '50 1 2', '50 1 3', '100 1 1', '100 1 2', '100 1 3', '200 1 1', '200 1 2', '200 1 3', '500 1 1',
          '400 1 2', '400 1 3', '1000 1 1', '800 1 2', '800 1 3', '1650 1 1', '1500 1 2', '1500 1 3', '100 2 1', 
          '100 2 2', '100 2 3', '200 2 1', '200 2 2', '200 2 3', '100 3 1', '100 3 2', '100 3 3', '200 3 1', '200 3 2',
          '200 3 3', '100 4 1', '100 4 2', '100 4 3', '200 4 1', '200 4 2', '200 4 3', '200 5 1', '200 5 2', '200 5 3',
          '400 5 1', '400 5 2', '400 5 3']

columns=['EventDesc','FullName', 'SwimTime','Age','AltAdjSwimTime','LSC','TeamName','MeetName','StandardName']
df = pd.DataFrame(columns=columns)

for year in range(8):
    print("Year: "+ str(year+2012))
    for age in range(11):
        print("Age: " + str(age+15))
        for e in events:
            print("Event: " + e)
            dist, stroke, course = e.split()
            wd.get('https://www.usaswimming.org/times/event-rank-search')
            try:
                WebDriverWait(wd, 15).until(lambda wd: wd.execute_script('return jQuery.active') == 0)
                WebDriverWait(wd, 15).until(lambda wd: wd.execute_script('return document.readyState') == 'complete')
            except Exception:
                print("Loading took too much time!")
            comp_year_script = "$(\'#Times_EventRankSearch_Index_Div_1ddlDateRanges\').data(\'kendoDropDownList\').value(\'" + str(year+17) + "\')"
            wd.execute_script(comp_year_script)
            dist_script = "$(\'#Times_EventRankSearch_Index_Div_1cboDistance\').data(\'kendoDropDownList\').value(\'" + dist + "\')"
            wd.execute_script(dist_script)
            stroke_script = "$(\'#Times_EventRankSearch_Index_Div_1cboStroke\').data(\'kendoDropDownList\').value(\'" + stroke + "\')"
            wd.execute_script(stroke_script)
            course_script = "$(\'#Times_EventRankSearch_Index_Div_1cboCourse\').data(\'kendoDropDownList\').value(\'" + course + "\')"
            wd.execute_script(course_script)
            standard_script = '$(\'#Times_EventRankSearch_Index_Div_1ddlStandards\').data(\'kendoDropDownList\').value(\'11\')'
            wd.execute_script(standard_script)
            start_age_script = "$(\'#Times_EventRankSearch_Index_Div_1ddlStartAge\').data(\'kendoDropDownList\').value(\'" + str(age+15) + "\')"
            wd.execute_script(start_age_script)
            end_age_script = "$(\'#Times_EventRankSearch_Index_Div_1ddlEndAge\').data(\'kendoDropDownList\').value(\'" + str(age+15) + "\')"
            wd.execute_script(end_age_script)
            only_members_script = '$(\'#Times_EventRankSearch_Index_Div_1ddlIncludedMembers\').data(\'kendoDropDownList\').value(\'No\')'
            wd.execute_script(only_members_script)
            wd.execute_script("document.getElementById('MaxResults').value = 4000;")
            radio = wd.find_element_by_id("SelectedGender_Female")
            wd.execute_script("arguments[0].click();", radio)
            time.sleep(2.0)
            button = wd.find_element_by_id("saveButton")
            wd.execute_script("arguments[0].click();", button)
            try:
                WebDriverWait(wd, 15).until(lambda wd: wd.execute_script('return jQuery.active') == 0)
                WebDriverWait(wd, 15).until(lambda wd: wd.execute_script('return document.readyState') == 'complete')
            except Exception:
                print('Skipped: ' + str(e))
            try:
                data = pd.read_html(wd.page_source)
                df2 = data[0][1].str.extract(r'^(\d+) - (.+) (\d*:?\d+.\d+).*?Age: (\d+) Alt Adj: (\d*:?\d+.\d+) LSC: (\D+) Team: (.*?(?= 2)|.*?) (20.*|.*) Cut: (.+) PROG\. INDIV\. RELAY$').drop(0,axis=1)
                df2.insert(0, 'EventDesc', e)
                df2.columns = columns
                df = pd.concat([df,df2])
            except ValueError:
                pass
            print(df.shape)

df.sample(5)

df.to_csv('women.csv', index=False)