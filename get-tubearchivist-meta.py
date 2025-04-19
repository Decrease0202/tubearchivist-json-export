import os
from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import requests
from PIL import Image

#################################################
#recommended layout of .info.json file
#{
#  "id": "",
#  "channel_id": "",
#  "title": "",
#  "upload_date": "",
#  "description": null,
#  "categories": null,
#  "thumbnail": null,
#  "tags": null,
#  "view_count": null
#}
#################################################


##########################################################
### Set your file path!
### Example

# /data/media/emby/youtube 

rootfile = "" 

### Set your server!
### Example
# username: elastic
# password: password
# server: 192.168.0.10
# port:9200

# Elasticsearch(['http://elastic:password@192.168.0.10:9200'])


es = Elasticsearch()

##########################################################


for r, d, f, in os.walk(rootfile):
    
    for file in f:
        workingfile = os.path.join(r, file)
        jsonfile = workingfile.replace('.mp4', '.info.json')

        if workingfile.endswith('.mp4'):
            tubeid = workingfile.split('_', 1)[1][0:11]
        
        
            try:
                json = open(jsonfile)
                print("Matching JSON found for: " + tubeid)
            except:
                print("Missing JSON: " + tubeid)

                print("Searching Elastic...")
                search_query = {
                    "match": {
                    "youtube_id": tubeid
                    }
                }


                res = es.search(index="ta_video", query=search_query)


                for hit in res['hits']['hits']:

                    #create nfo file
                    filex = (hit["_source"]["media_url"]).split(".")
    
                    tree = ET.ElementTree("tree")

                    document = ET.Element("episodedetails")
                    n1 = ET.SubElement(document, "plot")
                    n1.text = hit["_source"]["description"]
                    n2 = ET.SubElement(document, "title")
                    n2.text = hit["_source"]["title"]
                    n3 = ET.SubElement(document, "aired")
                    n3.text = hit["_source"]["published"]
                    n4 = ET.SubElement(document, "youtubeid")
                    n4.text = hit["_source"]["youtube_id"]

                    tree._setroot(document)
                    tree.write(jsonfile, encoding = "UTF-8", xml_declaration = True)  
                    os.chmod(jsonfile, 0o777)
                    print("JSON added: " + jsonfile)

                    #get thumbnail
                    print("Get thumbnail...")
                    thumbnail = hit["_source"]["vid_thumb_url"]
                    thumbfilepng = workingfile.replace('.mp4', '.png')
                    thumbfilewebp = workingfile.replace('.mp4', '.webp')

                    thumbwebp = requests.get(thumbnail, allow_redirects=True)

                    #convert to png from webp
                    open(thumbfilewebp, 'wb').write(thumbwebp.content)
                    thumbpng = Image.open(thumbfilewebp).convert("RGB")
                    thumbpng.save(thumbfilepng)

                    #remove temp webp file
                    os.remove(thumbfilewebp)
