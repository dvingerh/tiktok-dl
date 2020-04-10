import os
import time
import requests
import json
import random
import socket
import struct
import sys


class User(object):
	userId = None
	userName = None
	videoCount = None
	roomId = None

	def __init__(self, userId, secUid, userName, videoCount, roomId):
		self.userId = userId
		self.secUid = secUid
		self.userName = userName
		self.videoCount = videoCount
		self.roomId = roomId


class Video(object):
	awemeId = None
	url = None
	timestamp = None
	createTime = None
	author = None

	def __init__(self, awemeId, url, createTime, description, author):
		self.awemeId = awemeId
		self.url = url
		self.createTime = createTime
		self.description = description
		self.author = author

def generatePublicIp():
	return str(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))


def awemeRequest(request_path, type="get"):
	headers = {
		"User-Agent": "okhttp", "X-Forwarded-For": generatePublicIp()
	}
	url = "http://api-t.tiktok.com" \
		+ request_path \
		+ "&device_id=6806252436203849221" \
		+ "&iid=6806252686306150149" \
		+ "&version_code=100303" \
		+ "&build_number=10.3.3" \
		+ "&version_name=10.3.3" \
		+ "&aid=1233" \
		+ "&app_name=musical_ly" \
		+ "&app_language=en" \
		+ "&channel=googleplay" \
		+ "&device_platform=android" \
		+ "&device_brand=Google" \
		+ "&device_type=Pixel" \
		+ "&os_version=9.0.0"
	if type == "get":
		resp = requests.get(url, headers=headers)
	if type == "post":
		resp = requests.post(url, headers=headers)
	return resp


def awemeDownload(video):
	headers = {
		"User-Agent": "okhttp"
	}
	filepath = os.path.join("downloaded", video.author,
							(str(video.awemeId) + ".mp4"))
	if not os.path.isfile(filepath):
		resp = requests.get(video.url, headers=headers)
		if resp.status_code == 200:
			open(filepath, 'wb').write(resp.content)
			return True
	else:
		return False


def getUserByUsername(username, retry=1):
	try:
		endpoint = "/aweme/v1/discover/search/" \
			+ "?keyword=" + username \
			+ "&cursor=0" \
			+ "&count=10" \
			+ "&type=1" \
			+ "&hot_search=0" \
			+ "&search_source=discover"
		response = awemeRequest(endpoint, type="post").json()
		#open('user.json', 'w').write(json.dumps(response))
		for userObj in response.get("user_list"):
			userInfo = userObj.get("user_info")
			if (userInfo.get("unique_id") == username):
				userId = userInfo.get('uid')
				videoCount = userInfo.get('aweme_count')
				roomId = userInfo.get('room_id')
				secUid = userInfo.get('sec_uid')
				user = User(userId=userId, secUid=secUid, userName=username,
							videoCount=videoCount, roomId=roomId)
				return user
		print("> User not found, exiting.")
		sys.exit(0)
	except (TypeError, AttributeError):
		if retry < 4:
			print(
				"! Unexpected response by API endpoint, retrying ({:d}).".format(retry))
			print()
			time.sleep(0.5)
			retry += 1
			return getUserByUsername(username=username, retry=retry)
		else:
			print("! Maximum retries exceeded, exiting.")
			sys.exit(1)


def getUserVideos(uid, secUid, cursor=0, hasmore=True, page=1, count=0, total=0, retry=1):
	try:
		print("> Getting page {:d}.".format(page))
		print()
		endpoint = "/aweme/v1/aweme/post/?" \
			+ "user_id=" + uid \
			+ "&count=20" \
			+ "&max_cursor=" + str(cursor)
		response = awemeRequest(endpoint, type="get").json()
		#open('feed.json', 'w').write(json.dumps(response))
		hasmore = response.get('has_more', True)
		cursor = response.get("max_cursor", cursor)
		#open('videos.json', 'w').write(json.dumps(response))
		for videoObj in response.get("aweme_list"):
			awemeId = videoObj.get("aweme_id")
			url = videoObj.get("video").get("play_addr").get('url_list')[0]
			createTime = videoObj.get("create_time")
			description = videoObj.get("desc")
			userName = videoObj.get("author").get('unique_id')
			video = Video(awemeId=awemeId, url=url, createTime=createTime,
						  description=description, author=userName)
			count += 1
			if awemeDownload(video=video):
				print(
					"> Downloading new video {:s}.mp4 ({:d}/{:d})".format(video.awemeId, count, total))
			else:
				print(
					"! Skipped existing file {:s}.mp4 ({:d}/{:d})".format(video.awemeId, count, total))
		if hasmore:
			print()
			page += 1
			getUserVideos(uid=uid, secUid=secUid, cursor=cursor, hasmore=hasmore,
						  page=page, count=count, total=total, retry=1)
		else:
			print()
			print(
				"> Finished downloading ({:d}/{:d}) videos.".format(count, total))
			if count < total:
				print("! {:d} videos are missing, they are either private or have\n! otherwise not been returned by TikTok's API for unknown reasons.".format(
					(total-count)))
	except (TypeError, AttributeError):
		if retry <= 4:
			print(
				"! Unexpected response by API endpoint, retrying ({:d}).".format(retry))
			print()
			time.sleep(0.5)
			retry += 1
			getUserVideos(uid=uid, secUid=secUid, cursor=cursor,
						  hasmore=hasmore, page=page, count=count, total=total, retry=retry)
		else:
			print("! Maximum retries exceeded, exiting.")
			sys.exit(1)
	except KeyboardInterrupt:
		print()
		print("! Downloading was cancelled by the user, exiting.")
		sys.exit(0)


def ensureDownloadDir(user):
	path = os.path.join(os.getcwd(), "downloaded", user)
	if not os.path.exists(path):
		os.makedirs(path)

def main():
	try:
		usernameToDownload = sys.argv[1]
	except IndexError:
		print("> No username argument was given, exiting.")
		sys.exit(1)

	if usernameToDownload:
		user = getUserByUsername(username=usernameToDownload, retry=1)
		if user:
			print("> User:    {:s}".format(user.userName))
			print("> SecUid:  {:s}".format(user.secUid))
			print("> Id:      {:s}".format(user.userId))
			print("> Videos:  {:d}".format(user.videoCount))
			print("> Room Id: {:d}".format(user.roomId))
			print("")
			ensureDownloadDir(user=user.userName)
			getUserVideos(uid=user.userId, secUid=user.secUid, cursor=0, hasmore=True,
						  page=1, count=0, total=user.videoCount, retry=1)
		else:
			print("> No user object received, exiting.")


if __name__ == "__main__":
	main()
