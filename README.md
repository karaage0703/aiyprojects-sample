# aiyprojects-sample
google aiyprojects(Vision Kit/Voice Kit) sample code

# Setup
## common
Execute following command, you will clone this repository.
```sh
$ cd && git clone https://github.com/karaage0703/aiyprojects-sample
```

## simple cam
### Hardware
- Vision Kit

### Software
If you want to enable autostart, execute following commands:
```sh
$ sudo cp ~/aiyprojects-sample/service/simple_cam.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable simple_cam.service
```

## food diary
### Hardware
- Vision Kit

### Software
- Get slack token

```sh
$ sudo pip3 install slacker
```

### AIY Kit version
- food_diary.py AIY Kits Release 2018-04-13
- food_diary_20180803.py AIY Kits Release 2018-08-03
- simple_cam.py AIY Kits Release 2018-08-03


# Licence
This software is released under the Apache License, see LICENSE.


# References
https://github.com/google/aiyprojects-raspbian
