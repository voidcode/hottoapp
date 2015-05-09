##HowToApp

This is the leadning-app created on Ubuntu Desktop 14.04

All courses is create in .md file. 

All courses are save in /home/your-user/.howtoapp-courses/ 

Try see (https://github.com/voidcode/.howtoapp-courses)

Each course has an multiple choice test/ exam.
The are create in json format, the file-ending is .test

You need to save course(.test + .md) in the /home/your-user/.howtoapp-courses/ folder

Below you can see screenshots an running HowToApp app

![CourseView](https://raw.githubusercontent.com/voidcode/howtoapp/master/PR/HowToApp_001.png)

![Exam](https://raw.githubusercontent.com/voidcode/howtoapp/master/PR/HowToApp_002.png)

![Coursebuilder](https://raw.githubusercontent.com/voidcode/howtoapp/master/PR/HowToApp_003.png)

#Install and run it
```
    cd /tmp && wget https://raw.githubusercontent.com/voidcode/howtoapp/master/install && gksudo install
```

#Just run it (after install)
```
    cd $HOME && ./run
```

All courses are save in /home/user/.howtoapp-courses/ 

Try see (https://github.com/voidcode/.howtoapp-courses)

#Or manual install and run
```
    sudo -i
    apt-get install git
    atp-get install pip
    pip install python-markdown
    cd /home/$USER/ && git clone https://github.com/voidcode/.howtoapp-courses.git
    cd /home/$USER/ && git clone git@github.com:voidcode/howtoapp.git
    cd howtoapp && chmod +x main.py &&
    ./run
```