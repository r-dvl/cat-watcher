# Cat Watcher
Motion detector built with Python, OpenCV and Pymongo. Once motion is detected the motion frame is posted in a MongoDB and shown in my React WebApp __lima-frontend__
> [lima-frontend](https://github.com/R-dVL/lima-frontend)

## Dependencies
- Python3
- Webcam
- MongoDB

## Structure
### Camera
Any webcam or camera detected by the computer works correctly. The Camera class is constructed with an id that identifies the camera to be used.

### MongoDB
I'm using Mongo DB to save motion frames in base64 with their date (changing to singleton instance since it is constructed once and constructor parameters are read from configuration.py).

### Configuration
This project is built and deployed with a Jenkins Job that creates an archive .env with all MongoDB parameters (user, password, uri...).
> [automationLibrary](https://github.com/R-dVL/automationLibrary)

### cat-watcher
Main loop where motion detector is built and executed.

## TODO
- [ ] Change MongoDB to HTTP Request from __lima-backend__ (base64 images are too big for this request) and delete MongoDB and Configuration classes.
  > [lima-backend](https://github.com/R-dVL/lima-backend)
