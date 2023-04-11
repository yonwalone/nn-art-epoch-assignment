

class CONVLayer:

    def __init__(self, matrix):

        self.matrix = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
        self.matrix_height = len(self.matrix)
        
        self.matrix_width = len(self.matrix[0])
        for parameterIndex in range(0, self.matrix_height):
            if(len(self.matrix[parameterIndex]) != self.matrix_width):
                raise Exception("Matrix must has the same width in all rows")
            
    def act(image):
        # image is 3 dim array or 2dim ???
        image_height = len(image)
        image_width = len(image[0])


        h = 1


    def handleError():
        g= 1



    


    