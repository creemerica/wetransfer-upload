import os
import sys
import json
import requests
import mimetypes
import collections
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

class WeTransfer(object):

	chunksize = 5242880

	def __init__(self, channel="", api_url="https://www.wetransfer.com/api/v1/transfers", bitly_url=""):
		self.channel 	= channel
		self.api_url  	= api_url
		self.bitly_url	= bitly_url

	def start(self, files):
		mimetypes.init()
		try:
			transferId = self.getTransferId()
		
			if os.path.isfile(files):
				self.uploadFile(transferId, files)
			elif os.path.isdir(files):
				self.uploadDir(files, transferId)
			else:
				print("Not a file/directory : " + files)
			
			return self.finalizeTransfer(transferId, files)
		except:
			print ""
			if transferId:
				self.cancelTransfer(transferId)

	def getTransferId(self):
		transferId =  { 
			"channel"	:	self.channel, 
			"expire_in"	:   "3m",
			"from"		:   "",
			"message"	: 	"",
			"pw" 		: 	"",
			"to[]" 		:   "",
			"ttype" 	:  	"4",
			"utype" 	:  	"js"
		}

		request 	= requests.post(self.api_url, data=transferId)
		response 	= json.loads(request.content)

		return response["transfer_id"]

	def getFileObjectId(self, transferId, filename, filesize):
		fileObjectId =  { 
			"chunked"	: 	"true", 
			"direct"	:	"false",
			"filename"	:	filename,
			"filesize"	: 	filesize
		}

		request 	= requests.post((self.api_url + "/{0}/file_objects").format(transferId), data=fileObjectId)
		response 	= json.loads(request.content)

		return response

	def getChunkInfoForUpload(self, transferId, fileObjectId, chunkNumber, chunkSize=chunksize):
		dataChunk = { 
			"chunkNumber"	:	chunkNumber,
			"chunkSize" 	:  	chunkSize,
			"retries" 		: 	"0" 
		}

		request 	= requests.put((self.api_url + "/{0}/file_objects/{1}").format(transferId, fileObjectId), data=dataChunk)
		response 	= json.loads(request.content)

		return response

	def uploadFile(self, transferId, fileToUpload):
		with open(fileToUpload, 'rb') as f:
			fileMimeType 	= "application/octet-stream" 
			fileSize 		= os.path.getsize(fileToUpload)
			fileName 		= os.path.basename(fileToUpload)

			dataFileObjectId = self.getFileObjectId(transferId, fileName, fileSize)

			if dataFileObjectId.has_key("url"):
				self.uploadChunk(dataFileObjectId, fileName, f.read(fileSize), fileMimeType, 0, fileSize)
				self.finalizeChunks(transferId, dataFileObjectId["file_object_id"], 1)
			else:
				chunkNumber = 1
				
				for piece in self.readInChunks(f):
					chunkInfo = self.getChunkInfoForUpload(transferId, dataFileObjectId["file_object_id"], chunkNumber, sys.getsizeof(piece))
					self.uploadChunk(chunkInfo, fileName, piece, fileMimeType, chunkNumber-1, fileSize)
					chunkNumber = chunkNumber + 1

				self.finalizeChunks(transferId, dataFileObjectId["file_object_id"], chunkNumber - 1)

	def uploadDir(self, top, transferId):
		'''descend the directory tree rooted at top,
		   calling the upload function for each regular file'''

		for root, dirs, files in os.walk(top): 
			while len(dirs) > 0:  
				dirs.pop()  
			
			for name in files:
				self.uploadFile(transferId, os.path.abspath(os.path.join(root, name)))

	def uploadChunk(self, chunkInfo, filename, dataBin, fileType, chunkNumber, fileSize):
		url = chunkInfo["url"]
		
		dataChunkUpload = collections.OrderedDict()
		for k, v in chunkInfo["fields"].items():
			dataChunkUpload[k] = v

		dataChunkUpload["file"] = (filename, dataBin, fileType)
		
		e = MultipartEncoder(fields = dataChunkUpload)
		m = MultipartEncoderMonitor(e, self.createCallback(chunkNumber*self.chunksize, fileSize))

		request = requests.post(url, data=m, headers={'Content-Type': e.content_type})

	def finalizeChunks(self, transferId, fileObjectId, partCount):
		dataFinalizeChunk = {
			"finalize_chunked"  :	"true",
			"part_count"  		: 	partCount
		}

		request = requests.put((self.api_url + "/{0}/file_objects/{1}").format(transferId, fileObjectId), data=dataFinalizeChunk)

	def finalizeTransfer(self, transferId, fileDirectory):
		request 	= requests.put((self.api_url + "/{0}/finalize").format(transferId))
		response 	= json.loads(request.content)
		url 		= response["shortened_url"]

		if self.bitly_url:
			request 	= requests.get((self.bitly_url + "{0}").format(url))
			response 	= json.loads(request.content)
			url 		= response["data"]["url"]

		return url

	def cancelTransfer(self, transferId):
		request = requests.put((self.api_url + "/{0}/cancel").format(transferId))
		
	def drawProgressBar(self, percent, barLen=40):
		sys.stdout.write("\r")
		progress = ""
		for i in range(barLen):
			if i < int(barLen * percent):
				progress += "="
			else:
				progress += " "
		sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
		sys.stdout.flush()

	def createCallback(self, previousChunks, fileSize):
		def callback(monitor):
			self.drawProgressBar(float(previousChunks + monitor.bytes_read)/float(fileSize))
			pass

		return callback

	def readInChunks(self, file_object, chunk_size=chunksize):
		"""Lazy function (generator) to read a file piece by piece.
		Default chunk size: 5Mo."""
		while True:
			data = file_object.read(chunk_size)
			if not data:
				break
			yield data