"""Generate the original, copyright-safe artwork used by the app.

Every image in ``assets/`` (except the Chicken McNugget Theorem figure and the
author photo) is drawn programmatically by this script using Pillow. Nothing is
copied or derived from photographs or other websites, so the artwork carries no
third-party copyright.

Run from the repository root:

    python scripts/generate_images.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

# Where generated images are written (repo_root/assets).
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

# Supersampling factor: draw large, then downscale for smooth edges.
SS = 4


def _blob_outline(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    seed: int,
    points: int = 140,
    wobble: float = 0.16,
) -> list[tuple[float, float]]:
    """Build an irregular, nugget-like closed outline around an ellipse.

    The outline is an ellipse whose radius is perturbed by a few random-phase,
    low-frequency sine waves, which produces the organic "hand-formed" edge
    that real nuggets have.

    Args:
        cx: X coordinate of the blob center, in pixels.
        cy: Y coordinate of the blob center, in pixels.
        rx: Base horizontal radius, in pixels.
        ry: Base vertical radius, in pixels.
        seed: Seed for the pseudo-random wobble (fixed => reproducible art).
        points: Number of outline vertices; more points = smoother edge.
        wobble: Relative amplitude of the edge perturbation (0..~0.3).

    Returns:
        List of (x, y) vertex tuples describing a closed polygon.
    """
    rng = random.Random(seed)
    # 3 sine components with random phase/frequency give a smooth wobble.
    waves = [
        (rng.uniform(0.5, 1.0) * wobble, rng.randint(2, 3), rng.uniform(0, math.tau)),
        (rng.uniform(0.3, 0.6) * wobble, rng.randint(4, 5), rng.uniform(0, math.tau)),
        (rng.uniform(0.15, 0.3) * wobble, rng.randint(6, 9), rng.uniform(0, math.tau)),
    ]
    pts: list[tuple[float, float]] = []
    for i in range(points):
        t = math.tau * i / points
        r_scale = 1.0 + sum(a * math.sin(f * t + p) for a, f, p in waves)
        pts.append((cx + rx * r_scale * math.cos(t), cy + ry * r_scale * math.sin(t)))
    return pts


def _draw_nugget(size: int, seed: int) -> Image.Image:
    """Draw a single golden-fried nugget on a transparent background.

    Layers, bottom to top: soft drop shadow, dark crust base, mid golden body,
    lighter top face, crumb speckles (dark + light), and a soft highlight.

    Args:
        size: Output image is size x size pixels (RGBA).
        seed: Random seed controlling the nugget's unique shape and crumbs.

    Returns:
        RGBA ``PIL.Image.Image`` of the nugget.
    """
    s = size * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rng = random.Random(seed * 7919 + 13)

    cx, cy = s / 2, s / 2
    rx, ry = s * 0.36, s * 0.28

    # --- drop shadow -------------------------------------------------------
    shadow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).polygon(
        _blob_outline(cx, cy + s * 0.06, rx * 1.02, ry * 1.02, seed), fill=(60, 35, 8, 90)
    )
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(s * 0.02)))

    # --- crust: darker outer edge -----------------------------------------
    draw.polygon(_blob_outline(cx, cy, rx, ry, seed), fill=(166, 100, 28, 255))
    # --- body: main golden layer, slightly inset ---------------------------
    draw.polygon(_blob_outline(cx, cy - s * 0.005, rx * 0.965, ry * 0.955, seed), fill=(214, 148, 51, 255))
    # --- top face: lighter fried batter ------------------------------------
    draw.polygon(_blob_outline(cx, cy - s * 0.02, rx * 0.9, ry * 0.86, seed), fill=(233, 178, 84, 255))

    # --- crumb texture ------------------------------------------------------
    # Dark toasted crumbs and light batter crumbs scattered inside the body.
    for _ in range(int(s * 1.5)):
        t = rng.uniform(0, math.tau)
        rr = rng.uniform(0, 0.88)
        px = cx + rx * 0.9 * rr * math.cos(t)
        py = cy - s * 0.02 + ry * 0.86 * rr * math.sin(t)
        crumb = rng.uniform(s * 0.003, s * 0.011)
        if rng.random() < 0.55:
            color = (
                rng.randint(150, 185), rng.randint(88, 118), rng.randint(24, 48),
                rng.randint(70, 160),
            )
        else:
            color = (
                rng.randint(238, 252), rng.randint(196, 222), rng.randint(120, 160),
                rng.randint(60, 140),
            )
        draw.ellipse([px - crumb, py - crumb, px + crumb, py + crumb], fill=color)

    # --- soft top-left highlight -------------------------------------------
    hl = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(hl).polygon(
        _blob_outline(cx - rx * 0.22, cy - ry * 0.34, rx * 0.42, ry * 0.30, seed + 5),
        fill=(255, 236, 180, 70),
    )
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(s * 0.03)))

    return img.resize((size, size), Image.LANCZOS)


def _draw_sauce_cup(size: int) -> Image.Image:
    """Draw a small red dipping-sauce cup on a transparent background.

    Args:
        size: Output image is size x size pixels (RGBA).

    Returns:
        RGBA ``PIL.Image.Image`` of the sauce cup.
    """
    s = size * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = s / 2
    top, bottom = s * 0.30, s * 0.82
    top_rx, bot_rx = s * 0.34, s * 0.26
    # Cup body (trapezoid) with elliptical bottom.
    draw.polygon(
        [(cx - top_rx, top + s * 0.02), (cx + top_rx, top + s * 0.02),
         (cx + bot_rx, bottom), (cx - bot_rx, bottom)],
        fill=(240, 240, 238, 255),
    )
    draw.ellipse([cx - bot_rx, bottom - s * 0.05, cx + bot_rx, bottom + s * 0.05], fill=(222, 222, 220, 255))
    # Cup rim.
    draw.ellipse([cx - top_rx, top - s * 0.06, cx + top_rx, top + s * 0.10], fill=(250, 250, 248, 255))
    # Sauce surface with a glossy dollop.
    draw.ellipse([cx - top_rx * 0.86, top - s * 0.035, cx + top_rx * 0.86, top + s * 0.085], fill=(196, 30, 24, 255))
    draw.ellipse([cx - top_rx * 0.30, top - s * 0.015, cx + top_rx * 0.05, top + s * 0.030], fill=(232, 88, 70, 200))
    return img.resize((size, size), Image.LANCZOS)


def _paper_background(width: int, height: int) -> Image.Image:
    """Create a warm kraft-paper style gradient background.

    Args:
        width: Banner width in pixels.
        height: Banner height in pixels.

    Returns:
        RGB ``PIL.Image.Image`` gradient, light center to warm edges.
    """
    img = Image.new("RGB", (width, height))
    px = img.load()
    cx, cy = width / 2, height / 2
    max_d = math.hypot(cx, cy)
    for y in range(height):
        for x in range(width):
            d = math.hypot(x - cx, y - cy) / max_d  # 0 center .. 1 corner
            r = int(252 - 26 * d)
            g = int(242 - 34 * d)
            b = int(222 - 46 * d)
            px[x, y] = (r, g, b)
    return img


def generate_all() -> None:
    """Generate every asset image and write it into ``assets/``.

    Produces:
        * ``nugget_1.png`` .. ``nugget_3.png`` — individual nuggets.
        * ``nugget_banner.png`` — landing page banner (nuggets + sauce cup).
        * ``author_placeholder.png`` — placeholder avatar for the About page.
    """
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # Individual nuggets (different seeds => different shapes).
    for i, seed in enumerate((11, 42, 77), start=1):
        _draw_nugget(560, seed).save(ASSETS_DIR / f"nugget_{i}.png")

    # Banner: scatter nuggets + a sauce cup over the paper background.
    w, h = 1500, 500
    banner = _paper_background(w // 4, h // 4).resize((w, h), Image.LANCZOS).convert("RGBA")
    layout = [  # (x, y, size, seed, rotation degrees)
        (60, 90, 330, 3, -14),
        (330, 150, 360, 8, 22),
        (620, 70, 340, 21, -6),
        (880, 160, 350, 34, 15),
        (1150, 80, 330, 55, -21),
    ]
    for x, y, size, seed, rot in layout:
        nug = _draw_nugget(size, seed).rotate(rot, expand=True, resample=Image.BICUBIC)
        banner.alpha_composite(nug, (x, y))
    banner.alpha_composite(_draw_sauce_cup(240), (1290, 250))
    banner.convert("RGB").save(ASSETS_DIR / "nugget_banner.png", quality=92)

    # Placeholder avatar (navy circle with initials) for the About page.
    s = 512 * 2
    avatar = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(avatar)
    d.ellipse([0, 0, s, s], fill=(23, 48, 84, 255))
    d.ellipse([s * 0.30, s * 0.18, s * 0.70, s * 0.58], fill=(214, 224, 238, 255))  # head
    d.ellipse([s * 0.14, s * 0.62, s * 0.86, s * 1.30], fill=(214, 224, 238, 255))  # shoulders
    avatar.resize((512, 512), Image.LANCZOS).save(ASSETS_DIR / "author_placeholder.png")


if __name__ == "__main__":
    generate_all()
    print(f"Images written to {ASSETS_DIR}")
