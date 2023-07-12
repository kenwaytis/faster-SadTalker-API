import os
import torch 

# from gfpgan import GFPGANer

from src.demo_onnx import GFPGANFaceAugment

from tqdm import tqdm

from src.utils.videoio import load_video_to_cv2

import cv2


class GeneratorWithLen(object):
    """ From https://stackoverflow.com/a/7460929 """

    def __init__(self, gen, length):
        self.gen = gen
        self.length = length

    def __len__(self):
        return self.length

    def __iter__(self):
        return self.gen

def enhancer_list(images, method='gfpgan', bg_upsampler='realesrgan'):
    gen = enhancer_generator_no_len(images, method=method, bg_upsampler=bg_upsampler)
    return list(gen)

def enhancer_generator_with_len(images, method='gfpgan', bg_upsampler='realesrgan'):
    """ Provide a generator with a __len__ method so that it can passed to functions that
    call len()"""

    if os.path.isfile(images): # handle video to images
        images = load_video_to_cv2(images)

    gen = enhancer_generator_no_len(images, method=method, bg_upsampler=bg_upsampler)
    gen_with_len = GeneratorWithLen(gen, len(images))
    return gen_with_len

def enhancer_generator_no_len(images, method='gfpgan', bg_upsampler='realesrgan'):
    """ Provide a generator function so that all of the enhanced images don't need
    to be stored in memory at the same time. This can save tons of RAM compared to
    the enhancer function. """

    print('face enhancer....')
    if not isinstance(images, list) and os.path.isfile(images): # handle video to images
        images = load_video_to_cv2(images)

    # ------------------------ set up GFPGAN restorer ------------------------
    if  method == 'gfpgan':
        arch = 'clean'
        channel_multiplier = 2
        model_name = 'GFPGANv1.4'
        url = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth'


    # ------------------------ set up background upsampler ------------------------
    bg_upsampler = None

    # determine model paths
    model_path = '/home/SadTalker/gfpgan/weights/GFPGANv1.4.onnx'

    # restorer = GFPGANer(
    #     model_path=model_path,
    #     upscale=2,
    #     arch=arch,
    #     channel_multiplier=channel_multiplier,
    #     bg_upsampler=bg_upsampler)
    restorer = GFPGANFaceAugment(model_path=model_path,use_gpu=True)

    # ------------------------ restore ------------------------
    for idx in tqdm(range(len(images)), 'Face Enhancer:'):
        
        img = cv2.cvtColor(images[idx], cv2.COLOR_RGB2BGR)
        
        # restore faces and background if necessary
        # cropped_faces, restored_faces, r_img = restorer.enhance(
        #     img,
        #     has_aligned=False,
        #     only_center_face=False,
        #     paste_back=True)
        r_img, _ = restorer.forward(img)
        
        r_img = cv2.cvtColor(r_img, cv2.COLOR_BGR2RGB)
        yield r_img
