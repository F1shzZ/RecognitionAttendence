import boto3
import botostubs
from botocore.exceptions import ClientError
from os import environ
from PIL import Image
client=boto3.client('rekognition') # type: botostubs.Rekognition

def ResizePhoto(inputFile,outputFile):
#	print("Input file is: ",inputFile)
#	print("Output file is: ",outputFile)

	# resize the photo
#	from PIL import Image

	basewidth=300

	imgInput=Image.open(inputFile)

	wpercent=(basewidth / float(imgInput.size[0]))

	hsize=int((float(imgInput.size[1]) * float(wpercent)))

	imgOutput=imgInput.resize((basewidth, hsize), Image.ANTIALIAS)

	imgOutput.save(outputFile)

	imgInput.close()
	imgOutput.close()


def DetectFaces(photoFile):
#	import boto3
#	client=boto3.client('rekognition')

	img=open(photoFile,'rb')

	response = client.detect_faces(Image={'Bytes': img.read()},Attributes=['ALL'])

	nFaces = 0
#	print('Detected faces for ' + photoFile)
	for faceDetail in response['FaceDetails']:
		nFaces = nFaces+1
#		print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
#			+ ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')

	img.close()

	return(nFaces)


def CompareFaces(sourceFile,targetFile):
#	print("Source file is: ",sourceFile)
#	print("Target file is: ",targetFile)

	threshold=90
#	import boto3
#	client=boto3.client('rekognition')

	imgSource=open(sourceFile,'rb')
	imgTarget=open(targetFile,'rb')

	response=client.compare_faces(SimilarityThreshold=threshold,
                               SourceImage={'Bytes': imgSource.read()},
        	               TargetImage={'Bytes': imgTarget.read()})

	confidence=[]
	for faceMatch in response['FaceMatches']:
		position = faceMatch['Face']['BoundingBox']
		confidence = str(faceMatch['Face']['Confidence'])
#		print('The face at ' +
#			str(position['Left']) + ' ' +
#			str(position['Top']) +
#			' matches with ' + confidence + '% confidence')

	imgSource.close()
	imgTarget.close()

	return(confidence)


def CreateCollection(collectionId):
#	import boto3
	maxResults=1
#	client=boto3.client('rekognition')

	#Create a collection
	print('Creating collection:' + collectionId)
	response=client.create_collection(CollectionId=collectionId)
	print('Collection ARN: ' + response['CollectionArn'])
	print('Status code: ' + str(response['StatusCode']))
	print('Done...')


def ListCollections():
#	import boto3
	maxResults=1
#	client=boto3.client('rekognition')

	#Display all the collections
#	print('Displaying collections...')
	response=client.list_collections(MaxResults=maxResults)
	
	collectionIds=[]
	while True:
		collections=response['CollectionIds']

		for collection in collections:
			collectionIds.append(collection)
#			print (collection)
		if 'NextToken' in response:
			nextToken=response['NextToken']
			response=client.list_collections(NextToken=nextToken,MaxResults=maxResults)
		else:
 			break

#	print('done...')

	return(collectionIds)


def DescribeCollection(collectionId):
#	import boto3
#	from botocore.exceptions import ClientError
#	from os import environ

	print('Attempting to describe collection ' + collectionId)
#	client=boto3.client('rekognition')

	try:
		response=client.describe_collection(CollectionId=collectionId)
		print("Collection Arn: "  + response['CollectionARN'])
		print("Face Count: "  + str(response['FaceCount']))
		print("Face Model Version: "  + response['FaceModelVersion'])
		print("Timestamp: "  + str(response['CreationTimestamp']))

	except ClientError as e:
		if e.response['Error']['Code'] == 'ResourceNotFoundException':
			print ('The collection ' + collectionId + ' was not found ')
		else:
			print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
	print('Done...')


def DeleteCollection(collectionId):
#	import boto3
#	from botocore.exceptions import ClientError
#	from os import environ

	print('Attempting to delete collection ' + collectionId)
	client=boto3.client('rekognition')
	statusCode=''
	try:
		response=client.delete_collection(CollectionId=collectionId)
		statusCode=response['StatusCode']

	except ClientError as e:
		if e.response['Error']['Code'] == 'ResourceNotFoundException':
			print ('The collection ' + collectionId + ' was not found ')
		else:
			print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
		statusCode=e.response['ResponseMetadata']['HTTPStatusCode']
	print('Operation returned Status Code: ' + str(statusCode))
	print('Done...')


def IndexFaces(collectionId,photoFile,name):
#	import boto3
	maxFaces=1
#	client=boto3.client('rekognition')
	
	img=open(photoFile,'rb')

	response=client.index_faces(CollectionId=collectionId,
				Image={'Bytes': img.read()},
				ExternalImageId=name,
				MaxFaces=maxFaces,
				QualityFilter="AUTO",
				DetectionAttributes=['ALL'])

	facesIds=[]

