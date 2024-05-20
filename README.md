# Replicate Google Drive
## Content
1. Abstract
2. Setup Python Environment
3. Install the Google APIs client library for Python
4. Specifying project in Google Cloud Console
5. Authorize API requests (user authorization)
6. Running the Code
7. Future Scopes 
8. Bibliography

## Abstract
When you try and download multiple files, or a folder with multiple sub-folders and files, you'll see that Google Drive doesn't simply download all the files sequentially. It will first attempt to zip all the files, and then download the zip file. 

Here's the problem with this approach. When you have a LOT of files, or a big folder (with multiple sub-folders and files), the zipping takes a lot of time, and it often fails to zip altogether. 

So I created the program that (given a folder) downloads all the files in that folder, and then recursively goes into each sub-folder and downloads all the files in the consecutive sub-folder(s). 

## Setup Python Environment
Opening the terminal on Mac and typing python would tell you the version of python that is installed in your computer

<img width="567" alt="image" src="https://github.com/saatweek/replicate_gdrive/assets/43529908/292a002e-0f7d-4e31-b5a1-6fb4a1e80a10">

As you can see from the above image, I'm working with Python version 3.11.5

I need to assume that you already have a relatively recent version of python already installed in your laptop. I'm also assuming that you have pip already installed as well

## Install the Google APIs client library for Python

Assuming you just typed `python` in your terminal to check the version of your python installation, I know want you to exit out of that by typing `exit()` and then hitting the Enter button. We'll now use pip to install all the dependencies. So just type these commands in your terminal and execute each one of them
```
pip install -U pip google-api-python-client oauth2client
python3 -c "import googleapiclient, httplib2, oauth2client"
```

## Specifying project in Google Cloud Console

An application using Google APIs requires a project. Those are managed in the Google Cloud Developers Console or simply, "devconsole." In this project, we're only going to use the Google Drive API, so we have a magic link (below in Step 1) that:

 - Takes you to the devconsole
 - Walks you through creating a new project (or choosing an existing one), and
 - Automagically enables the Drive API

Let's do it!

 1. Navigate to [console.developers.google.com/start/api?id=drive](console.developers.google.com/start/api?id=drive) and login to your Google account.
 2. If you don't have any projects yet, you'll see this screen to accept the [Google APIs Terms of Service](https://console.developers.google.com/terms):

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/690da8d7-c5dc-450e-8bc8-a2b88c88abe7)

Once you accept the terms, a new project named "My Project" will be created, and the Drive API automatically enabled.

  3. If instead, you've already created a project, you'll get this screen instead:

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/20eef921-d93d-45ac-b15f-78f799ab8352)

When you click the **Create a project** pulldown, choose an existing project or really create a new project.

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/7bca7991-c9d8-480c-8275-c8fe2312fb9a)

Once you've made your selection (new or existing project), the Drive API will be automatically enabled for you. 

  4. You'll know the Drive API has been enabled with this confirmation:

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/54c22269-9f6c-4961-8182-fad3c13d2020)

  5. Click **Go to credentials** to move to the next step.

## Authorize API requests (user authorization)

To get OAuth2 credentials for user authorization, go back to the API manager and select the "Credentials" tab on the left-nav:

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/784a0ff3-06d2-490e-ad6c-f55bfdcf6001)

When you get there, you'll see all your credentials in three separate sections:

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/ff71d230-ad76-40ac-a5c2-c2aac68042ef)

The first is for API keys, the second OAuth 2.0 client IDs, and the last OAuth2 service accts—we're using the one in the middle.

From the Credentials page, click on the + Create Credentials button at the top, which then gives you a dialog where you'd choose "OAuth client ID:"

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/0688b0a3-94d2-44fa-b85f-032329b4f745)

On the next screen, you have 2 actions: configuring your app's authorization "consent screen" and choosing the application type:

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/9c707fc2-d176-46a9-b2e7-a5bc7510ab71)

If you have not set a consent screen, you will see the warning in the console and would need to do so now. (Skip this these next steps if your consent screen has already been setup.)

