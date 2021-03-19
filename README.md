
![image](/project.png)
**Created By: Scott Bernstein (@_scottbernstein) & John Jackson (@johnjhacking)**
----------------------------------------------------------------------------------
# URLFlayer
This script was created to help Bug Bounty Hunters discover important URLs quickly, without the burden of having to manually run enumeration per URL and sort out all of the desired paths and response codes. All you need is to know what path you're interested in looking for, and utilize the script to test for it. The idea was to save time if you have to test a ton of subdomains in a Bug Bounty Program, especially if there's a specific piece of technology that you're looking for.
# Installing the script:
```
git clone http://x.x.x.x
```
# Installing the requirements:
```
pip3 install aiohttp
```
# Using the Script
```
optional arguments:
  -h, --help            show this help message and exit
  --pattern             matches code within a request
  -s, --success         Only show 200 status codes
  -p PATH, --path PATH
  -t TIMEOUT, --timeout TIMEOUT
Required Arguments:
  FILE, feed it a URL list
  ```
# Examples
**Pull up the help menu**
```
python3 url-flayer.py -h
```
**Checking all URLs in a file for the /login path**
```
python3 url-flayer.py urls.txt -p /login 
```
**Checking all URLs in a file for the /admin path and displaying 200 Response Codes only**
```
python3 url-flayer.py urls.txt -p /admin --success
```
**Checking all URLs in a file for a path and creating timeout rules**
```
python3 url-flayer.py urls.txt -p /moodle/moodle/Gruntfile.js -t 5000
```
**Checking all URLs in a file for a path, suppressing errors, and outputing it into a file**
```
python3 url-flayer.py urls.txt -p /admin/something --noerror > foo.txt
```
**Real example**
```
python3 url-flayer.py urls.txt -p /carbon/admin --success --noerror --pattern ADMIN > foo.txt
```
Hope you enjoy the tool! Happy hunting!
