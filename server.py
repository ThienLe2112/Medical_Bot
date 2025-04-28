from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import uvicorn
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import Optional, Union
from typing import AsyncGenerator
import threading
import cv2
import time
from ultralytics import YOLO

# some_file_path = "video.mp4"

def rescale_frame(frame_input, percent=75):
    width = int(frame_input.shape[1] * percent/100)
    height = int(frame_input.shape[0] * percent/100)
    dim = (width, height)
    return cv2.resize(frame_input, dim, interpolation=cv2.INTER_AREA)

def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] *
             (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)


def draw_box(results, frame):
    for result in results:
        # get the classes names
        classes_names = result.names
        # iterate over each box
        for box in result.boxes:
            # check if confidence is greater than 40 percent
            if box.conf[0] > 0.6:
                # get coordinates
                [x1, y1, x2, y2] = box.xyxy[0]
                # convert to int
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # get the class
                cls = int(box.cls[0])
                cls_conf = box.conf[0]
                # get the respective colour
                colour = getColours(cls)
                cls_name = classes_names[int(box.cls[0])]


                # draw the rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 1)

                # class name

                # put the class name and confidence on the image
                cv2.putText(frame, f'{cls_name} {cls_conf:.2f}', (
                    x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 2)
                

    return frame


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

class Camera:
    """
    A class to handle video capture from a camera.
    """

    def __init__(self, url: Optional[Union[str, int]] = 0) -> None:
        """
        Initialize the camera.

        :param camera_index: Index of the camera to use.
        """
        # self.cap = cv2.VideoCapture('/home/dog/web/video.mp4')
        # self.cap = cv2.VideoCapture('D://Documents//DaiHoc//Nam4_HK2//AIOT//Web//video.mp4')
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO("best2.engine")
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.lock = threading.Lock()
        self.frame_detect =0 
        self.init=0

    def get_frame(self) -> bytes:
        """
        Capture a frame from the camera.

        :return: JPEG encoded image bytes.
        """
        with self.lock:
            #frame = cam.capture_array()
            # frame = self.cap.capture_array()
            ret, frame= self.cap.read()
            if ret is None:
                return 0
            
            frame = rescale_frame(frame, 25)
            self.frame_detect = frame.copy()
            future = self.executor.submit(self.model, self.frame_detect)
            self.future2 = self.executor.submit(draw_box, future.result(), self.frame_detect)
            # if self.future2.done():
            self.frame_detect = self.future2.result()
            # else:
            #     self.frame_detect = frame
            # if self.init == 0:
            #     self.frame_detect = frame
            #     self.init = 1
            
            # if future2.done():
            #     frame_detect = future2.result()
            # else:
            #     frame_detect = frame
            # objs = detect.get_objects(interpreter, 0.4)[:args.top_k]
            
            # objs = detect.get_objects(interpreter, 0.4)
            # cv2_im = append_objs_to_img(cv2_im, inference_size, objs, labels)

            ret, jpeg = cv2.imencode('.jpg', self.frame_detect)
            # ret, jpeg = cv2.imencode('.jpg', cv2_im)
            if not ret:
                return b''
            time.sleep(0.01)

            return jpeg.tobytes()

    def release(self) -> None:
        """
        Release the camera resource.
        """
        with self.lock:
            if self.cap.isOpened():
                self.cap.release()
    def reset(self):
        self.__init__()


async def gen_frames() -> AsyncGenerator[bytes, None]:
    """
    An asynchronous generator function that yields camera frames.

    :yield: JPEG encoded image bytes.
    """
    try:
        while True:
            frame = camera.get_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break
            await asyncio.sleep(0)
    except (asyncio.CancelledError, GeneratorExit):
        print("Frame generation cancelled.")
    finally:
        camera.reset()
        print("Frame generator exited.")


@app.get("/video")
async def video_feed() -> StreamingResponse:
    """
    Video streaming route.

    :return: StreamingResponse with multipart JPEG frames.
    """
    return StreamingResponse(
        gen_frames(),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )


@app.get("/snapshot")
async def snapshot() -> Response:
    """
    Snapshot route to get a single frame.

    :return: Response with JPEG image.
    """
    frame = camera.get_frame()
    if frame:
        return Response(content=frame, media_type="image/jpeg")
    else:
        return Response(status_code=404, content="Camera frame not available.")



if __name__== "__main__":
    camera = Camera()
    uvicorn.run(app,host="192.168.7.150",port=8080)
