
import os
import cv

in_dir = "../data/inputs/sample-test"
out = "output.avi"


# loading images, create Guys and store it into guys
frameSize = (652, 498)
#frameSize = (453, 325)
fourcc = cv.CV_FOURCC('F', 'M', 'P', '4')
my_video = cv.CreateVideoWriter(out, 
                              fourcc, 
                              15, 
                              frameSize,
                              1)

for root, _, files in os.walk(in_dir):
    for a_file in files:
        guy_source = os.path.join(in_dir, a_file)
        print guy_source
        image = cv.LoadImage(guy_source)

        small_im = cv.CreateImage(frameSize, 
                                  image.depth ,
                                  image.nChannels)        
        cv.Resize(image, small_im, cv.CV_INTER_LINEAR)
        cv.WriteFrame(my_video, small_im)

print "Finished !"