#	print('Results for ' + photoFile)
#	print('Faces indexed:')
	for faceRecord in response['FaceRecords']:
		facesIds.append(faceRecord['Face']['FaceId'])
#		print('  Face ID: ' + faceRecord['Face']['FaceId'])
#		print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

#	print('Faces not indexed:')
#	for unindexedFace in response['UnindexedFaces']:
#		print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
#		print(' Reasons:')
#		for reason in unindexedFace['Reasons']:
#			print('   ' + reason)

	img.close()

	return(facesIds)


def ListFaces(collectionId):
#	import boto3
	maxResults=1
	tokens=True
#	client=boto3.client('rekognition')

	response=client.list_faces(CollectionId=collectionId,
	MaxResults=maxResults)

	name=[]
	facesIds=[]

#	print('Faces in collection ' + collectionId)

	while tokens:
		faces=response['Faces']
		for face in faces:
			name.append(face['ExternalImageId'])
			facesIds.append(face['FaceId'])
#			print(face)
		if 'NextToken' in response:
			nextToken=response['NextToken']
			response=client.list_faces(CollectionId=collectionId,
					NextToken=nextToken,MaxResults=maxResults)
		else:
			tokens=False

	return(facesIds)


def DeleteFaces(collectionId,facesIds):
#	import boto3
#	client=boto3.client('rekognition')

	response=client.delete_faces(CollectionId=collectionId,
		FaceIds=facesIds)
	print(str(len(response['DeletedFaces'])) + ' faces deleted:')
	for faceId in response['DeletedFaces']:
		print(faceId)


def SearchFaces(collectionId,faceId):
#	import boto3
	threshold=90
	maxFaces=10
#	client=boto3.client('rekognition')

	response=client.search_faces(CollectionId=collectionId,
				FaceId=faceId,
				FaceMatchThreshold=threshold,
				MaxFaces=maxFaces)

	faceMatches=response['FaceMatches']

	name=[]
	facesIds=[]
#	print('Matching Faces')
	for match in faceMatches:
		name.append(match['Face']['ExternalImageId'])
		facesIds.append(match['Face']['FaceId'])
#		print('FaceId: ' + match['Face']['FaceId'])
#		print('ExternalImageId: ' + match['Face']['ExternalImageId'])
#		print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")

	return(name)


def SearchFacesByImage(collectionId,photoFile):
#	import boto3
	threshold=90
	maxFaces=10
#	client=boto3.client('rekognition')

	img=open(photoFile,'rb')

	response=client.search_faces_by_image(CollectionId=collectionId,
				Image={'Bytes': img.read()},
				FaceMatchThreshold=threshold,
				MaxFaces=maxFaces)

	faceMatches=response['FaceMatches']

	name=[]
	facesIds=[]
#	print('Faces matching the largest face in image from ' + photoFile)
	for match in faceMatches:
		name.append(match['Face']['ExternalImageId'])
		facesIds.append(match['Face']['FaceId'])
#		print('FaceId: ' + match['Face']['FaceId'])
#		print('ExternalImageId: ' + match['Face']['ExternalImageId'])
#		print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")

	img.close()

	return(name)


def SearchFacesIdsByImage(collectionId,photoFile):
#	import boto3
	threshold=90
	maxFaces=10
#	client=boto3.client('rekognition')

	img=open(photoFile,'rb')

	response=client.search_faces_by_image(CollectionId=collectionId,
				Image={'Bytes': img.read()},
				FaceMatchThreshold=threshold,
				MaxFaces=maxFaces)

	faceMatches=response['FaceMatches']

	name=[]
	facesIds=[]
#	print('Faces matching the largest face in image from ' + photoFile)
	for match in faceMatches:
		name.append(match['Face']['ExternalImageId'])
		facesIds.append(match['Face']['FaceId'])
#		print('FaceId: ' + match['Face']['FaceId'])
#		print('ExternalImageId: ' + match['Face']['ExternalImageId'])
#		print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")

	img.close()

	return(facesIds)


def SearchFacesByValidImage(collectionId,photoFile):
	nFaces=DetectFaces(photoFile)
	facesIds=[]
	if nFaces>0:
		facesIds=SearchFacesIdsByImage(collectionId,photoFile)

	return(facesIds)


def AddFacesWithoutDuplication(collectionId,photoFile,name):
	facesIds=SearchFacesByValidImage(collectionId,photoFile)
	if len(facesIds)==0:
		facesIds=IndexFaces(collectionId,photoFile,name)

	return(facesIds)


def DeleteFacesByImage(collectionId,photoFile):
	facesIds=SearchFacesByValidImage(collectionId,photoFile)
	if facesIds:
		DeleteFaces(collectionId,facesIds)

	return(facesIds)

