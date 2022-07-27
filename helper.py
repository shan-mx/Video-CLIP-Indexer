import base64
import cv2
import subprocess
from clip_client import Client
from typing import List, Tuple, Dict
from docarray import Document, DocumentArray
import numpy as np

client = Client(server='grpc://0.0.0.0:51000')


def get_frame_types(file: str):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [file]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types)


def get_keyframes_b64(file: str, save_image: bool = False):
    frame_types = get_frame_types(file)
    i_frames = [x[0] for x in frame_types if x[1] == 'I']  # select the key frames
    keyframes_b64 = []
    if i_frames:
        cap = cv2.VideoCapture(file)
        for frame_num in i_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            success, frame = cap.read()
            if success:
                if save_image:
                    outname = str(frame_num) + '.jpg'
                    cv2.imwrite(outname, frame)
                    print('Saved: ' + outname)
                retval, buffer = cv2.imencode('.jpg', frame)
                pic_b64 = base64.b64encode(buffer).decode()  # get b64 string from ndarray
                keyframes_b64.append((frame_num, pic_b64))
        cap.release()
    return keyframes_b64


def search_frame(file_name: str, prompt: str, topn: int):
    keyframe_data = get_keyframes_b64(file_name)
    da = DocumentArray(
        [Document(tags={'index': str(tup[0])}, uri='data:image/jpg;base64,' + tup[1]) for tup in keyframe_data])
    d = Document(
        text=prompt,
        matches=da,
    )
    r = client.rank([d])
    result = r['@m', ['tags', 'uri', 'scores__clip_score__value']]
    return [each[:topn] for each in result]


def get_img_np_from_b64(img):
    b, g, r = cv2.split(cv2.imdecode(np.fromstring(base64.b64decode(img), dtype=np.uint8), cv2.IMREAD_COLOR))
    return cv2.merge([r, g, b])  # convert cv2's BGR to PIL's RGB


if __name__ == '__main__':
    print(search_frame('1.mp4', '一群人站在一起', 5))
