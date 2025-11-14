#!/usr/bin/env python3
"""
GIF Face Generator
Generates unique face images as frames for animated GIFs
"""

import hashlib

# Component definitions
BACKGROUNDS = ['#F0F8FF', '#FAEBD7', '#E6E6FA', '#F5F5DC', '#FFF0F5', '#F0FFF0']
FACE_COLORS = ['#FFD700', '#90EE90', '#ADD8E6', '#FFB6C1', '#FFA07A', '#87CEEB']

HEADS = [
    '<circle cx="50" cy="60" r="30" stroke="#444" stroke-width="1"/>',
    '<ellipse cx="50" cy="60" rx="25" ry="32" stroke="#444" stroke-width="1"/>',
    '<ellipse cx="50" cy="60" rx="32" ry="25" stroke="#444" stroke-width="1"/>',
    '<rect x="20" y="30" width="60" height="60" rx="15" stroke="#444" stroke-width="1"/>'
]

EYES = [
    '''<g fill="#333333">
        <circle cx="40" cy="55" r="3"/>
        <circle cx="60" cy="55" r="3"/>
    </g>''',
    '''<g>
        <circle cx="40" cy="55" r="5" fill="white" stroke="#333333" stroke-width="1"/>
        <circle cx="40" cy="55" r="2.5" fill="#333333"/>
        <circle cx="60" cy="55" r="5" fill="white" stroke="#333333" stroke-width="1"/>
        <circle cx="60" cy="55" r="2.5" fill="#333333"/>
    </g>''',
    '''<g stroke="#333333" stroke-width="2" stroke-linecap="round" fill="none">
        <path d="M 35 58 Q 40 52 45 58" />
        <path d="M 55 58 Q 60 52 65 58" />
    </g>''',
    '''<g>
        <circle cx="40" cy="55" r="3" fill="#333333"/>
        <path d="M 55 58 Q 60 52 65 58" stroke="#333333" stroke-width="2" stroke-linecap="round" fill="none"/>
    </g>''',
    '''<g>
        <circle cx="40" cy="55" r="5" fill="white" stroke="#333333" stroke-width="1"/>
        <circle cx="37" cy="55" r="2.5" fill="#333333"/>
        <circle cx="60" cy="55" r="5" fill="white" stroke="#333333" stroke-width="1"/>
        <circle cx="63" cy="55" r="2.5" fill="#333333"/>
    </g>'''
]

MOUTHS = [
    '<path d="M 40 75 Q 50 85 60 75" stroke="#333333" fill="none" stroke-width="2" stroke-linecap="round"/>',
    '<path d="M 40 72 C 40 82, 60 82, 60 72 Z" fill="#333333"/>',
    '<ellipse cx="50" cy="78" rx="5" ry="4" fill="#333333"/>',
    '<path d="M 40 75 Q 45 80 50 75 T 60 75" stroke="#333333" fill="none" stroke-width="2" stroke-linecap="round"/>',
    '<line x1="40" y1="78" x2="60" y2="78" stroke="#333333" stroke-width="2" stroke-linecap="round"/>'
]

ACCESSORIES = [
    '',
    '''<g fill="#222222">
        <rect x="35" y="15" width="30" height="20" />
        <rect x="30" y="35" width="40" height="5" />
    </g>''',
    '''<g fill="#D22B2B">
        <path d="M 50 92 L 40 87 L 40 97 Z" />
        <path d="M 50 92 L 60 87 L 60 97 Z" />
        <circle cx="50" cy="92" r="3" fill="#A01B1B" />
    </g>''',
    '''<g stroke="#333333" stroke-width="1.5" fill="none">
        <circle cx="40" cy="55" r="8"/>
        <circle cx="60" cy="55" r="8"/>
        <path d="M 48 55 Q 50 50 52 55"/>
    </g>'''
]

def seed_to_components(seed):
    """Convert seed to component indices via SHA-256"""
    hash_bytes = hashlib.sha256(seed.encode()).digest()
    
    return {
        'background': BACKGROUNDS[hash_bytes[0] % len(BACKGROUNDS)],
        'face_color': FACE_COLORS[hash_bytes[1] % len(FACE_COLORS)],
        'head': HEADS[hash_bytes[2] % len(HEADS)],
        'eyes': EYES[hash_bytes[3] % len(EYES)],
        'mouth': MOUTHS[hash_bytes[4] % len(MOUTHS)],
        'accessory': ACCESSORIES[hash_bytes[5] % len(ACCESSORIES)]
    }

def generate_svg(seed="default"):
    """Generate SVG markup for a face"""
    components = seed_to_components(seed)
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120">
    <style>
        text {{
            font-family: sans-serif;
            font-weight: bold;
            fill: #333333;
        }}
    </style>

    <rect width="100%" height="100%" fill="{components['background']}"/>
    <rect x="2" y="2" width="96" height="116" fill="none" stroke="#666" stroke-width="0.5" stroke-dasharray="2 2" />

    <text x="5" y="12" font-size="8">USA</text>
    <text x="50" y="115" font-size="10" text-anchor="middle">FOREVER</text>

    <g fill="{components['face_color']}">
        {components['head']}
    </g>

    {components['eyes']}

    {components['mouth']}

    {components['accessory']}
</svg>'''
