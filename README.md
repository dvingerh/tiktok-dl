# tiktok-dl

# NOTICE

**This script is not fully functional. You will have to acquire the following information through either packet sniffing with a rooted phone, emulator or some other method:**

- API Server Host (e.g. api-t.tiktok.com)
- device_id (e.g. 68062524349203849239)
- iid (e.g. 681418433854095829)

**As of recently this script will throw an error most of the time. Consider the code only useful as a base to work off.** 

![Version 1.0](https://img.shields.io/badge/Version-1.0-orange.svg)
![Python 2.7, 3.5](https://img.shields.io/badge/Python-2.7%2C%203.5%2B-3776ab.svg)

Python script to download videos from a TikTok profile without any watermarks. Supports Python 2.7 and 3.5.

Downloads will be saved to `downloaded/username`. Directories are automatically created if they don't exist yet.

### Requirements

This script requires the `requests` module to be installed.

### Usage

Download videos from profile with the following command:
`python tiktok-dl.py justinbieber`

##### Example terminal output

```
$ python3 tiktok-dl.py justinbieber                                                   
> User:    justinbieber                                                               
> SecUid:  MS4wLjABAAAAIDvnmw4IM9I6Jk7M0up6Fd4JC_OtGgVCwsy0vu51T9CGyxQwGLEmN_QZY1v2TYY
> Id:      6756702871704192005                                                        
> Videos:  32                                                                         
> Room Id: 0                                                                          
                                                                                      
> Getting page 1.                                                                     
                                                                                      
> Downloading new video 6812821765211917574.mp4 (1/32)                                
> Downloading new video 6812815870713220357.mp4 (2/32)                                
> Downloading new video 6812814770958257413.mp4 (3/32)                                
> Downloading new video 6812813216117296390.mp4 (4/32)                                
> Downloading new video 6812808886446230790.mp4 (5/32)                                
> Downloading new video 6810055635254660357.mp4 (6/32)                                
> Downloading new video 6808655310224411909.mp4 (7/32)                                
> Downloading new video 6808652575945035014.mp4 (8/32)                                
> Downloading new video 6808651710739926278.mp4 (9/32)                                
> Downloading new video 6808650981153328389.mp4 (10/32)                               
> Downloading new video 6808641590442200326.mp4 (11/32)                               
> Downloading new video 6808571208997686533.mp4 (12/32)                               
> Downloading new video 6808569761513966854.mp4 (13/32)                               
> Downloading new video 6808363388104740102.mp4 (14/32)                               
> Downloading new video 6807852937331723525.mp4 (15/32)                               
> Downloading new video 6807475852838784261.mp4 (16/32)                               
> Downloading new video 6806376811073735941.mp4 (17/32)                               
> Downloading new video 6805321224894385413.mp4 (18/32)                               
> Downloading new video 6795261949773876486.mp4 (19/32)                               
> Downloading new video 6795034946617511173.mp4 (20/32)                               
                                                                                      
> Getting page 2.                                                                     
                                                                                      
! Unexpected response by API endpoint, retrying (1).                                  
                                                                                      
> Getting page 2.                                                                     
                                                                                      
> Downloading new video 6794224096830917893.mp4 (21/32)                               
> Downloading new video 6780460113833528582.mp4 (22/32)                               
> Downloading new video 6780099674331270405.mp4 (23/32)                               
> Downloading new video 6780098336016862469.mp4 (24/32)                               
> Downloading new video 6780097123401682181.mp4 (25/32)                               
> Downloading new video 6780096407366847750.mp4 (26/32)                               
> Downloading new video 6779731367304449285.mp4 (27/32)                               
> Downloading new video 6779709221039574277.mp4 (28/32)                               
> Downloading new video 6779707075514666245.mp4 (29/32)                               
> Downloading new video 6777729787864599813.mp4 (30/32)                               
> Downloading new video 6777728217194286341.mp4 (31/32)                               
> Downloading new video 6777723295006592261.mp4 (32/32)                               
                                                                                      
> Finished downloading (32/32) videos.                                                
```
