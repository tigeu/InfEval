from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager


class DrawBoundingBoxService:
    """
    Service that provides methods for drawing bounding boxes on a given image.

    Methods
    -------
    draw_bounding_boxes(predictions, image, settings, create=True)
        Draws bounding boxes of all predictions on the given image, using the given settings. Create image if create
    draw_gt_boxes(gts, image, settings)
        Draws filled bounding boxes of all ground truths in red if not matched by any prediction, green if matched
    _draw_bounding_box(draw, prediction, settings)
        Draws bounding box of a single prediction on the given image, using the given settings
    _draw_gt_bounding_box(draw, gt, settings)
        Draws filled bounding boxes of a single ground truth in red if not matched by any prediction, green if matched
    _draw_label(draw, prediction, settings, width)
        Draw label with a box around it above the image using the given settings
    _get_label_coordinates(text_width, text_height, width, xmin, ymin)
        Get label coordinates so that the label is not cut off if on the edge of the image
    _get_colors(data_class, settings)
        Get colors based on current settings (black/white or color for given data_class)
    """

    def draw_bounding_boxes(self, predictions, image, settings, create=True):
        """
        Draws bounding boxes of all predictions on the given image, using the given settings. Create image if create

        Parameters
        ----------
        predictions : list
            List of dictionaries, each representing a single prediction
        image : Path
            Path of current image
        settings : dict
            Dictionary containing several settings for drawing (including stroke size, colors, etc.)
        create : bool
            Indicates whether the transparent image has to be created yet

        Returns
        -------
        ImageDraw
            Transparent image containing all drawings
        """
        predictions = list(filter(lambda pred: pred['class'] in settings['classes'], predictions))
        # create transparent image
        if create:
            with Image.open(image) as img:
                width, height = img.size
            image = Image.new('RGBA', (width, height), (255, 0, 0, 0))
            draw = ImageDraw.Draw(image)
        # use given (transparent) image
        else:
            width, height = image.size
            draw = ImageDraw.Draw(image)

        for prediction in predictions:
            self._draw_bounding_box(draw, prediction, settings)

        # draw labels last so they are not overlapped by boxes
        if settings['show_labeled']:
            for prediction in predictions:
                self._draw_label(draw, prediction, settings, width)

        return image

    def draw_gt_boxes(self, gts, image, settings):
        """
        Draws filled bounding boxes of all ground truths in red if not matched by any prediction, green if matched

        Parameters
        ----------
        gts : list
            List of dictionaries, each representing a single ground truth
        image : Path
            Path of current image
        settings : dict
            Dictionary containing several settings for drawing (including stroke size, colors, etc.)

        Returns
        -------
        ImageDraw
            Transparent image containing all drawings
        """
        with Image.open(image) as img:
            width, height = img.size

        transparent_image = Image.new('RGBA', (width, height), (255, 0, 0, 0))
        draw = ImageDraw.Draw(transparent_image)

        gts.sort(key=lambda val: (val['xmax'] - val['xmin']) * (val['ymax'] - val['ymin']), reverse=True)
        for gt in gts:
            self._draw_gt_bounding_box(draw, gt, settings)
        return transparent_image

    def _draw_bounding_box(self, draw, prediction, settings):
        """
        Get colors based on current settings (black/white or color for given data_class)

        Parameters
        ----------
        draw : ImageDraw
            Drawing object
        prediction : dict
            Dictionary representing the current prediction
        settings : dict
            Dictionary containing several settings for drawing (including stroke size, colors, etc.)
        """
        xmin, ymin, xmax, ymax = prediction['xmin'], prediction['ymin'], prediction['xmax'], prediction['ymax']
        color, font_color = self._get_colors(prediction['class'], settings)
        draw.rectangle([xmin, ymin, xmax, ymax], outline=color, width=settings['stroke_size'])

    def _draw_gt_bounding_box(self, draw, gt, settings):
        """
        Draws filled bounding boxes of a single ground truth in red if not matched by any prediction, green if matched

        Parameters
        ----------
        draw : ImageDraw
            Drawing object
        gt : dict
            Dictionary representing the current ground truth
        settings : dict
            Dictionary containing several settings for drawing (including stroke size, colors, etc.)
        """
        xmin, ymin, xmax, ymax = gt['xmin'], gt['ymin'], gt['xmax'], gt['ymax']
        stroke_size = settings['stroke_size']
        if gt['matched']:
            if settings['ground_truth_transparent']:
                draw.rectangle([xmin, ymin, xmax, ymax], outline="green", width=stroke_size)
            else:
                draw.rectangle([xmin, ymin, xmax, ymax], fill=(0, 255, 0, 95), outline="green", width=stroke_size)
        else:
            if settings['ground_truth_transparent']:
                draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=stroke_size)
            else:
                draw.rectangle([xmin, ymin, xmax, ymax], fill=(255, 0, 0, 95), outline="red", width=stroke_size)

    def _draw_label(self, draw, prediction, settings, width):
        """
        Draw label with a box around it above the image using the given settings

        Parameters
        ----------
        draw : ImageDraw
            Drawing object
        prediction : dict
            Dictionary representing the current prediction
        settings : dict
            Dictionary containing several settings for drawing (including stroke size, colors, etc.)
        width : int
            Width of current image
        """
        data_class = prediction['class']
        xmin, ymin = prediction['xmin'], prediction['ymin']
        font_size, stroke_size = settings['font_size'], settings['stroke_size']

        color, font_color = self._get_colors(data_class, settings)
        file = font_manager.findfont('DejaVuSans')
        font = ImageFont.truetype(file, font_size)
        label = data_class
        if 'confidence' in prediction:
            label += ": {0} %".format(str(prediction['confidence']))
        text_width, text_height = font.getsize(label)

        label_coordinates = self._get_label_coordinates(text_width, text_height, width, xmin, ymin)
        draw.rectangle(label_coordinates, outline=color, fill=color, width=stroke_size)
        draw.text((label_coordinates[0], label_coordinates[1]), label, fill=font_color, font=font)

    def _get_label_coordinates(self, text_width, text_height, width, xmin, ymin):
        """
        Get label coordinates so that the label is not cut off if on the edge of the image

        Parameters
        ----------
        text_width : int
            Width of label text
        text_height : int
            Height of label text
        width : int
            Width of current image
        xmin : int
            Left x-coordinate of current bounding box
        ymin : int
            Top y-coordinate of current bounding box

        Returns
        -------
        list
            List containg xmin, ymin, xmax, ymax for label box
        """
        # check whether label expands image on top
        ymin_text = ymin - text_height
        if ymin_text < 0:
            ymin_text = 0
            ymin = text_height

        # check whether label expands image on right
        xmax_text = xmin + text_width
        if xmax_text > width:
            xmin = width - text_width
            xmax_text = width
        label_rect = [xmin, ymin_text, xmax_text, ymin]
        return label_rect

    def _get_colors(self, data_class, settings):
        """
        Get colors based on current settings (black/white or color for given data_class)

        Parameters
        ----------
        data_class : int
            Index of the current class
        settings : dict
            Dictionary containing several settings for drawing (including stroke size, colors, etc.)

        Returns
        -------
        str
            Color string representing the drawing color
        str
            Color string representing the font color
        """
        font_color = "black"
        if settings['show_colored']:
            index = settings['classes'].index(data_class)
            color = settings['colors'][index]
        else:
            color = "black"
            font_color = "white"
        return color, font_color
