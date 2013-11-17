__author__ = 'zhaoyuli'
import urllib
import time
import datetime
import Image
import cv2
import shutil


picDict = {'0': '0.png',
           '1': '1.png',
           '2': '2.png',
           '3': '3.png',
           '4': '4.png',
           '5': '5.png',
           '6': '6.png',
           '7': '7.png',
           '8': '8.png',
           '9': '9.png',
           'a': 'a.png',
           'b': 'b.png',
           'c': 'c.png',
           'd': 'd.png',
           'e': 'e.png',
           'f': 'f.png',
           'g': 'g.png',
           'h': 'h.png',
           'i': 'i.png',
           'j': 'j.png',
           'k': 'k.png',
           'l': 'l.png',
           'm': 'm.png',
           'n': 'n.png',
           'o': 'o.png',
           'p': 'p.png',
           'q': 'q.png',
           'r': 'r.png',
           's': 's.png',
           't': 't.png',
           'u': 'u.png',
           'v': 'v.png',
           'w': 'w.png',
           'x': 'x.png',
           'y': 'y.png',
           'z': 'z.png'
}

def imgFilter(img, chop):
    width, height = img.size
    data = img.load()
    # Iterate through the rows.
    print data
    for y in range(height):
        for x in range(width):
            print data[x,y]
            # Make sure we're on a dark pixel, make it pure black.
            if data[x, y] > 128:
                data[x, y] = 225
                continue
            else:
                data[x,y] = 0

            # Keep a total of non-white contiguous pixels.
            total = 0

            # Check a sequence ranging from x to image.width.
            for c in range(x, width):

                # If the pixel is dark, add it to the total.
                if data[c, y] < 128:
                    data[c, y] = 0
                    total += 1
                # If the pixel is light, stop the sequence.
                else:
                    break
            # If the total is less than the chop, replace everything with white.
            if total <= chop:
                for c in range(total):
                    data[x + c, y] = 255

            # Skip this sequence we just altered.
            x += total


    # Iterate through the columns.
    for x in range(width):
        for y in range(height):

            # Make sure we're on a dark pixel.
            if data[x, y] > 128:
                data[x, y] = 255
                continue

            # Keep a total of non-white contiguous pixels.
            total = 0

            # Check a sequence ranging from y to image.height.
            for c in range(y, height):

                # If the pixel is dark, add it to the total.
                if data[x, c] < 128:
                    data[x, c] = 0
                    total += 1

                # If the pixel is light, stop the sequence.
                else:
                    break

            # If the total is less than the chop, replace everything with white.
            if total <= chop:
                for c in range(total):
                    data[x, y + c] = 255

            # Skip this sequence we just altered.
            y += total




def readPic(image):

    theKey = ''
    currentMax = 0
    for key, picName in picDict.iteritems():
        path = './codepic/'+picName
        #print key
        temp = my_image_similarity(image, path)
        if temp > currentMax:
            currentMax = temp
            theKey = key
    print theKey





def my_image_similarity(filepath1, filepath2):
    list1 = list(Image.open(filepath1).getdata())
    list2 = list(Image.open(filepath2).getdata())
    counter = 0;
    for i in range(100):
        if list1[i] == list2[i]:
            counter = counter + 1

    return counter


#sudo pip install numpy PIL
def image_similarity(filepath1, filepath2):
    import numpy
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)
    #if image1.size != image2.size or image1.getbands() != image2.getbands():
    #    return -1
    s = 0
    for band_index, band in enumerate(image1.getbands()):
        m1 = numpy.array([p[band_index] for p in image1.getdata()]).reshape(*image1.size)
        m2 = numpy.array([p[band_index] for p in image2.getdata()]).reshape(*image2.size)
        s += numpy.sum(numpy.abs(m1-m2))
    return s

#sudo pip install PIL
def pil_image_similarity(filepath1, filepath2):
    import math
    import operator

    image1 = Image.open(filepath1).convert('L').point(lambda i: i > 128 and 255)
    image2 = Image.open(filepath2).convert('L').point(lambda i: i > 128 and 255)

    h1 = image1.histogram()
    h2 = image2.histogram()

    rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return rms

# sudo pip install numpy
def numpy_image_similarity(filepath1, filepath2):
    import Image
    from numpy import average, linalg, dot
    import sys
    images = [filepath1, filepath2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in Image.open(image).getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    res = dot(a / a_norm, b / b_norm)
    return res

for i in range(10):
    time.sleep(1)
    time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    time_stamp_jpg = time_stamp + '.jpg'
    urllib.urlretrieve("http://218.58.65.23/select/checkcode.asp", time_stamp_jpg)
    shutil.copy(time_stamp_jpg, time_stamp + 'origin.png')

    #cvImg = cv2.imread(time_stamp_jpg)
    #grayCvImg = cv2.cvtColor(cvImg, cv2.COLOR_RGB2GRAY)
    #cv2.imwrite(time_stamp_jpg, grayCvImg)



    img = Image.open(time_stamp_jpg)
    grayImg = img.convert('L').point(lambda i: i > 128 and 255)
    grayImg.save(time_stamp_jpg)
    #imgFilter(grayImg, 0)
    frame1 = grayImg.crop(((0, 0, 10, 10)))
    frame1.save(time_stamp + '_1.png')
    frame2 = grayImg.crop(((10, 0, 20, 10)))
    frame2.save(time_stamp + '_2.png')
    frame3 = grayImg.crop(((20, 0, 30, 10)))
    frame3.save(time_stamp + '_3.png')
    frame4 = grayImg.crop(((30, 0, 40, 10)))
    frame4.save(time_stamp + '_4.png')

    readPic(time_stamp + '_1.png')
    readPic(time_stamp + '_2.png')
    readPic(time_stamp + '_3.png')
    readPic(time_stamp + '_4.png')