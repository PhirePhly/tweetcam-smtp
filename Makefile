install: tweetcam.py tweetcam.service
	install tweetcam.py /usr/local/bin/
	install tweetcam.service /lib/systemd/system/
	systemctl daemon-reload

enable: install
	systemctl enable tweetcam.service
	systemctl restart tweetcam.service
