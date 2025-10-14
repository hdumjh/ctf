from PIL import Image
import sys

im = Image.open(sys.argv[1])
width = im.size[0]  
height = im.size[1]  
#print "/* width:%d */"%(width)  
#print "/* height:%d */"%(height)  
pix = im.load()

count = 0   
for h in range(0, 100):         
    r, g, b=pix[h,h]
    #rgb = (r, g, b)
    print g