Click on "Configure consent screen" where you select an "External" app (or "Internal" if you're a Google Workspace [formerly "Google Workspace"] customer):

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/10f94bc0-6d71-4b88-837b-bb4c26a6339a)

It doesn't matter which you pick because you're not publishing your code sample. Most people will select "External" to be taken to a more complex screen, but you really only need to complete the "Application name" field at the top:

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/77de8258-d923-4f89-aca5-d2f443a5edcd)

The only thing you need at this time is just an application name so pick someone that reflects the codelab you're doing then click **Save**.

Now go back to the Credentials tab to create an OAuth2 client ID. Here you'll see a variety of OAuth client IDs you can create:

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/ce10dc73-7a1f-469c-866e-85d0445c4e99)

We're developing a command-line tool, which is **Other**, so choose that then click the **Create** button. Choose a client ID name reflecting the app you're creating or simply take the default name, which is usually, "Other client N".

 1. A dialog with the new credentials appears; click **OK** to close
    
![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/69853001-e14b-46a7-8620-edbcfe70563c)

 2. Back on the Credentials page, scroll down to the "OAuth2 Client IDs" section find and click the download icon ![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/b415df55-d197-4714-a2dd-7a292d993ef9) to the far right bottom of your newly-created client ID.
    
![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/d4b99c87-7b44-4c99-acab-0ad74a38aa71)

 3. This open a dialog to save a file named `client_secret-LONG-HASH-STRING.apps.googleusercontent.com.json`, likely to your **Downloads** folder. We recommend shortening to an easier name like `credentials.json` (which is what this app uses), then save it to the directory/folder where you'll be saving this `main.py` app

## Running the Code

Open the `main.py` python file. Simply scroll to the last line of code. You'll see the following function written : 

```
download_all_files_in_this_folder("12e1Ll_AOK_RyfgjVy8DiS7ckHrvOxrRa", "/Volumes/WD/HDD backup/")
```
As you probably notice, it takes 2 arguments :
 1. The first argument takes the `folder_id` of the google drive folder you want to replicate. How do you find the folder id? Simply open your Google Drive folder (that you want to replicate) in your browser and check the URL. So for example, if I want to replicate the folder "HDD backup" from my Google Drive to my system, I would open the "HDD Backup" folder on my browser and the folder id is the highlighted part of the link
    
<img width="661" alt="image" src="https://github.com/saatweek/replicate_gdrive/assets/43529908/5b120b7f-4224-4a09-aa02-596c57b7d2a4">

 2. The second argument is the path where you want to save all the components of the folder (in my case, I am saving it to my external HDD)

### IMPORTANT NOTE

The first time you execute the script, it won't have the authorization to access the user's files on Drive (yours). The command-line script is paused as a browser window opens and presents you with the OAuth2 permissions dialog:

![image](https://github.com/saatweek/replicate_gdrive/assets/43529908/235f6ad2-43d3-4271-92a3-f67234c1acbe)

This is where the application asks the user for the permissions the code is requesting (via the SCOPES variable). In this case, it's the ability to view the file metadata from the user's Google Drive. Yes, in your code, these permission scopes appear as URIs, but they're translated into the language specified by your locale in the OAuth2 flow dialog window. The user must give explicit authorization for the requested permission(s) requested, else the "run flow" part of the code will throw an exception, and the script does not proceed further.

THAT'S IT! After you've changed the arguments and authorized the program to use your Google Drive account, you should be able to run the program without any errors, and it will download everything present in that folder to whichever path you specified in the second argument. 

## Future Scopes 

Based on whatever ideas I got laying on my bed before sleeping, here are a few improvements I'm thinking I'll mnake sometime in the future:

  1. Implement multiprocessing for faster downloads
  2. Make this into a webapp which connects to your Google Drive Account and then saves everything using this program (to whichever folder to specify it to)
     
## Bibliography

  1. [Python Codelab](http://g.co/codelabs/gsuite-apis-intro)
  2. [Drive API Documentation](https://developers.google.com/drive/api/guides/manage-downloads)
