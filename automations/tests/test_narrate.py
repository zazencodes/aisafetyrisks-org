"""Narration API and paid-clip caching checks, without making network requests."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx
import numpy as np

from paper_video.config import load_config
from paper_video.narrate import audio_key, narrate, synthesize
from paper_video.workdir import load_json


class NarrationTests(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config().tts

    def test_v4_request_and_lossless_audio(self):
        requests = []
        def handler(request):
            requests.append(request)
            return httpx.Response(200, content=np.full(4800, 1000, dtype='<i2').tobytes())
        with httpx.Client(base_url='https://api.elevenlabs.io', transport=httpx.MockTransport(handler)) as client:
            samples = synthesize(client, '50% — a test.', self.cfg)
        self.assertEqual(len(samples), 4800)
        self.assertEqual(samples[0], 0)
        body = json.loads(requests[0].content)
        self.assertEqual(body['model_id'], 'eleven_v4')
        self.assertEqual(body['text'], '50 percent ,  a test.')
        self.assertEqual(requests[0].url.params['output_format'], 'pcm_24000')

    def test_changed_model_or_voice_settings_invalidate_cache(self):
        key = audio_key('Test', self.cfg)
        for change in ({'model': 'eleven_v3'}, {'voice': 'other'}, {'stability': 0.8}, {'seed': 7}):
            self.assertNotEqual(key, audio_key('Test', self.cfg.model_copy(update=change)))

    def test_api_errors_fail_loudly(self):
        with httpx.Client(base_url='https://api.elevenlabs.io', transport=httpx.MockTransport(
            lambda request: httpx.Response(401, text='invalid key')
        )) as client:
            with self.assertRaisesRegex(RuntimeError, '401.*invalid key'):
                synthesize(client, 'Test', self.cfg)

    def test_resume_after_failure_does_not_pay_for_completed_clip(self):
        with TemporaryDirectory() as temp:
            wd = SimpleNamespace(audio=Path(temp) / 'audio')
            sb = SimpleNamespace(clips=lambda: [('a', 'First'), ('b', 'Second')])
            with patch('paper_video.narrate.api_key', return_value='test-key'), patch(
                'paper_video.narrate.synthesize', side_effect=[np.ones(4800), RuntimeError('interrupted')]
            ):
                with self.assertRaisesRegex(RuntimeError, 'interrupted'):
                    narrate(wd, sb, self.cfg)
            self.assertEqual(set(load_json(wd.audio / 'manifest.json')), {'a'})
            with patch('paper_video.narrate.api_key', return_value='test-key'), patch(
                'paper_video.narrate.synthesize', return_value=np.ones(7200)
            ) as generate:
                durations = narrate(wd, sb, self.cfg)
            self.assertEqual(generate.call_count, 1)
            self.assertEqual(generate.call_args.args[1], 'Second')
            self.assertEqual(durations, {'a': 0.2, 'b': 0.3})


if __name__ == '__main__':
    unittest.main()
