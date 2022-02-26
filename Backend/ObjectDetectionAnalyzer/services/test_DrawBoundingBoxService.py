from unittest import TestCase
from unittest.mock import patch, ANY

from PIL import Image, ImageDraw

from ObjectDetectionAnalyzer.services.DrawBoundingBoxService import DrawBoundingBoxService


class TestDrawBoundingBoxService(TestCase):
    """
    Test DrawBoundingBoxService
    """

    def setUp(self):
        self.draw_bounding_box_service = DrawBoundingBoxService()
        self.settings = {
            'stroke_size': 15,
            'show_colored': True,
            'show_labeled': True,
            'font_size': 35,
            'classes': ['class1', 'class2'],
            'colors': ['color1', 'color2']
        }
        self.classes = {'class1': 0, 'class2': 1, 'class3': 2}
        self.predictions = [{'class': 'class1', 'confidence': 50, 'xmin': 50, 'ymin': 50, 'xmax': 75, 'ymax': 75},
                            {'class': 'class1', 'confidence': 25, 'xmin': 25, 'ymin': 25, 'xmax': 60, 'ymax': 60},
                            {'class': 'class2', 'confidence': 10, 'xmin': 10, 'ymin': 30, 'xmax': 30, 'ymax': 75}]

    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_label')
    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_bounding_box')
    @patch('PIL.Image.open')
    def test_draw_bounding_boxes(self, open, draw_bounding_box, draw_label):
        open.return_value = Image.new('RGBA', (100, 100), (255, 0, 0, 0))

        self.draw_bounding_box_service.draw_bounding_boxes(self.predictions, "img.jpg", self.settings)

        self.assertEqual(draw_bounding_box.call_count, 3)
        self.assertEqual(draw_label.call_count, 3)

    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_label')
    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_bounding_box')
    def test_draw_bounding_boxes_without_create(self, draw_bounding_box, draw_label):
        image = Image.new('RGBA', (1000, 1000), (255, 0, 0, 0))
        self.draw_bounding_box_service.draw_bounding_boxes(self.predictions, image, self.settings, False)

        self.assertEqual(draw_bounding_box.call_count, 3)
        self.assertEqual(draw_label.call_count, 3)

    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_gt_bounding_box')
    @patch('PIL.Image.open')
    def test_draw_gt_boxes(self, open, draw_gt_bounding_box):
        image = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
        open.return_value = image
        gts = [{'class': 'class1', 'confidence': 50, 'xmin': 50, 'ymin': 50, 'xmax': 75, 'ymax': 75},
               {'class': 'class1', 'confidence': 25, 'xmin': 25, 'ymin': 25, 'xmax': 60, 'ymax': 60},
               {'class': 'class2', 'confidence': 10, 'xmin': 10, 'ymin': 30, 'xmax': 30, 'ymax': 75}]

        result = self.draw_bounding_box_service.draw_gt_boxes(gts, image, self.settings)

        self.assertEqual(result, image)
        self.assertEqual(draw_gt_bounding_box.call_count, 3)

    @patch('PIL.ImageDraw.ImageDraw.rectangle')
    def test_draw_gt_bounding_box(self, rectangle):
        image = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        gt = {'matched': True, 'confidence': 50, 'xmin': 50, 'ymin': 50, 'xmax': 75, 'ymax': 75}

        self.draw_bounding_box_service.draw_gt_bounding_box(draw, gt, self.settings)

        rectangle.assert_called_with([50, 50, 75, 75], fill=(0, 255, 0, 95), outline="green", width=15)

    @patch('PIL.ImageDraw.ImageDraw.rectangle')
    def test_draw_gt_bounding_box_no_match(self, rectangle):
        image = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        gt = {'matched': False, 'confidence': 50, 'xmin': 50, 'ymin': 50, 'xmax': 75, 'ymax': 75}

        self.draw_bounding_box_service.draw_gt_bounding_box(draw, gt, self.settings)

        rectangle.assert_called_with([50, 50, 75, 75], fill=(255, 0, 0, 95), outline="red", width=15)

    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_label')
    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_bounding_box')
    @patch('PIL.Image.open')
    def test_draw_bounding_boxes_not_labeled(self, open, draw_bounding_box, draw_label):
        open.return_value = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
        self.settings['show_labeled'] = False

        self.draw_bounding_box_service.draw_bounding_boxes(self.predictions, "img.jpg", self.settings)

        self.assertEqual(draw_bounding_box.call_count, 3)
        self.assertEqual(draw_label.call_count, 0)

    @patch('PIL.ImageDraw.ImageDraw.rectangle')
    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.get_colors')
    def test_draw_bounding_box(self, get_colors, rectangle):
        get_colors.return_value = ("black", "white")

        transparent_image = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
        draw = ImageDraw.Draw(transparent_image)
        prediction = {'class': 'class1', 'confidence': 50, 'xmin': 50, 'ymin': 50, 'xmax': 75, 'ymax': 75}

        self.draw_bounding_box_service.draw_bounding_box(draw, prediction, self.settings)

        rectangle.assert_called_with([50, 50, 75, 75], outline="black", width=15)

    @patch('PIL.ImageDraw.ImageDraw.text')
    @patch('PIL.ImageDraw.ImageDraw.rectangle')
    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.get_label_coordinates')
    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.get_colors')
    def test_draw_label(self, get_colors, get_label_coordinates, rectangle, text):
        get_colors.return_value = ("black", "white")
        get_label_coordinates.return_value = [50, 40, 60, 50]

        transparent_image = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
        draw = ImageDraw.Draw(transparent_image)
        prediction = {'class': 'class1', 'confidence': 50, 'xmin': 50, 'ymin': 50, 'xmax': 75, 'ymax': 75}

        self.draw_bounding_box_service.draw_label(draw, prediction, self.settings, 100)

        rectangle.assert_called_with([50, 40, 60, 50], outline="black", fill="black", width=15)
        text.assert_called_with((50, 40), "class1: 50 %", fill="white", font=ANY)

    def test_get_label_coordinates(self):
        label_rect = self.draw_bounding_box_service.get_label_coordinates(50, 10, 100, 50, 50)

        self.assertEqual(label_rect, [50, 40, 100, 50])

    def test_get_label_coordinates_expand_top(self):
        label_rect = self.draw_bounding_box_service.get_label_coordinates(50, 10, 100, 50, 5)

        self.assertEqual(label_rect, [50, 0, 100, 10])

    def test_get_label_coordinates_expand_right(self):
        label_rect = self.draw_bounding_box_service.get_label_coordinates(60, 10, 100, 50, 50)

        self.assertEqual(label_rect, [40, 40, 100, 50])

    def test_get_label_coordinates_expand_top_right(self):
        label_rect = self.draw_bounding_box_service.get_label_coordinates(60, 10, 100, 50, 5)

        self.assertEqual(label_rect, [40, 0, 100, 10])

    def test_get_colors_colored(self):
        color, font_color = self.draw_bounding_box_service.get_colors('class1', self.settings)

        self.assertEqual(color, "color1")
        self.assertEqual(font_color, "black")

    def test_get_colors_colored_class2(self):
        color, font_color = self.draw_bounding_box_service.get_colors('class2', self.settings)

        self.assertEqual(color, "color2")
        self.assertEqual(font_color, "black")

    def test_get_colors_not_colored(self):
        self.settings['show_colored'] = False
        color, font_color = self.draw_bounding_box_service.get_colors('class1', self.settings)

        self.assertEqual(color, "black")
        self.assertEqual(font_color, "white")
