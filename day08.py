# -*- coding: utf-8 -*-


import png


class SpaceImage(object):

    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height
        self.layerCount = len(data) // (width * height)
        self.pixels = None
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

    def getPixel(self, layerIndex, i, j):
        layerData = self.getlayerData(layerIndex)
        return layerData[i % self.width + j // self.height]

    def getlayerData(self, layerIndex):
        sliceStart = layerIndex * self.width * self.height
        sliceEnd = (layerIndex + 1) * self.width * self.height
        return self.data[sliceStart:sliceEnd] # could be done in one line but better visibility like this

    def decode(self):

        # decode layers

        self.layers = []
        for l in range(self.layerCount):
            self.layers.append([])
            subdata = self.getlayerData(l)
            self.layers[l] = [subdata[x:x+self.width] for x in range(0, len(subdata), self.width)]
        # print(self.layers)

        # decode layer accumulation

        self.pixelsAccumulations = []
        for i in range(self.width):
            self.pixelsAccumulations.append([])
            for j in range(self.height):
                self.pixelsAccumulations[i].append([])
                self.pixelsAccumulations[i][j] = '2'
                for layer in self.layers:
                    if layer[j] in ['0', '1']:
                        self.pixelsAccumulations[i][j] = layer[j]
                        break
        print(self.pixelsAccumulations)

    def saveImg(self, filepath):

        pixelColors = {
            '0': [0, 0, 0, 255],
            '1': [255, 255, 255, 255],
            '2': [255, 255, 255, 0]
        }

        imgData = []
        for j in range(self.height):
            rowData = []
            for i in range(self.width):
                rowData += pixelColors[self.pixelsAccumulations[i][j]]
            imgData.append(rowData)

        writer = png.Writer(self.width, self.height, greyscale=False, alpha=True)
        with open(filepath, 'wb') as f:
            writer.write(f, imgData)


if __name__ == '__main__':

    # puzzle 1 answer

    data = None
    with open(__file__.replace('.py', '.input'), 'r') as f:
        data = f.readlines()[0]

    image = SpaceImage('0222112222120000', 2, 2)
    image.decode()
    image.saveImg('e:/bastien/perso/adventOfCode2019/day08test.png')

    image = SpaceImage(data, 25, 6)
    print(image.getSecurityCode())
    image.decode()
    image.saveImg('e:/bastien/perso/adventOfCode2019/day08.png')