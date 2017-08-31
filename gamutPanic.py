#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image,ImageDraw, ImageFont


def prepareMidImage(fillText = "ABCDEFGHIJKLMNOPQVWYZ", imgSize = (800,600),fontSize = 10, fontFamily=""):
    fontColor = (0,0,0,255)
    print "Creating text Image."
    midImage = Image.new("RGBA",imgSize,(255,255,255,0))

    print "Loading Font...",
    try:
        fnt = ImageFont.truetype(fontFamily,fontSize)
        print
    except:
        print "font not found!"
        print "using default (and default size)"
        print
        fnt = ImageFont.load_default()
    drw = ImageDraw.Draw(midImage) #now we can draw on the midImage

    fillLen = len(fillText)
    counter = 0
    text = ""
    coordy = 0

    #y passes
    print "Calculating workload...",
    passes = (imgSize[1]/fnt.getsize(fillText)[1])
    passCounter = 1
    print "{} passes.".format(passes)
    print "Rendering text..."
    print
    while (coordy < imgSize[1]):
        pre = int(passCounter/float(passes)*100)
        print "\33[2K", #clean the line
        print "\r", #get the cursor in the start of the line
        if(pre <= 100):
            print "{}% ({}/{})".format(pre ,passCounter,passes),
            sys.stdout.flush() #flush is need cause the ANSI codes
        while (True):
            #optmization needed.
            text+=fillText[counter]
            sizeNow = fnt.getsize(text)

            counter+=1
            if(counter > len(fillText)-1):
                counter = 0

            if sizeNow[0] > imgSize[0]:
                break

        drw.text((0,coordy),text,font=fnt,fill=fontColor)
        coordy+= fnt.getsize(text)[1]
        passCounter+=1
        text = ""
    print "\nText Image complete."
    print
    return midImage

def forceMask(img):
    newMask = Image.new("1",img.size,(1))
    img = img.split()[3]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            p = img.getpixel((i,j))
            if(p < 15):
                newMask.putpixel((i,j),(0))
            else:
                newMask.putpixel((i,j),(255))
    return newMask

def merge(textImg,otherImg):
    print "Resizing top-level image..."
    otherImg = otherImg.resize(textImg.size)
    print "Creating the alphaMask..."
    alphaMask = textImg
    alphaMask = forceMask(alphaMask)
    print "Blending..."
    textImg.paste(otherImg,mask = alphaMask)
    print "Blend complete."
    return textImg


if __name__ == "__main__":
    import argparse
    parse = argparse.ArgumentParser()
    parse.add_argument("-m","--mask", help="The mask image")
    parse.add_argument("-s","--size", help="size of the output in pixels",nargs=2, type=int, default=[800, 600])
    parse.add_argument("-o","--output", help="output's file name", default="output.png")
    parse.add_argument("-t","--txt", help="txt file to write in the output")
    parse.add_argument("-bg", help="the color of the background",nargs=3, type=int, default=[75, 75, 75])
    parse.add_argument("-f","--font", help="a ''.ttf' font")
    parse.add_argument("-fs","--font-size", help="font size in points",type=int, default=12)
    parse.add_argument("--show", help="show the output image",action="store_true")
    args = parse.parse_args()
    print
    if args.txt is not None:
        try:
            #the text file
            t = open(os.path.realpath(args.txt),'r').read().replace("\n","")
            t = t.replace("                "," ")
            t = t.replace("            "," ")
            t = t.replace("        "," ")
            t = t.replace("    "," ") #needed for A E S T H E T I C S.

        except:
            print "text file not found"
            sys.exit(1)
    else:
        args.txt = "ABCDEFGHIJKLMNOPQVWYZ"

    try:
        #the mask file
        nImage = Image.open(os.path.realpath(args.mask)).convert("RGBA").resize(tuple(args.size))
    except:
        print "image file not found"
        sys.exit(1)

    mid = prepareMidImage(t,imgSize = tuple(args.size),fontSize= args.font_size,fontFamily=args.font)
    print "Reading top-level image."

    r = merge(mid,nImage)
    lowImage = Image.new("RGB",tuple(args.size),tuple(args.bg))
    lowImage.paste(r,mask= r.split()[3]) #mid's alpha
    if(args.show):
        lowImage.show()
    try:
        lowImage.save(args.output)
    except:
        print "Error writing the output"
        sys.exit(1)

    print "\nAll Done."
