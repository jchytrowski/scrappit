# scrappit
I wrote scrappit to declutter my saved-links on my reddit account, by downloading and unsaving specific categories of links, primarily image albums, gifs, and videos.

> scrappit.py [--Archive] [--Download] [--Both]


## Get an API key
You'll need your own API ID and Key to use this; [Get your own here.](https://www.reddit.com/prefs/apps). You can learn about the process [here.](https://github.com/reddit/reddit/wiki/OAuth2)

## Set environmental variables (I use .bashrc)
export REDDIT_USERNAME='Username'
export REDDIT_API_PASS='hunter2'
export REDDIT_API_ID='hunter22'

You could also set your reddit password here, but I prefer to use a prompt each time.

## Flags

###  --Archive
Create a pkl archive of saved links to ~/reddit_saved.dict ; I use this to store post IDs, and later iterate over during the download process. * WARNING * This will currently overwrite the file if it already exists.

###  --Download
Download the images, webms, gifs, and gifv's stored on reddituploads, imgur, and gfycat. * Warning * Posts are unsaved if the download succesfully completes.

### --Over18
Download adult content? The default is set to false.

