## Note：

1. This project is still being updated, if you have any questions you can ask in issues.
2. Please note that the use of the model is subject to the original developer license usage.

## Update:

2023.8.2

1. replace the default image (if there is a copyright issue, please issues inform, will change as soon as possible)
2. update the TTS server, it is now a full runnable system
3. Update the model download address. Please note that the use of the models is subject to the original developer license usage.

## What is it:

1. This project is from OpenTalker/SadTalker
2. This project transforms SadTalker into a Docker container that provides a RESTful API, combined with the open source TTS service (which has been provided in addition to the mirror), input text that is to get the output Talking Face video.
3. This project greatly improves the original SadTalker reasoning speed (10x!) This project greatly improves the inference speed of the original SadTalker (10x !). Means including but not limited to: optimize the file saving logic, optimize the function call logic, face enhancement part of the conversion model operator......

## Installation:

1. Ensure that you have installed

- docker
- nvidia driver
- nvidia container

2. Download the model from the following address and store it in the corresponding directory according to the instructions.

   - **SadTalker's checkpoints**:  
     Create the necessary directories using the following command:
     ```shell
     mkdir -p checkpoints
     ```
     Download all model files from the latest releases at `./checkpoints`.  
     [SadTalker releases](https://github.com/OpenTalker/SadTalker/releases)

   - **gfpgan in onnx**:  
     Download all remaining model files in the latest releases of this project and store them in `./gfpgan/weights`.  
     You can create the directory using:
     ```shell
     mkdir -p gfpgan/weights
     ```
     [releases](https://github.com/kenwaytis/faster-SadTalker-API/releases)


3. The docker-compose.yml file specifies the fixed image that is ready. If you want to build your own image from scratch, you can change the image name so that docker builds the image from source.

   In the ***docker-compose.yml*** :
   Modify the

   ```
   image: paidax/faster-sadtalker-api:0.1.3
   ```

   to

   ```dockerfile
   image: namespace/faster-sadtalker-api:0.1.3
   ```

4. Specify the TTS server address

   Update: TTS service is now integrated into docker-compose, if you have customization needs you can refer to `localhost:9566/docs` to modify

5. Starting the Container Service

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
