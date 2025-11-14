# Dynamic_GIF_Generator
Dynamic_GIF_Generator that creates dynamic GIF for remote controlled marketing

# Dynamic_GIF_Generator

Generates animated GIF images with cycling faces based on URL seed parameters.

## What This Does

Server-side animated GIF generation with deterministic output:
- `/face.gif?seeds=rocket,sunset,ocean` → Returns animated GIF cycling through 3 faces
- Same seeds = same GIF (always)
- Different seeds = different GIF
- Works everywhere (email, social media, messengers, all platforms)

## Deployment

### Render Configuration:
- **Build Command:** `pip install flask cairosvg pillow`
- **Start Command:** `python server.py`
- **Runtime:** Python 3

### Usage After Deploy:

```
https://your-app.onrender.com/face.gif?seeds=rocket,sunset,ocean
https://your-app.onrender.com/face.gif?seeds=user123,user456
https://your-app.onrender.com/face.gif?seeds=morning,noon,evening,night
```

## API

### GET /face.gif
**Parameters:**
- `seeds` (string, required) - Comma-separated list of seed values. Each generates one frame.
- `duration` (integer, optional) - Milliseconds per frame. Default: 1000 (1 second)

**Returns:** Animated GIF (image/gif)

**Examples:**
- `/face.gif?seeds=a,b,c` - 3 frames cycling every 1 second
- `/face.gif?seeds=red,blue&duration=2000` - 2 frames cycling every 2 seconds

## Technical Details

- **Components:** 14,400 possible face combinations per frame
- **Method:** SHA-256 deterministic hashing
- **Output:** Animated GIF, loops forever
- **Format:** Optimized GIF with transparency

## Features

- Zero JavaScript required
- Deterministic generation
- Infinite unique combinations
- Universal compatibility
- Works as email attachments, social uploads, messenger sends
- True "forever stamp" - cycles automatically everywhere

## License

MIT
