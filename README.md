# tweetcam-smtp
A Tweeting Camera which uses Email as its uplink

Depends on a locally running email MTA like Postfix running. Presumably it
will need a smarthost relay like Gmail to get the email out.

Depends on configparser 

```
sudo apt install python-pip
sudo pip install configparser
```

Watches for a negative edge on GPIO17 to trigger a picture.

GPIO27 is a heartbeat LED which shows that the daemon is running.

GPIO22 lights up when the picture is captured until its finished queuing the
email and ready to take another photo.

Blogpost with all design details coming.
