# cadavre exquis

1. créez un venv 

```
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
```

2. Activez l'environnement 

Mac 
```$ . venv/bin/activate```

Windows
```> venv\Scripts\activate```

3. installez les paquets avec pip

```
python3 pip install Flask
python3 pip install scrapy
python3 pip install requests
python3 pip install google_images_search
```

windows: 
```pip install windows-curses```

4. exportez l'app

Mac
```export FLASK_APP=views.py``` 

Windows
```set FLASK_APP=views.py``` 

5. lancez l'app

```flask run```

