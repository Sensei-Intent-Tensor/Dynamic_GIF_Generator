#!/usr/bin/env python3
"""
Dynamic GIF Generator Server
Serves animated GIF face images based on URL seed parameters
"""

from flask import Flask, Response, request
from flask_cors import CORS
import os
from io import BytesIO

try:
    import cairosvg
    HAS_CAIRO = True
except ImportError:
    HAS_CAIRO = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from generate_face_gif import generate_svg

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Simple info page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dynamic GIF Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 { color: #333; }
            code {
                background: #f0f0f0;
                padding: 4px 8px;
                border-radius: 4px;
                font-family: monospace;
            }
            .example {
                margin: 20px 0;
                padding: 15px;
                background: #f9f9f9;
                border-left: 4px solid #4CAF50;
            }
            img {
                border: 2px solid #ddd;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬 Dynamic GIF Generator</h1>
            <p>Generates animated GIF face images based on seed values.</p>
            
            <h2>Usage</h2>
            <div class="example">
                <code>/face.gif?seeds=SEED1,SEED2,SEED3</code>
            </div>
            
            <h2>Examples</h2>
            <p><strong>Seeds: rocket, sunset, ocean</strong></p>
            <img src="/face.gif?seeds=rocket,sunset,ocean" width="150">
            <p><code>/face.gif?seeds=rocket,sunset,ocean</code></p>
            
            <p><strong>Seeds: red, blue (faster)</strong></p>
            <img src="/face.gif?seeds=red,blue&duration=500" width="150">
            <p><code>/face.gif?seeds=red,blue&duration=500</code></p>
            
            <h2>API</h2>
            <p><strong>GET /face.gif</strong></p>
            <ul>
                <li><strong>Parameter:</strong> <code>seeds</code> (comma-separated strings, required)</li>
                <li><strong>Parameter:</strong> <code>duration</code> (milliseconds per frame, optional, default: 1000)</li>
                <li><strong>Returns:</strong> Animated GIF (image/gif)</li>
            </ul>
            
            <h2>Features</h2>
            <ul>
                <li>Deterministic generation (same seeds = same GIF)</li>
                <li>14,400 possible combinations per frame</li>
                <li>Animated GIF format (loops forever)</li>
                <li>Works everywhere (email, social, messengers)</li>
                <li>True "forever stamp"</li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/face.gif')
def serve_face_gif():
    """Generate and serve animated GIF based on seed parameters"""
    seeds_param = request.args.get('seeds', 'default')
    duration = int(request.args.get('duration', 1000))  # milliseconds per frame
    
    if not HAS_CAIRO:
        return Response(
            "GIF generation requires cairosvg. Install: pip install cairosvg",
            status=500,
            mimetype='text/plain'
        )
    
    if not HAS_PIL:
        return Response(
            "GIF generation requires Pillow. Install: pip install pillow",
            status=500,
            mimetype='text/plain'
        )
    
    try:
        # Parse seeds
        seeds = [s.strip() for s in seeds_param.split(',')]
        
        if not seeds or not seeds[0]:
            return Response(
                "Error: 'seeds' parameter required (comma-separated list)",
                status=400,
                mimetype='text/plain'
            )
        
        # Generate PNG frames for each seed
        frames = []
        for seed in seeds:
            svg_content = generate_svg(seed)
            png_data = cairosvg.svg2png(
                bytestring=svg_content.encode('utf-8'),
                output_width=400,
                output_height=480
            )
            img = Image.open(BytesIO(png_data))
            frames.append(img)
        
        # Create animated GIF
        output = BytesIO()
        frames[0].save(
            output,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,  # Loop forever
            optimize=True
        )
        output.seek(0)
        
        return Response(output.read(), mimetype='image/gif')
        
    except Exception as e:
        return Response(
            f"Error generating GIF: {str(e)}",
            status=500,
            mimetype='text/plain'
        )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🎬 Dynamic GIF Generator Starting...")
    print(f"📍 Server running on port: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
