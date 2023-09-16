import matplotlib.pyplot as plt
import numpy as np
from skimage import data


def find_range(num_1, num_2):
    """Performs Integer division, used for number of times to watermark
    Args:
        num_1 (Int): Dividend
        num_2 (Int): Divisor

    Returns:
        Int: Quoitient rounded plus one to ensure coverage for watermark.
    """
    return int(round((num_1 / num_2)) + 1)

class Watermark():
    def __init__(self, font_size, font_name, text):
        #TODO Add more fonts.
        """Initializes watermark object

        Args:
            font_size (Int): Size of font
            font_name (String): Name of font to use from font dict.
            text (String): Text to watermark on image
        """
        self.fig = plt.figure()
        self.font_dict = {'Dejavu Sans Mono' : 
                          { 'font_height' : 1,
                            'font_width' : .6}}
        self.font_name = font_name
        self.font_size = font_size
        self.text = text
    
    def set_font_size_in(self):
        """Converts font size from pts to inches. Takes font height and width
        from font dictionary.

        Returns:
            Float: Height in inches.
            Float: Width in inches.
        """
        font_size_in = self.font_size / 72
        font_height = self.font_dict[self.font_name]['font_height'] * font_size_in 
        font_width = self.font_dict[self.font_name]['font_width'] * font_size_in
        return font_height, font_width

    def add_space(self):
        """Adds space to watermark text.
        """
        self.text += " "

    def make_watermark(self, img):
        """Creates a watermark on the image based on self attributes.

        Args:
            img (ndarray): Image data as ndarray

        Returns:
            ndarray: Returns watermarked image as ndarray.
        """
        #resizes fig to img_size
        fig = self.fig
        fig.figimage(img, resize=True)

        #gets figure sizes for calculations
        fig_width, fig_height = fig.get_figwidth(), fig.get_figheight()
        font_height, font_width = self.set_font_size_in()

        #finding amount of times to reiterate
        x_range = find_range(fig_width, font_width * len(self.text))
        y_range = find_range(fig_height, font_height)
        
        #iterates through and creates text
        for x_num in range(-(x_range),x_range,1):
            for y_num in range(-(y_range),y_range, 1):
                fig.text((((font_width)/ fig_width) * len(self.text)) * x_num, (font_height / fig_height) * y_num, self.text, color='#FFFFFF33', fontweight='ultralight', fontsize=self.font_size, va="center", ha='center', rotation=0, fontfamily='monospace')
        fig.canvas.draw()
        
        #new_img is now watermarked
        new_img = np.asarray(fig.canvas.renderer.buffer_rgba())
        plt.close(fig)
        return new_img