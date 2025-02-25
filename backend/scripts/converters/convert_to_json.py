import json

theses = [
    {
        "author": "Ambrus Barna",
        "year": 2023,
        "abstract": (
            "This paper describes in detail a system and its architecture for managing direction change and braking signals on scooters and bicycle s, using a sensor with an accelerometer and gyroscope on the back of the hand. The project aims to provide a solution for direction signals on the crank without removing the hand from the handlebars, thus avoiding the resulting accidents. The user is able to indicate a change of direction by gestures such as turning the hand sideways, so that it is not necessary to take the hand completely off the steering wheel, thus maintaining the balance of the vehicle. Brake signals are automatic as a result of acceler ation sensing. The system uses two microcontrollers (ESP32 and ESP8266), one of which processes the sensor data, while the other runs a web server and lights the corresponding LEDs. The web server is responsible for the communication between the microcontr ollers and also runs a web page that acts as a user interface. On the web page, active signals such as turn signals and brake signals are displayed and can be switched on and off. Communication between the different components is wireless using WiFi techno logy."
        ),
        "keywords": ["microcontroller", "WiFi", "gyroscope", "accelerometer"]
    },
    {
        "author": "Bacs Bernat",
        "year": 2023,
        "abstract": (
            "This thesis presents the implementation of a smart home control system. The system mainly performs home automation tasks such as temperature control, watering of plants and automatic movement of shutter , thus facilitating the user's daily life. Nowadays, IoT devices are playing an increasingly important role for people, and we can't imagine our lives without them. Since most  people have an internet connection at home, building such an IoT system is easier, cheaper and more efficient because there is no need for wires to communicate between devices.   The system I developed and built consists of a central computer with a touch screen display connected to it, where you can follow and intervene in the automation processes, you can see statistics about the temperature in the room, for example. Several sensors are connected to this central part via Bluetooth or MQTT communication pr otocols, which provide data and perform the automation tasks. In my thesis I document the design and construction of this system in detail, illustrating each part with diagrams."
        ),
        "keywords": ["IoT", "Home-automation", "Raspberry Pi", "MQTT"]
    },
    {
        "author": "Bako Jozsef",
        "year": 2023,
        "abstract": (
            "Measuring temperature has always played an important role in human life due to the curiosity of it’s nature. With the advance of the world and the temperatures measuring technologies, this taskhas become a trivial problem, regardless of what we measure the temperature of. The scope of this project is to create a heat follower robot and a mobile application for controlling it, which identifies the temperature extremes in a closed area and approaches it, as well. As for the app, my aim is to establish a Bluetooth connection between this and the robot and show a picture of it’s view to the user. Also, I want it to make manual control possible."
        ),
        "keywords": ["temperature measurement", "bluetooth", "application", "robot control"]
    },
    {
        "author": "Balint Adolf",
        "year": 2023,
        "abstract": (
            "The  topic  of  my  paper  is  documenting  and  tracking  the  game  of  backgammon  game  in  which  I  dealt  with  game  programming,  image  processing,  and  real-time  game  tracking  of  game  progres.  Backgammon  and  image  processing  cover  two  areas  of  particular  interest  to  me..  The  Romanian  Backgammon  Federation  organizes  various  national  and  international  competitions,  where tracking and automatic arbitration are of particular interest.  The  Python  programming  language  allows  for  the  creation  of  virtual  versions  of  backgammon,  which  gives  the  game  a  new  dimension  by  interactively  playing  it  on  the  computer .  The  goal  of  game  programming  was  to  enable  two  players  to  compete  against  each  other  on  the  computer  and record the game for later replay .  OpenCV  (Open  Source  Computer  Vision  Library)  is  a  popular  library  used  in  image  processing.  With  its  help,  the  computer  can  recognize  shapes  and  process  images,  allowing  for  capturing  the  sequential  playing  positions.  My  goal  in  the  field  of  image  processing,  was  to  extract  still  frames  from a video and identify the position of pieces, thus tracking the game's progress.  Therefore,  my  objective  was  to  create  an  application  by  combining  Python  and  OpenCV  that  automatically  evaluates  the  board  game.The  software  to  be  made  must  recognize  the  positions  of  pieces and tracks the players' moves, allowing for virtual gameplay between two individuals."
        ),
        "keywords": ["backgammon", "image processing", "OpenCV", "Python"]
    },
    {
        "author": "Bocsardi Andras",
        "year": 2023,
        "abstract": (
            "The topic of this thesis is the classification of brain tumours using convolutionalneural networks. In the first half of the paper, I will describe neural networks basedon  the  literature,  starting  from  simple  M-P  neurons  to  convolutional  neuralnetworks, covering their structure and their training. In the second half of thepaper, I present three models I developed that classified brain tumours into fourgroups with an accuracy of over 85%. The first model I implemented was a simpleconvolutional neural network. With the second model I achieved only moderateperformance  improvements  by  changing  the  architecture  and  preventingoverfitting. For both models I tuned the hyperparameters. The best performingmodel was the third one, implemented with transfer learning and using VGG16 asthe base model. This model achieved the best accuracy (96%). In developing thethree models, I used methods to continuously improve the performance of neuralnetworks  by  understanding  the  different  mechanisms  of  action.  The  model  Ideveloped  could  form  the  basis  for  an  application  that  provides  practicingradiologists with rapid preclassification in seconds, making their job easier."
        ),
        "keywords": ["convolutional neural networks", "brain tumor", "classification", "keras"]
    }
]

with open("theses.json", "w") as json_file:
    json.dump(theses, json_file, indent=4)
