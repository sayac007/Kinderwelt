"""The privacy fixture has actual structured metadata, not a suggestive filename."""
import unittest
from pathlib import Path
try:
    from PIL import Image
except ModuleNotFoundError:
    Image = None
ROOT = Path(__file__).resolve().parents[2]


class AvatarPrivacyFixtureTests(unittest.TestCase):
    @unittest.skipIf(Image is None, 'Pillow is optional; install it to verify structured EXIF fixture data')
    def test_synthetic_png_really_contains_gps_camera_and_transparency(self):
        path = ROOT / 'tests/fixtures/avatar/gps-source.png'
        self.assertLess(path.stat().st_size, 4096)
        with Image.open(path) as image:
            self.assertEqual(image.format, 'PNG')
            self.assertEqual(image.getchannel('A').getextrema(), (0, 255))
            exif = image.getexif()
            self.assertEqual(exif[271], 'FixtureCamera')
            gps = exif.get_ifd(34853)
            self.assertEqual((gps[1], gps[3]), ('N', 'E'))
            self.assertEqual(tuple(float(v) for v in gps[2]), (0, 0, 0))
            self.assertEqual(tuple(float(v) for v in gps[4]), (0, 0, 0))
