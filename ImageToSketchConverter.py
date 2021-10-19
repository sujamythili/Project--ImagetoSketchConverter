
import streamlit as slite
import numpy as npy
import cv2
from PIL import Image
import io
import time
import base64



#Left sidebar Configuration
slite.page_set(
     page_title="Convert Image to Pencil Sketch",
     initial_sidebar_state="expanded",
)

#def is the keyword to define Function 
def sketch_image_download(img,filename,text):
    read = io.BytesIO()
    img.save(read, format="JPEG")
    data = base64.b64encode(read.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{data}" download="{filename}">{text}</a>'
    return href

def convert_image_to_sketch(img):
    #asarray() function is used when we want to convert input to an array.
    #cv2. imdecode() function reads data from specified memory cache and converts (decodes) data into image format; It is mainly used for compressing image data format to facilitate network transmission
    #cv2. cvtColor() method is used to convert an image from one color space to another. 
    #the bitwise NOT function flips pixel values. All pixels that are greater than zero are set to zero, and all pixels that are equal to zero are set to 255.
    #You can use GaussianBlur() method of cv2 library to blur an image.
    #Grayscaling - Converting image from other spaces i.e, RGB,CMYK to gray 
    
    #Python OpenCV has several filtering techniques to perform smoothing operations on images, like - Gaussian Filtering, Median Filtering, 
    #Bilateral Filtering. Images can contain different types of noise, especially because of camera sensor. 
    #These smoothing techniques are generally used to reduce noise, reduce detail, and so on. Each pixel in an image gets multiplied by Gaussian Kernel. It means, a Gaussian Kernel is a square array of pixels.    
    #sample synatx - cv2.GaussianBlur(src, ksize, sigma_x, dst, sigma_y, border_type)

    file_bytes = npy.asarray(bytearray(img), dtype=npy.uint8)
    cvImage = cv2.imdecode(file_bytes, 1)
        
    cvImageGrayScale = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
    cvImageGrayScaleInversion = cv2.bitwise_not(cvImageGrayScale)
    cvImageBlured = cv2.GaussianBlur(cvImageGrayScaleInversion, (21, 21), sigmaX = 0, sigmaY = 0)
    sketchImage = cv2.divide(cvImageGrayScale, 255 - cvImageBlured, scale = 256)
    
    return sketchImage
    
slite.title("Convert your Image to Pencil Sketch")

slite.sidebar.title("Please Upload your image")

slite.set_option('deprecation.showfileUploaderEncoding', False)

img = Image.open("upload.jpg")
image = slite.image(img)

uploaded_file = slite.sidebar.file_uploader(" ", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:  
    image.image(uploaded_file)

if slite.sidebar.button("Convert to Pencil Sketch"):
     
     if uploaded_file is None:
         slite.sidebar.error("Please upload a image to convert")
        
     else:
        with slite.spinner('Converting into Pencil Sketch...'):
            
            sketchImage = convert_image_to_sketch(uploaded_file.read())
            
            time.sleep(2)
            #image.image(sketchImage)
            slite.success('Converted!')
            slite.success('Click "Download Image" below the sketched image to download the image')
            image = slite.image(sketchImage)
            slite.sidebar.success("Please scroll down for your sketched image!")


if slite.button("Download Image"):
    if uploaded_file:
        sketchedImage = convert_image_to_sketch(uploaded_file.read())
        image.image(sketchedImage)
        result = Image.fromarray(sketchedImage)
        slite.success("Press the below Link")
        slite.markdown(sketch_image_download(result,"sketched.jpg",'Download '+"Sketched.jpg"), unsafe_allow_html=True)
    else:
        slite.error("Please upload a image first")
