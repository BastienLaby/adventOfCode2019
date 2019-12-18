# -*- coding: utf-8 -*-


class SpaceImage(object):

    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height
        self.layerCount = len(data) // (width * height)
        self.layers = []

    def getSecurityCode(self):
        digitsCounts = []
        for i in range(self.layerCount):
            subdata = self.getlayerData(i)
            digitsCounts.append({
                '0': subdata.count('0'),
                '1': subdata.count('1'),
                '2': subdata.count('2')
            })

        securitylayer = sorted(digitsCounts, key=lambda i: i['0'])[0]
        return securitylayer['1'] * securitylayer['2']

    def getlayerData(self, layerIndex):
        sliceStart = layerIndex * self.width * self.height
        sliceEnd = (layerIndex + 1) * self.width * self.height
        return self.data[sliceStart:sliceEnd] # could be done in one line but better visibility like this

    def decodeLayers(self):
        self.layers = []
        for l in range(self.layerCount):
            self.layers.append([])
            subdata = self.getlayerData(l)
            self.layers[l] = [subdata[x:x+self.width] for x in range(0, len(subdata), self.width)] # magic formula : split one list into multiple sublists of size self.width

    def printImg(self):

        pixelColors = {
            '2': '.',
            '1': '#',
            '0': '.'
        }

        for j in range(self.height):
            for i in range(self.width):
                pixels = [layer[j][i] for layer in self.layers]
                while '2' in pixels:
                    pixels.remove('2')
                pixelValue = '2' if not pixels else pixels[0]
                print(pixelColors[pixelValue] + ' ', end='')
            print('')


if __name__ == '__main__':

    image = SpaceImage('0222112222120000', 2, 2)
    image.decodeLayers()
    image.printImg()

    data = None
    with open(__file__.replace('.py', '.input'), 'r') as f:
        data = f.readlines()[0]

    image = SpaceImage(data, 25, 6)
    print(image.getSecurityCode())
    image.decodeLayers()
    image.printImg()
