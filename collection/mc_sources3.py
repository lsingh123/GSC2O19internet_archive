#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:00:17 2019

@author: lavanyasingh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:21:42 2019

@author: lavanyasingh
"""

import mediacloud.api
import csv
import os

os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data')


key = '6e5564bc0c07edb1c307a8a7a34adbcb19a6d27c3d202987a1426a9066341308'
mc = mediacloud.api.MediaCloud(key)
country_id = 1935

#get a list of tags within a tag_sets_id
#returns dict in Country:tag_id format
def get_by_id(id):
    last_proc_tag = 0
    items = {}
    while True : 
        fetched = mc.tagList(tag_sets_id = 1935, last_tags_id = last_proc_tag, rows = 100)
        for tag in fetched:
            items[tag['label']] = tag['tags_id']
        if len(fetched) < 100: break 
        last_proc_tag = fetched[-1]['tags_id']
    return items

#get list of all media sources and write to a csv
#columns: country, url, title, language, type
def get_media():
    countries = get_by_id(country_id)
    with open('mc_sources_meta.csv', mode = 'w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        for country in countries:
            last_proc_id = 0
            while True:
                fetched = mc.mediaList(tags_id = countries[country], rows = 100, 
                                       last_media_id = last_proc_id)
                for item in fetched:
                    #each item will definitely have a title and url
                    title = item['name']
                    url = item['url']
                    #items may or may not have languages and types
                    #so we check for Nonetypes to avoid a type error
                    lang, t = None, None
                    if item['metadata']['language'] != None: lang = item['metadata']['language']['label']
                    if item['metadata']['media_type'] != None: t = item['metadata']['media_type']['label']
                    print(url)
                    w.writerow([country, url, title, lang, t])
                if len(fetched) < 100: break
                last_proc_id = fetched[-1]['media_id']

#write all mc sources to a csv
def get_all_countries():
    media = get_media()
    with open('mc_sources_meta.csv', mode = 'w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        for source in media:
            w.writerow([source['country'], source['url'], source['title'], 
                        source['language'], source['type']])
              
#run this line to store all the mc sources to a csv sorted by country
if __name__ == '__main__':
    get_media()    
   

        
    
        
