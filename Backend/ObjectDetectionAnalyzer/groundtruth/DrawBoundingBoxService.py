from PIL import Image, ImageDraw, ImageFont


class DrawBoundingBoxService:
    def __init__(self):
        # taken from https://github.com/theislab/DeepCollisionalCrossSection/blob/master/palettes.py
        self.colors = [
            "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
            "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
            "#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
            "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
            "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
            "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
            "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
            "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",
            "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
            "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
            "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
            "#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
            "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
            "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
            "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
            "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58"
        ]

    def draw_bounding_boxes(self, predictions, image, classes, settings):
        with Image.open(image) as img:
            width, height = img.size

        transparent_image = Image.new('RGBA', (width, height), (255, 0, 0, 0))
        draw = ImageDraw.Draw(transparent_image)
        for prediction in predictions:
            self.draw_bounding_box(classes, draw, prediction, settings)

        # draw labels last so they are not overlapped by boxes
        if settings['show_labeled']:
            for prediction in predictions:
                self.draw_label(classes, draw, prediction, settings, width)

        return transparent_image

    def draw_bounding_box(self, classes, draw, prediction, settings):
        xmin, ymin, xmax, ymax = prediction['xmin'], prediction['ymin'], prediction['xmax'], prediction['ymax']
        color, font_color = self.get_colors(classes, prediction['class'], settings)
        draw.rectangle([xmin, ymin, xmax, ymax], outline=color, width=settings['stroke_size'])

    def draw_label(self, classes, draw, prediction, settings, width):
        data_class = prediction['class']
        xmin, ymin = prediction['xmin'], prediction['ymin']
        font_size, stroke_size = settings['font_size'], settings['stroke_size']

        color, font_color = self.get_colors(classes, data_class, settings)
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

    def get_colors(self, classes, data_class, settings):
        font_color = "black"
        if settings['show_colored']:
            color = self.colors[classes[data_class]]
        else:
            color = "black"
            font_color = "white"
        return color, font_color
