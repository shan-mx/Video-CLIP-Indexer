from clip_client import Client
from docarray import Document, DocumentArray
import skvideo.io
import imagehash
from PIL import Image
from numpy import ndarray

client = Client(server='grpc://0.0.0.0:51000')


def get_keyframes(video_data: 'ndarray', cut_sim: float):
    last_hash = imagehash.phash(Image.fromarray(video_data[0]))
    i_frames = [0]
    frame_num = 0
    for each_frame in video_data:
        frame_hash = imagehash.phash(Image.fromarray(each_frame))
        similarity = 1 - (last_hash - frame_hash)/len(frame_hash.hash)**2
        if similarity < cut_sim:
            i_frames.append(frame_num)
        frame_num += 1
        last_hash = frame_hash
    return i_frames


def get_keyframes_data(file: str, cut_sim: float):
    video_data = read_video(file)
    key_frames = get_keyframes(video_data, cut_sim)
    video_length = len(video_data)
    key_frames.append(video_length)
    keyframes_data = [((i, key_frames[key_frames.index(i)+1]), video_data[i]) for i in key_frames if i != video_length]
    return keyframes_data


def search_frame(file_name: str, prompt: str, topn: int, cut_sim: float):
    keyframe_data = get_keyframes_data(file_name, cut_sim)
    da = DocumentArray([Document(tags={'left': str(tup[0][0]), 'right': str(tup[0][1])}, tensor=tup[1]) for tup in keyframe_data])
    d = Document(text=prompt, matches=da)
    r = client.rank([d])
    result = r['@m', ['tags', 'tensor', 'scores__clip_score__value']]
    return [each[:topn] for each in result]


def read_video(file: str):
    return skvideo.io.vread(file)


def write_video(file: str, data: 'ndarray'):
    skvideo.io.vwrite(file, data)
