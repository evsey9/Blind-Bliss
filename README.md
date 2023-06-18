# Blind Bliss
A project by students of Innopolis University for generating an audio description of visual content.

## Launch 

Copy env_list_default.txt into env_list.txt and edit the openai and telegram bot token lines.

Then, build docker image:
```
docker build -t evsey/blind-bliss .
```

After building:
```
docker run --name blind-bliss-container --env-file ./env_list.txt evsey/blind-bliss
```

Restart container after it stopped:
```
docker restart blind-bliss-container
docker attach blind-bliss-container
```