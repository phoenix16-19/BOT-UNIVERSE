import pygame
import math
import random
from collections import deque

# ---------------- Palette / Helpers ----------------

def lerp(a, b, t): return a + (b - a) * t

def make_vertical_gradient(w, h, top_rgb, bottom_rgb):
    surf = pygame.Surface((w, h))
    r1, g1, b1 = top_rgb; r2, g2, b2 = bottom_rgb
    for y in range(h):
        t = y / (h - 1)
        r = int(lerp(r1, r2, t)); g = int(lerp(g1, g2, t)); b = int(lerp(b1, b2, t))
        pygame.draw.line(surf, (r, g, b), (0, y), (w, y))
    return surf

# Van Gogh inspired palettes
SKY_TOP = (10, 12, 35)
SKY_BOTTOM = (18, 24, 70)
STAR_COLOR = (250, 235, 180)
ACCENT_BLUES = [(80,160,220), (90,190,255), (70,130,200)]
WARM_YELLOWS = [(255,210,70), (255,190,50), (255,170,40)]

# ---------------- Glow Cache ----------------

class GlowCache:
    def __init__(self):
        self.cache = {}  # key: (color_rgb, size) -> surface

    def get(self, base_color, size):
        key = (base_color, size)
        if key in self.cache:
            return self.cache[key]
        surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        cx = cy = size
        r, g, b = base_color
        for rad in range(size, 0, -1):
            t = rad / size
            alpha = int(120 * (t ** 2))
            pygame.draw.circle(surf, (r, g, b, alpha), (cx, cy), rad)
        self.cache[key] = surf
        return surf

# ---------------- Flow Field (Painterly strokes) ----------------

class FlowField:
    def __init__(self, w, h, cell=50):
        self.w, self.h, self.cell = w, h, cell
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self.vectors = self._generate_vectors()
        self.strokes = []
        self.fade_rect = pygame.Surface((w, h), pygame.SRCALPHA)
        self.fade_rect.fill((0,0,0,4))  # low alpha for gradual fade

    def _generate_vectors(self):
        vectors = []
        golden_angle = math.radians(137.5)
        idx = 0
        for y in range(0, self.h, self.cell):
            row = []
            for x in range(0, self.w, self.cell):
                # swirl orientation with slight deterministic angle
                ang = (idx * golden_angle) % (math.tau)
                ang += random.uniform(-0.6, 0.6)
                row.append((math.cos(ang), math.sin(ang)))
                idx += 1
            vectors.append(row)
        return vectors

    def spawn_stroke(self):
        x = random.randrange(0, self.w)
        y = random.randrange(0, self.h)
        life = random.randint(12, 28)
        color = random.choice(ACCENT_BLUES + [(40,60,120)])
        self.strokes.append({
            "x": x, "y": y,
            "vx": 0, "vy": 0,
            "life": life,
            "max_life": life,
            "color": color
        })

    def update(self):
        # gentle fade (simulate drying paint)
        self.surface.blit(self.fade_rect, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        # spawn probability
        if random.random() < 0.5:
            self.spawn_stroke()

        # iterate strokes
        alive = []
        for s in self.strokes:
            gx = int(s["x"] // self.cell)
            gy = int(s["y"] // self.cell)
            if 0 <= gy < len(self.vectors) and 0 <= gx < len(self.vectors[0]):
                vx, vy = self.vectors[gy][gx]
                # slight curl noise jitter
                vx += random.uniform(-0.2, 0.2)
                vy += random.uniform(-0.2, 0.2)
                speed = 2.2
                s["x"] += vx * speed
                s["y"] += vy * speed
                s["life"] -= 1
                # opacity falls with life
                alpha = int(70 * (s["life"] / s["max_life"]))
                if alpha > 0:
                    pygame.draw.circle(
                        self.surface,
                        (*s["color"], alpha),
                        (int(s["x"]), int(s["y"])),
                        3
                    )
            if s["life"] > 0:
                alive.append(s)
        self.strokes = alive

    def draw(self, target):
        target.blit(self.surface, (0, 0))


# ---------------- Spiral Star Field ----------------

class SpiralStars:
    def __init__(self, w, h, count=90):
        self.w, self.h = w, h
        self.cx = w // 2
        self.cy = h // 2
        self.stars = self._make(count)
        self.base_color = STAR_COLOR

    def _make(self, count):
        pts = []
        golden_angle = math.radians(137.5)
        for i in range(count):
            radius = (i + 1) * 6.0
            angle = i * golden_angle
            jitter_r = random.uniform(-1.6, 1.6)
            jitter_a = random.uniform(-0.25, 0.25)
            pts.append({
                "radius": radius + jitter_r,
                "angle": angle + jitter_a,
                "tw_phase": random.random() * math.tau
            })
        return pts

    def draw(self, surface, t):
        # subtle global rotation
        rot = t * 0.15
        for s in self.stars:
            ang = s["angle"] + rot
            r = s["radius"]
            x = int(self.cx + math.cos(ang) * r)
            y = int(self.cy + math.sin(ang) * r)

            tw = (math.sin(t * 2.4 + s["tw_phase"]) + 1) * 0.5
            size = 1 + int(tw * 2)
            col = self.base_color
            pygame.draw.circle(surface, col, (x, y), size)

# ---------------- Universe ----------------

class Universe:
    def __init__(self, width=1000, height=700):
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bot Universe")
        self.clock = pygame.time.Clock()
        self.bots = []

        # Layers
        self.bg_surface = make_vertical_gradient(width, height, SKY_TOP, SKY_BOTTOM)
        self.flow = FlowField(width, height, cell=55)
        self.stars = SpiralStars(width, height)

        self.glow_cache = GlowCache()

        # Optional global mood (later compute from bots)
        self.global_mood = 0.5

    def add_bot(self, bot):
        self.bots.append(bot)

    # ---- Visual Helpers ----

    def draw_bot(self, bot):
        """Wrap existing bot.draw with aura + fallback if bot.draw missing."""
        # For mood color pick something dynamic (placeholder)
        base_col = random.choice(WARM_YELLOWS) if hasattr(bot, "mood") and bot.mood > 0.6 else random.choice(ACCENT_BLUES)
        radius = 18
        glow = self.glow_cache.get(base_col, radius * 2)
        # Random position fallback if bot has no x,y
        x = getattr(bot, "x", random.randint(50, self.width - 50))
        y = getattr(bot, "y", random.randint(50, self.height - 50))

        # Draw glow
        self.screen.blit(glow, (x - glow.get_width() // 2, y - glow.get_height() // 2), special_flags=pygame.BLEND_ADD)
        # Core
        pygame.draw.circle(self.screen, base_col, (x, y), radius)

        # Call bot's own draw (if exists)
        if hasattr(bot, "draw"):
            try:
                bot.draw(self.screen)
            except Exception:
                pass

    # ---- Main Tick ----

    def tick(self):
        t = pygame.time.get_ticks() / 1000.0

        # Background base
        self.screen.blit(self.bg_surface, (0, 0))

        # Flow strokes update/draw
        self.flow.update()
        self.flow.draw(self.screen)

        # Spiral stars
        self.stars.draw(self.screen, t)

        # Bots logic + visuals
        for bot in self.bots:
            if hasattr(bot, "act"):
                try:
                    bot.act(self)
                except Exception:
                    pass
            self.draw_bot(bot)

        # (Optional) global mood tint overlay (later)
        # tint = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # mood_t = self.global_mood
        # tint.fill((30, 50, int(120 * mood_t), int(40 * mood_t)))
        # self.screen.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

        pygame.display.flip()
        self.clock.tick(60)