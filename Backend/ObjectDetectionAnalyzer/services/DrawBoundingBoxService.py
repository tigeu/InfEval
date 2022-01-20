from PIL import Image, ImageDraw, ImageFont


class DrawBoundingBoxService:
    def draw_bounding_boxes(self, predictions, image, settings):
        predictions = list(filter(lambda pred: pred['class'] in settings['classes'], predictions))
        with Image.open(image) as img:
            width, height = img.size

        transparent_image = Image.new('RGBA', (width, height), (255, 0, 0, 0))
        draw = ImageDraw.Draw(transparent_image)

        for prediction in predictions:
            self.draw_bounding_box(draw, prediction, settings)

        # draw labels last so they are not overlapped by boxes
        if settings['show_labeled']:
            for prediction in predictions:
                self.draw_label(draw, prediction, settings, width)

        return transparent_image

    def draw_bounding_box(self, draw, prediction, settings):
        xmin, ymin, xmax, ymax = prediction['xmin'], prediction['ymin'], prediction['xmax'], prediction['ymax']
        color, font_color = self.get_colors(prediction['class'], settings)
        draw.rectangle([xmin, ymin, xmax, ymax], outline=color, width=settings['stroke_size'])

    def draw_label(self, draw, prediction, settings, width):
        data_class = prediction['class']
        xmin, ymin = prediction['xmin'], prediction['ymin']
        font_size, stroke_size = settings['font_size'], settings['stroke_size']

        color, font_color = self.get_colors(data_class, settings)
        font = ImageFont.truetype("arial", font_size)
        label = data_class
        if 'confidence' in prediction:
            label += ": {0} %".format(str(prediction['confidence']))
        text_width, text_height = font.getsize(label)

        label_coordinates = self.get_label_coordinates(text_width, text_height, width, xmin, ymin)
        draw.rectangle(label_coordinates, outline=color, fill=color, width=stroke_size)
        draw.text((label_coordinates[0], label_coordinates[1]), label, fill=font_color, font=font)

    def get_label_coordinates(self, text_width, text_height, width, xmin, ymin):
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

    def get_colors(self, data_class, settings):
        font_color = "black"
        if settings['show_colored']:
            index = settings['classes'].index(data_class)
            color = settings['colors'][index]
        else:
            color = "black"
            font_color = "white"
        return color, font_color
