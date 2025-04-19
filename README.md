# Get-TubeArchivist-JSON

Simple python script to extract the json that [TubeArchivist](https://github.com/bbilly1/tubearchivist) stores in Elastic.

My use case is keep meta data ready for manual import to another system. After having had the elastic search index becoming corrupted multiple times, and once being unable to recover the index. I wanted a way of being able to re-import files that arent able to be done using the system rescan.

Tube archivist is built with a manual file import feature. But the file needs to have its video ID and still be available on youtube to be able to import. If the video is no longer available, age restricted, or privetized, it wont be able to import without a seperate json file with the needed data. The goal is to prepare all videos in my archive with a json so it could be imported into another system. 

Thank you to [bbilly1](https://github.com/bbilly1) for all the great work on TubeArchivist. 

Usage:
configure your path and server and run. it will scan the path for files, pull the youtubeid out and search elastic for the metadata and write it a file matching the video file name. 
