import boto3
import requests
from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response



ID = ""
SecretKey = ""



INPUT_BUCKET = "serverless-video-upload-jinesh"
region = "us-east-1"



app = Flask(__name__)



def download_video(video_url,title,v_format):
    try:
        res = requests.get(video_url,verify=False)
        if res.status_code != 200:
            print ("Error: to get video from {}".format(video_url))
            return False
        with open('{}.{}'.format(title,v_format),'wb') as vf:
            vf.write(res.content)
        return '{}.{}'.format(title, v_format)
    except:
        print("Exception:")


def upload_video_to_s3(video_file,title):
    data = open(video_file,'rb')
    s3 = boto3.client('s3',aws_access_key_id=ID,aws_secret_access_key=SecretKey)
    s3.put_object(Bucket=INPUT_BUCKET, Key=title, Body=data)



# aws_access_key_id=ACCESS_KEY,
#aws_secret_access_key=SECRET_KEY


@app.route('/', methods=['POST'])
@app.route('/share', methods=['POST'])
def post_to_s3():
    print(request.json)
    if not request.json or not 'videourl' or not 'title' in request.json:
        abort(400)
    video_url = request.json.get('videourl')
    video_title = request.json.get('title')
    video_format = video_url.split(".")[-1]
    v_file = download_video(video_url,video_title,video_format)

    if v_file:
        # After download video, Upload to the S3 bucket
        upload_video_to_s3(v_file, video_title)
        return make_response(jsonify({"Status": "Success"}, 201))
    else:
        return make_response(jsonify({"error":"Internal Server Error"}, 500))




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

