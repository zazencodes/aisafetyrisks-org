"""Source audio must retain scene timing even when rendered scene tracks are incomplete."""
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

import numpy as np
import soundfile as sf

from paper_video.media import assemble, narration_track, probe
from paper_video.narrate import SAMPLE_RATE


class AssemblyTests(unittest.TestCase):
    def test_source_narration_and_gaps_survive_scene_concatenation(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            video = root / 'scene.mp4'
            # Deliberately silent scene audio: the master must use source narration.
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                            'color=c=black:s=32x32:r=10:d=2', '-an', '-c:v', 'libx264',
                            str(video)], check=True)
            sources = []
            for i, frequency in enumerate((440, 660)):
                path = root / f'{i}.wav'
                time = np.arange(SAMPLE_RATE // 2) / SAMPLE_RATE
                sf.write(path, 0.1 * np.sin(2 * np.pi * frequency * time), SAMPLE_RATE, subtype='PCM_16')
                sources.append(path)
            dest = root / 'master.mp4'
            assemble([video, video], dest, [(0, sources[0]), (2, sources[1])], 4)
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(dest), '-vn', '-ac', '1',
                                  '-ar', str(SAMPLE_RATE), '-f', 'f32le', 'pipe:1'],
                                 capture_output=True, check=True).stdout
            samples = np.frombuffer(raw, dtype='<f4')
            rms = lambda lo, hi: np.sqrt(np.mean(samples[int(lo*SAMPLE_RATE):int(hi*SAMPLE_RATE)]**2))
            self.assertGreater(rms(0.1, 0.3), 0.01)
            self.assertLess(rms(0.8, 1.8), 0.001)
            self.assertGreater(rms(2.1, 2.3), 0.01)
            self.assertAlmostEqual(probe(dest)['duration'], 4, delta=0.05)

    def test_overlapping_narration_fails(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source.wav'
            sf.write(source, np.zeros(SAMPLE_RATE), SAMPLE_RATE, subtype='PCM_16')
            with self.assertRaisesRegex(ValueError, 'overlaps'):
                narration_track([(0, source), (0.5, source)], 2, root / 'track.wav')


if __name__ == '__main__':
    unittest.main()
