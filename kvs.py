import boto3
import datetime, time



def hoursago(howmanyhours):

    hoursago = (datetime.datetime.now() - datetime.timedelta(hours = howmanyhours))
    timeStamp = int(time.mktime(hoursago.timetuple()))

    return timeStamp

def getstreaminfo():
    kvs = boto3.client("kinesisvideo")
    response = kvs.list_streams()

    for i in range(len(response['StreamInfoList'])):

      streaminfo = response['StreamInfoList'][i]
      for key,value in streaminfo.items():
         print(key,':',value)
      streamname = streaminfo['StreamName']
      datapointinfo = kvs.get_data_endpoint(StreamName=streamname, APIName='GET_MEDIA')
      datapoint = datapointinfo['DataEndpoint']
      print(datapoint)


def getlivevideourl(STREAM_NAME):
    kvs = boto3.client("kinesisvideo")
    endpoint = kvs.get_data_endpoint(
        APIName="GET_HLS_STREAMING_SESSION_URL",
        StreamName=STREAM_NAME
    )['DataEndpoint']
    client = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)

    url = client.get_hls_streaming_session_url(
        StreamName=STREAM_NAME,
        PlaybackMode="LIVE"
    )['HLSStreamingSessionURL']

    return url


def getarchivevideourl(STREAM_NAME,howmanyhoursago):
    kvs = boto3.client("kinesisvideo")
    endpoint = kvs.get_data_endpoint(
        APIName="GET_HLS_STREAMING_SESSION_URL",
        StreamName=STREAM_NAME
    )['DataEndpoint']
    client = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)

    url = client.get_hls_streaming_session_url(
          StreamName=STREAM_NAME,
          PlaybackMode = 'ON_DEMAND',
          HLSFragmentSelector={
          'FragmentSelectorType': 'PRODUCER_TIMESTAMP',
          'TimestampRange': {
          'StartTimestamp': hoursago(howmanyhoursago),
          'EndTimestamp': hoursago(0)
           }
          }
          )['HLSStreamingSessionURL']
    return url



STREAM_NAME = "kvs1"


#得到当前用户所有kinesis video stream的信息
getstreaminfo()

#得到当前正在直播的视频流链接，token的默认期为5分钟

print(getlivevideourl(STREAM_NAME))


#得到过去几个小时的视频流链接，token的默认器为5分钟，传入的第二个参数为几个小时前
# print(getarchivevideourl(STREAM_NAME, 3))




#from IPython.display import HTML
#HTML(data='<video src="{0}" autoplay="autoplay" controls="controls" width="300" height="400"></video>'.format(url))



