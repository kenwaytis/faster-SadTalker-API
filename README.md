## What is it:

1. This project is from OpenTalker/SadTalker
2. This project transforms SadTalker into a Docker container that provides a RESTful API, combined with the open source TTS service (which has been provided in addition to the mirror), input text that is to get the output Talking Face video.
3. This project greatly improves the original SadTalker reasoning speed (10x!) This project greatly improves the inference speed of the original SadTalker (10x !). Means including but not limited to: optimize the file saving logic, optimize the function call logic, face enhancement part of the conversion model operator......

## Installation:

1. Ensure that you have installed
   1.docker
   2.nvidia driver
   3.nvidia container
   4.TTS service is required for this service. You can get the API Docker image of the ready-made TTS from xxxx and start it with one click.

2. The docker-compose.yml file specifies the fixed image that is ready. If you want to build your own image from scratch, you can change the image name so that docker builds the image from source.

   In the ***docker-compose.yml*** :
   Modify the

   ```
   image: paidax/sadtalker:2.3.2
   ```

   to

   ```dockerfile
   image: namespace/sadtalker:latest
   ```

3. Specify the TTS server address

   ```shell
   export TTS_SERVER=http://your_tts_server
   ```

4. Starting the Container Service

   ```shell
   docker compose up
   ```

## Usage:

The interface address is

```http
localhost:10364
```

You can access the interface via the
```http
localhost:10364/docs
```

to view the interface documentation.
