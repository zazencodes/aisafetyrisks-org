You are designing the thumbnail of an educational explainer for aisafetyrisks.org, as a static Manim image (1280x720) built with aisr_kit. It appears on YouTube and as the cover image on the website, so it must work at the size of a phone's search result.

A good thumbnail does one job: it makes someone curious enough to click. It works together with the title, which sits next to it. The title names the topic; the thumbnail shows the one surprising, concrete moment that makes the topic interesting.

Headline:
- Use the storyboard's thumbnail headline: 2 to 4 plain words that describe a concrete moment or result from the paper, as the viewer would put it ("It skipped the coin"). It must not repeat the words of the title and must not be a label or the name of a concept ("Goal misgeneralization", "When capability masks wrong goals").
- Set it in `Serif(..., weight=BOLD)` at size 100 to 130, on one or two left-aligned lines in the top-left. It should take up roughly the top 40% of the frame.
- Color one key word with the accent the video uses for the same object, so the text and the image point at the same thing.

Image:
- One simple scene from the video's visual language that shows the moment the headline names: at most 4 or 5 shapes, drawn large, with thick strokes. A viewer should grasp what happened without reading anything else.
- No labels, captions, legends, badges or panel borders. The headline is the only text.
- Keep the image clear of the headline, and leave the bottom-right corner (about 180x90 pixels) empty for YouTube's timestamp.

Truth: the moment must be something the paper reports, described the way the paper describes it (see the integrity rules). No invented drama, no alarm colors, no question marks, no digits.

Hard rules: the first line is the `# storyboard: ...` line given in the output instructions and the second is `from aisr_kit import *`, the only import; no file, network, OS or introspection access; no names or attributes starting with a double underscore; define exactly one class `Thumbnail(Scene)` whose `construct` adds mobjects with `self.add(...)` and plays no animations; no digits in any text.

After rendering, look at `out/thumbnail.jpg` as it would appear at 320x180. If the headline is not readable in a second, or the image does not show what the headline says, fix it and render again.
