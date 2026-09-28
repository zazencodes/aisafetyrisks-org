# Open-source launch

Scope: publish the working repository at https://github.com/zazencodes/aisafetyrisks-org,
including the video pipeline, agent workflow, Manim kit and example source artifacts.
Use GPL-3.0-only for original code. Production approval remains with Alexander.

1. Update About to make running the pipeline the main support action, with a rough estimate
   of one five-hour Claude session per video and links to the repository and contributor guide.
2. Commit the current working pipeline and paper artifacts, preserving existing Git history.
3. Add the GPL-3.0 license, contributor setup and submission instructions, and third-party notices.
4. Scan all publishable files and Git history for credentials. Keep PDFs, generated media,
   local environments and credentials out of Git.
5. Verify dependency installation, the CLI, backlog validation, a local scene render and site
   build from a clean snapshot. Full video generation is contributed through the paper workflow.
6. Push the reviewed source and change the GitHub repository from private to public. Verify
   anonymous access to the repository, license and contributor guide.

Website deployment is a separate action from making the source repository public.
