# scrappit
{to download media and unsave reddit links}

## Get an API key
You'll need your own API to use this; [Get your own.](https://www.reddit.com/prefs/apps). You can learn about the process [here.](https://github.com/reddit/reddit/wiki/OAuth2)


## Flags

###  --Archive
Create a pkl archive of saved links @ ~/reddit_saved.dict ; I use this to store post IDs, and later iterate over during the download process. * WARNING * This will currently overwrite the file if it already exists.

###  --Download
Download the images, webms, gifs, and gifv's stored on reddituploads, imgur, and gfycat. * Warning * Posts are unsaved if the download succesfully completes.

### --Over18
Download adult content? The default is set to false.

