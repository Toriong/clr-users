I am trying to upload a file to the agora server so that I can reference it via its' url when a user sends a message to their peer. 

Here's how I structure the request that is sent to agora's server: 

`pathToFile = 'C:\Users\gtori\OneDrive\Desktop\messaging_hud\users\files\testFile.png'

headers = {'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW', 'Authorization': 'Bearer token'}

agoraUrl = https://a41.chat.agora.io/orgName/appName/chatfiles

res = requests.post(agoraUrl, { file:  pathToFile }, headers=headers) 
`

The response that I am getting from agora is a 400 error: 

`{'error': 'illegal_argument', 'exception': 'java.lang.IllegalArgumentException', 'timestamp': 1679064611494, 'duration': 0, 'error_description': 'file must be provided.'}  
fromServer:  {'msg': 'The file was not uploaded successfully to agora server.'}`

Even though the path to the file is valid. I get a `True` boolean when I test the validity of it by passing it in for `os.path.exists`. 

I'm following Agora's documentation linked here under "Upload a file": https://docs.agora.io/en/agora-chat/restful-api/message-management?platform=unity#upload-a-file
