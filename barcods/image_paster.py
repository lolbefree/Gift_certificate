from PIL import Image



class certification:

    def __init__(self, barcode, image_name):
        self.barcode = barcode
        self.image_name = image_name


    def five_100(self,):

        img1 = Image.open('500.jpg')                               # main image
        im = Image.open("8784542537122.png")                        # barcode image
        im.resize((600, 220)).save("barcode_resized.png")            # new size
        barcd = Image.open('barcode_resized.png')                   # save new size
        barcd.putalpha(255)

        img1.paste(barcd, (0, 1200), barcd)                         # paste barcode to main image
        img1.save("img_with_watermark.png")                         # save with barcode


