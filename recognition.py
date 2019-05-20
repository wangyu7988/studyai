import boto3
import io
from PIL import Image


if __name__ == "__main__":

    client = boto3.client('rekognition')
    response = client.create_stream_processor(
        Input={
            'KinesisVideoStream': {
                'Arn': 'arn:aws:kinesisvideo:us-east-1:201247618887:stream/kvs1/1557896017573'
            }
        },
        Output={
            'KinesisDataStream': {
                'Arn': 'arn:aws:kinesis:us-east-1:201247618887:stream/kds1'
            }
        },
        Name='wangyucam',
        Settings={
            'FaceSearch': {
                'CollectionId': 'wangyu',
                'FaceMatchThreshold': 85.0
            }
        },
        RoleArn='arn:aws:iam::201247618887:role/rekrole'
    )

    print(response)

    bucket = 'rekognition-video-console-demo-iad-wangyu-q317min9lbx66vm1ejvh'
    collectionId = 'wangyu'
    fileName = 'test.jpeg'
    threshold = 70
    maxFaces = 2

    client = boto3.client('rekognition')


    response = client.search_faces_by_image(CollectionId=collectionId,
                                            Image={'S3Object': {'Bucket': bucket, 'Name': fileName}},
                                            FaceMatchThreshold=threshold,
                                            MaxFaces=maxFaces)

    faceMatches = response['FaceMatches']
    print('Matching faces')
    for match in faceMatches:
        print('FaceId:' + match['Face']['FaceId'])
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print("\n")




# Calculate positions from from estimated rotation
def ShowBoundingBoxPositions(imageHeight, imageWidth, box, rotation):
    left = 0
    top = 0

    if rotation == 'ROTATE_0':
        left = imageWidth * box['Left']
        top = imageHeight * box['Top']

    if rotation == 'ROTATE_90':
        left = imageHeight * (1 - (box['Top'] + box['Height']))
        top = imageWidth * box['Left']

    if rotation == 'ROTATE_180':
        left = imageWidth - (imageWidth * (box['Left'] + box['Width']))
        top = imageHeight * (1 - (box['Top'] + box['Height']))

    if rotation == 'ROTATE_270':
        left = imageHeight * box['Top']
        top = imageWidth * (1 - box['Left'] - box['Width'])

    print('Left: ' + '{0:.0f}'.format(left))
    print('Top: ' + '{0:.0f}'.format(top))
    print('Face Width: ' + "{0:.0f}".format(imageWidth * box['Width']))
    print('Face Height: ' + "{0:.0f}".format(imageHeight * box['Height']))

if __name__ == "__main__":
    photo = 'test2.jpeg'
    client = boto3.client('rekognition')

    # Get image width and height
    image = Image.open(open(photo, 'rb'))
    width, height = image.size

    print('Image information: ')
    print(photo)
    print('Image Height: ' + str(height))
    print('Image Width: ' + str(width))

    # call detect faces and show face age and placement
    # if found, preserve exif info
    stream = io.BytesIO()
    if 'exif' in image.info:
        exif = image.info['exif']
        image.save(stream, format=image.format, exif=exif)
    else:
        image.save(stream, format=image.format)
    image_binary = stream.getvalue()

    response = client.detect_faces(Image={'Bytes': image_binary}, Attributes=['ALL'])

    print('Detected faces for ' + photo)
    for faceDetail in response['FaceDetails']:
        print('Face:')
        if 'OrientationCorrection' in response:
            print('Orientation: ' + response['OrientationCorrection'])
            ShowBoundingBoxPositions(height, width, faceDetail['BoundingBox'], response['OrientationCorrection'])

        else:
            print('No estimated orientation. Check Exif data')

        print('The detected face is estimated to be between ' + str(faceDetail['AgeRange']['Low'])
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years')
        print(str(faceDetail))







