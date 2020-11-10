
# Google Cloud - Video Intelligence

[![Google Cloud](https://www.gstatic.com/devrel-devsite/prod/v7cbba9dce83f2a54b727914bb06dd524b80e611a7d1fe33e121163235013f003/cloud/images/cloud-logo.svg)](https://cloud.google.com/video-intelligence)

Main goal of the task is to know the video analytics services offered by the Google Cloud, especially 
1. To know what are the type of services offered and its pro / cons
2. Try the simple demo 
3. Know which language is better 

#### To know what are the type of services offered and its pro / cons
Google Video Intelligence  provides 

1. **AutoML Video Intelligence**
AutoML Video Intelligence has a graphical interface that makes it easy to train your own custom models to classify and track objects within videos, *even if you have minimal machine learning experience.* It’s ideal for projects that require custom labels that aren’t covered by the pre-trained Video Intelligence API. 
- *pros* - easy customization, train the model to recogonize the uncaptured objects in the pretrained models
- *cons* - Requires minimum Machine learning knowledge, code maintanence in the server an extra resources are required
2. **Video Intelligence API**
Video Intelligence API has pre-trained machine learning models that automatically recognize a vast number of objects, places, and actions in stored and streaming video. Offering exceptional quality out of the box, it’s highly efficient for common use cases and improves over time as new concepts are introduced.
- *pros* - Dosn't require minimum Machine learning knowledge/experience, no extra code maintanence in the server, pretrainded models with better accuracy, easy use of an API
- *cons* - no customization of labels available, no way to train the model to recogonize the uncaptured objects in the pretrained models

## Benefits
- **Precise video analysis**
Video Intelligence API automatically recognizes more than 20,000 objects, places, and actions in stored and streaming video. It also distinguishes scene changes and extracts rich metadata at the video, shot, or frame level. Use in combination with AutoML Video Intelligence to create your own custom entity labels to categorize content.

- **Simplify media management**
Find value in vast archives by making media easily searchable and discoverable. Easily search your video catalog the same way you search text documents. Extract metadata that can be used to index, organize, and search your video content, as well as control and filter content for what’s most relevant.

- **Easily create intelligent video apps**
Gain insights from video in near real time using the streaming video annotation service and trigger events based on objects detected. Build engaging customer experiences with highlight reels, recommendations, interactive videos, and more.
 - **Automate expensive workflows**
Reduce time and costs associated with transcribing videos and generating closed captions, as well as flagging and filtering inappropriate content.

- **Process and store on Google Cloud**
Seamlessly integrate with Cloud Storage to easily store and upload videos to your model. Select the region where processing will take place and choose from any region where Google Cloud is available. Benefit from a consistent API, low-latency, and speed across multiple storage classes.

Advantages of GCP
1. Simple ways to access the API in the realtime
2. Advantage of using Google Storage 
3. Trigger object detection as events
4. Easy search and filter based on video meta data 
5. Auto captioning 
6. Room to introduce new ML models and labels

Disadvantages
1. No Face detection (beta phase)
2. Lack of person detection


### Demo with Video Intelligence API





