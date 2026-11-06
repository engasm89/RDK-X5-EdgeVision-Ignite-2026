"""Host-only mocked tests; NEVER imply the target board has been exercised."""
import importlib.util
from pathlib import Path
import struct
import io
import os
import subprocess
import tarfile
import sys
import tempfile
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    path=ROOT/relative
    spec=importlib.util.spec_from_file_location(path.stem, path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class CameraTests(unittest.TestCase):
    def test_capture_writes_only_nonempty_camera_frame(self):
        mod=load('scripts/02_camera_test.py')
        frame=types.SimpleNamespace(size=640*480*3, shape=(480,640,3))
        camera=mock.Mock()
        camera.isOpened.return_value=True
        camera.read.return_value=(True,frame)
        cv2=types.ModuleType('cv2')
        cv2.CAP_V4L2=200
        cv2.CAP_PROP_FRAME_WIDTH=3
        cv2.CAP_PROP_FRAME_HEIGHT=4
        cv2.VideoCapture=mock.Mock(return_value=camera)
        cv2.imwrite=mock.Mock(return_value=True)
        with tempfile.TemporaryDirectory() as temp, mock.patch.dict(sys.modules,{'cv2':cv2}):
            width,height=mod.capture(0,Path(temp)/'camera.png')
        self.assertEqual((width,height),(640,480))
        cv2.VideoCapture.assert_called_once_with(0,200)
        cv2.imwrite.assert_called_once()
        camera.release.assert_called_once()

    def test_camera_missing_is_error(self):
        mod=load('scripts/02_camera_test.py')
        camera=mock.Mock()
        camera.isOpened.return_value=False
        cv2=types.ModuleType('cv2')
        cv2.CAP_V4L2=200
        cv2.VideoCapture=mock.Mock(return_value=camera)
        with mock.patch.dict(sys.modules,{'cv2':cv2}), self.assertRaises(RuntimeError):
            mod.capture(0,Path('ignored.png'))
        camera.release.assert_called_once()


class LedTests(unittest.TestCase):
    def test_led_cleanup_even_if_output_fails(self):
        mod=load('scripts/05_led_test.py')
        hobot=types.ModuleType('Hobot')
        gpio=types.ModuleType('Hobot.GPIO')
        gpio.BOARD=10
        gpio.OUT=11
        gpio.LOW=0
        gpio.HIGH=1
        gpio.setwarnings=mock.Mock()
        gpio.setmode=mock.Mock()
        gpio.setup=mock.Mock()
        gpio.output=mock.Mock(side_effect=[ValueError('test controlled failure'),None])
        gpio.cleanup=mock.Mock()
        hobot.GPIO=gpio
        with mock.patch.dict(sys.modules,{'Hobot':hobot,'Hobot.GPIO':gpio}), self.assertRaises(ValueError):
            mod.blink(15,0.1,0.1)
        gpio.setup.assert_called_once_with(15,11,initial=0)
        gpio.cleanup.assert_called_once()


class SubmissionTests(unittest.TestCase):
    def test_shipped_draft_has_no_fake_submission(self):
        mod=load('scripts/06_verify_submission.py')
        self.assertNotEqual(mod.main(),0)




class EvidenceValidationTests(unittest.TestCase):
    def test_png_dimensions_rejects_invalid_header(self):
        mod=load('scripts/08_verify_submission.py')
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'fake.png'
            path.write_bytes(b'not-a-png' + b'0'*80)
            with self.assertRaises(ValueError):
                mod.png_dimensions(path)

    def test_png_dimensions_accepts_header(self):
        mod=load('scripts/08_verify_submission.py')
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'ok.png'
            path.write_bytes(b'\x89PNG\r\n\x1a\n' + struct.pack('>I', 13) + b'IHDR' + struct.pack('>II',640,480))
            self.assertEqual(mod.png_dimensions(path),(640,480))

    def test_empty_submission_links_are_not_approved(self):
        mod=load('scripts/08_verify_submission.py')
        self.assertNotEqual(mod.main(),0)



class VendorInstallTests(unittest.TestCase):
    def _install_in_temp(self, payloads):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td); (d/'scripts').mkdir(); (d/'bin').mkdir()
            script=(ROOT/'scripts/03_setup_model.sh').read_text(encoding='utf8')
            (d/'scripts/03_setup_model.sh').write_text(script)
            archive=d/'offline_fixture.tar.gz'
            with tarfile.open(archive,'w:gz') as tf:
                for name,data in payloads:
                    blob=data.encode()
                    t=tarfile.TarInfo(name=name); t.size=len(blob)
                    tf.addfile(t,io.BytesIO(blob))
            fake_curl=d/'bin/curl'
            fake_curl.write_text('#!/bin/sh\nwhile [ "$1" != "--output" ]; do shift; done\nshift\ncp "$FIXTURE_ARCHIVE" "$1"\n')
            fake_curl.chmod(0o755)
            env=os.environ.copy(); env['PATH']=str(d/'bin')+':'+env['PATH']; env['FIXTURE_ARCHIVE']=str(archive)
            r=subprocess.run(['bash',str(d/'scripts/03_setup_model.sh')], env=env,capture_output=True,text=True)
            installed=(d/'vendor/yolo11m_demo/runtime/python/main.py').exists()
            return r,installed

    def test_installs_offline_fixture_safely(self):
        r,installed=self._install_in_temp([('yolo11m_demo/runtime/python/main.py','print("demo")')])
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(installed)

    def test_rejects_traversal_from_vendor_archive(self):
        r,installed=self._install_in_temp([('yolo11m_demo/../../bad.txt','x'),('yolo11m_demo/runtime/python/main.py','x')])
        self.assertNotEqual(r.returncode,0)
        self.assertFalse(installed)

    def test_on_device_runner_refuses_host_machine(self):
        r=subprocess.run(['bash',str(ROOT/'scripts/04_run_yolo.sh'),'0'],capture_output=True,text=True)
        # Expected on a standard x86 CI host, not an RDK board.
        if not Path('/proc/device-tree/model').exists():
            self.assertEqual(r.returncode,3)
            self.assertIn('device tree',r.stderr)

    def test_on_device_runner_rejects_invalid_camera_argument(self):
        r=subprocess.run(['bash',str(ROOT/'scripts/04_run_yolo.sh'),'not-an-index'],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)

if __name__=='__main__':
    unittest.main()
