"""The privacy fixture has actual structured metadata, not a suggestive filename."""
import unittest
import re
from pathlib import Path
try:
    from PIL import Image
except ModuleNotFoundError:
    Image = None
ROOT = Path(__file__).resolve().parents[2]


class AvatarPrivacyFixtureTests(unittest.TestCase):
    @unittest.skipIf(Image is None, 'Pillow is needed to inspect structured EXIF fixtures')
    def test_all_three_formats_have_actual_gps_and_all_eight_orientation_tags(self):
        for ext in ['png','jpg','webp']:
            for orientation in range(1,9):
                path=ROOT/f'tests/fixtures/avatar/orientation-{orientation}.{ext}'
                with self.subTest(file=path.name), Image.open(path) as image:
                    self.assertEqual(image.size,(96,64))
                    exif=image.getexif()
                    self.assertEqual(exif[274],orientation)
                    self.assertEqual(exif[271],'FixtureCamera')
                    gps=exif.get_ifd(34853)
                    self.assertEqual((gps[1],gps[3]),('N','E'))
                    self.assertEqual(tuple(float(v) for v in gps[2]),(0,0,0))

    def test_runtime_import_path_has_no_network_camera_or_permission_requests(self):
        pending=['core/quest/avatar_import.gd','core/quest/custom_avatar.gd']
        seen=set()
        while pending:
            name=pending.pop()
            if name in seen:continue
            seen.add(name)
            text=(ROOT/name).read_text()
            self.assertNotRegex(text,r'\b(?:HTTPRequest|HTTPClient|WebSocketPeer|TCPServer|PacketPeerUDP|JavaClassWrapper)\b')
            self.assertNotRegex(text,r'(?:request_permission|request_permissions|shell_open|execute)\s*\(')
            self.assertNotIn('SYSTEM_DIR_PICTURES',text)
            self.assertNotIn('store_string(path',text)
            pending.extend(re.findall(r'preload\("res://([^\"]+\.gd)"\)',text))
        self.assertIn('core/quest/avatar_image.gd',seen)
        self.assertIn('core/quest/avatar_preview.gd',seen)
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
