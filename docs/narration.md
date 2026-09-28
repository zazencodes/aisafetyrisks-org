# ElevenLabs narration

`paper-video narrate <slug>` generates one WAV for each storyboard beat and roadmap checkpoint.
The configured model is Eleven v4 (`eleven_v4`). The pipeline requests mono 24 kHz PCM from
ElevenLabs, saves it as WAV, and records clip duration, model and voice in
`automations/works/<slug>/audio/manifest.json`. The audio directory is ignored by Git. The
assembly step places those source WAVs at the times recorded by the Manim scenes, so captions,
speech and visuals stay aligned.

## Set up access

1. In the intended ElevenLabs account, create a dedicated API key under **Developers → API
   Keys**. Grant **Text to Speech** access. The project's current key also has
   **Voices: Read** and **Models: Access**, with a 25,000-credit limit per credit refresh period;
   other endpoints have no access.
2. Put `ELEVENLABS_API_KEY=<key>` in the repository root's `.env`, then run `chmod 600 .env`.
   This file is ignored by Git. Keep the key out of `automations/config.toml`, logs and commits.
3. Run `uv sync --frozen`. The model ID, voice ID, stability, similarity, seed and request timeout
   are all required in `[tts]` of `automations/config.toml`.

The current voice is Jarnathan - Confident and Versatile (`c6SfcYrb2t09NHXiT80T`), selected
by the maintainer after reviewing the voice library. The first Eleven v4 publication used Roger
(`CwhRBWXzGAHq8TQ4Fs17`) because it was already selected in the maintainer's text-to-speech
page; it had not undergone a comparative voice review. Use a voice's **Copy voice ID** control
in ElevenLabs to get the exact ID. Audition it with Eleven v4,
since voices can sound different across models. The v4 model supports stability and similarity
settings; this pipeline uses 0.5 and 0.75 respectively.

## Generate or change a voice

From the repository root, after the storyboard passes its check:

```sh
uv run --frozen paper-video check <slug> storyboard
uv run --frozen paper-video narrate <slug>
uv run --frozen paper-video render <slug>
```

Changing `[tts].voice`, model, stability, similarity or seed invalidates the audio cache. The
next `narrate` call regenerates every affected clip and consumes ElevenLabs credits. Unchanged
clips are reused. Each completed clip is recorded immediately, so rerunning after an interruption
does not regenerate clips already completed with the same settings. Review the WAVs for
pronunciation and delivery before final publication; adjust the source narration or voice settings
and rerun if necessary. A storyboard edit must still pass the storyboard and science checks.

Narration duration changes scene timing. Follow the render command's list of scenes needing work
or a current visual review, using the scene brief and contact sheet for each one. Continue until
`paper-video render <slug>` exits successfully. Then:

```sh
uv run --frozen paper-video assemble <slug>
uv run --frozen paper-video site <slug>
uv run --frozen paper-video youtube <slug>
uv run --frozen paper-video report <slug>
```

Read the new `out/captions.vtt` from start to finish and watch the assembled video. Check that
speech, scene changes and captions agree; that the opening establishes the risk and paper; and
that the closing states the evidence boundary. `paper-video site` must follow the final assembly:
it refreshes the page's chapter times and hashed media mirror. It writes the page as a draft, even
when updating a published paper. Check that its science reviews remain current. A voice-only
change does not alter the reviewed storyboard or page prose, but any prose edit needs a new review.

For a reviewed paper, stop at human review unless the user explicitly asks to publish. When
publication is authorized, follow [the approval and deployment sequence](deployment.md#finish-and-publish-a-reviewed-paper):
`paper-video approve <slug>`, then `cd site && npm run deploy`. Verify the live page references
the new video key, and check the exact video URL returns HTTP 200, `video/mp4`, and byte-range
support. The prior hashed video remains available in R2 for existing cached links.
