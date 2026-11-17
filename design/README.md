# Design

The approved JobMatcher designs, as working HTML pages. They are the reference for the React app in `frontend/`.

## Open the previews

Open `previews/index.html` in a browser. The pages link to each other like the real app:

| Page | File |
|---|---|
| Landing | `previews/index.html` |
| Sign in / sign up | `previews/signin.html`, `previews/signup.html` |
| Add your CV | `previews/upload.html` |
| Check your details | `previews/review.html` |
| Matches, Saved, Applied tracker | `previews/dashboard.html` (`#matches`, `#saved`, `#applied`) |
| Prepare application | `previews/apply.html` |
| Profile | `previews/profile.html` |

All names and data in the previews are sample data.

## Design system

- Colours: page `#F6F5FB`, card `#FFFFFF`, tint `#E9E5FF`, lavender `#CDBFFF`, accent `#FF7F45`, peach `#FFE3D3`, ink `#1E1C2B`, muted `#5E5C6E`, line `#DAD6EA`.
- Fonts: Anton for display, Outfit for text.
- Easing: `cubic-bezier(.16,1,.3,1)`, and `cubic-bezier(.34,1.45,.64,1)` for springs.
- Identity: the filled cup shows the match score; the logo (`jobmatcher-logo.svg`) is a CV and a job overlapping, with the overlap in orange.
- Illustrations: Open Peeps by Pablo Stanley (CC0).

## Source

`source/` holds the Python scripts that generated the previews (`dash5.py`, `apply4.py`, `profile2.py`, `upload.py`, `review2.py`, `auth2.py`) and their CSS, followed by `polish.py`. They are kept for reference; they expect the folder layout they were written in.
