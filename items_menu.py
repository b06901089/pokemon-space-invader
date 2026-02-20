import pygame
from config import constant as C


def _format_item_description(item_key, item_data):
    # Create a human-friendly description from the item's effects
    effects = item_data.get('effects', {})
    parts = []
    if 'heal' in effects:
        parts.append(f"Restore {effects['heal']} HP")
    # add any other effect keys generically
    for k, v in effects.items():
        if k != 'heal':
            parts.append(f"{k}: {v}")
    if not parts:
        return "No description available."
    return "; ".join(parts)


def _format_powerup_description(idx):
    # Map powerup index to description consistent with game logic in main.py
    if idx == 1:
        return f"Increase maximum health by {C.POWERUP_RECOVER_HEALTH} when collected."
    elif idx == 2:
        return "Increase bullet fire rate / reduces cooldown."
    elif idx == 3:
        return "Upgrade ship fire mode (more bullets)."
    elif idx == 4:
        return "Spawn protective swords around the ship (currently only damage non-boss enemies)."
    else:
        return "Error: Unknown powerup."


def _load_image(path, size=None):
    try:
        surf = pygame.image.load(path).convert_alpha()
        if size is not None and size[0] > 0 and size[1] > 0:
            surf = pygame.transform.smoothscale(surf, size)
        return surf
    except Exception:
        # return a simple placeholder surface
        s = pygame.Surface((size[0] if size else 48, size[1] if size else 48), pygame.SRCALPHA)
        pygame.draw.rect(s, (180, 180, 180), s.get_rect(), border_radius=6)
        return s


def show_items_menu(screen):
    """
    Display a UI listing all items (from config/items.json) and powerups (from constants).

    Usage: call this before the main game loop. The function blocks and returns when the
    player presses SPACE, ENTER, or closes the window.
    """
    pygame.font.init()
    clock = pygame.time.Clock()
    w, h = screen.get_size()

    title_font = pygame.font.SysFont('Constantia', 36)
    header_font = pygame.font.SysFont('Constantia', 22)
    body_font = pygame.font.SysFont('Constantia', 16)

    # Prepare items list
    items = list(C.ITEM_JSON.items())  # list of (key, dict)
    powerups = list(enumerate(C.POWERUP_PATH))  # include index

    # Layout constants
    padding = 16
    thumb_size = (64, 64)
    left_col_width = w // 2 - padding * 2
    right_col_x = w // 2 + padding

    scroll_y = 0
    max_scroll = 0

    running = True
    while running:
        clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            scroll_y = min(scroll_y + 10, 0)
        elif keys[pygame.K_DOWN]:
            scroll_y = max(scroll_y - 10, -max_scroll)
        elif keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            running = False

        # Background overlay
        screen.fill((18, 18, 18))

        # # Title
        # title_surf = title_font.render('Items & Powerups', True, C.WHITE)
        # screen.blit(title_surf, (padding, padding))

        # Single-column layout: render Items first, then Powerups below
        content_x = padding
        content_y = padding + scroll_y
        full_w = w - padding * 2

        content_y += 8
        item_header = header_font.render('Items', True, C.WHITE)
        screen.blit(item_header, (content_x, content_y))
        content_y += 36

        # Items (full-width blocks stacked vertically)
        for key, data in items:
            rect = pygame.Rect(content_x, content_y, full_w, 120)
            pygame.draw.rect(screen, (28, 28, 28), rect)
            pygame.draw.rect(screen, (80, 80, 80), rect, 1)

            # image
            img_path = data.get('url', '')
            img = _load_image(img_path, thumb_size)
            img_rect = img.get_rect()
            img_rect.topleft = (content_x + 8, content_y + 8)
            screen.blit(img, img_rect)

            # name
            name_s = header_font.render(key, True, C.WHITE)
            screen.blit(name_s, (content_x + 8 + thumb_size[0] + 8, content_y + 8))

            # description
            desc = _format_item_description(key, data)
            # wrap text simple
            lines = []
            cur = ''
            text_max_w = full_w - (thumb_size[0] + 32)
            for word in desc.split(' '):
                if body_font.size((cur + ' ' + word).strip())[0] > text_max_w:
                    lines.append(cur)
                    cur = word
                else:
                    cur = (cur + ' ' + word).strip()
            if cur:
                lines.append(cur)
            for i, ln in enumerate(lines[:4]):
                txt = body_font.render(ln, True, (220, 220, 220))
                screen.blit(txt, (content_x + 8 + thumb_size[0] + 8, content_y + 36 + i * 18))

            content_y += 136

        # Small spacer and a header for powerups
        content_y += 8
        pu_header = header_font.render('Powerups', True, C.WHITE)
        screen.blit(pu_header, (content_x, content_y))
        content_y += 36

        # Powerups (stacked below items)
        for idx, pu in powerups:
            if idx == 0:
                continue
            path, size = pu
            size = size if size else (64, 64)
            rect = pygame.Rect(content_x, content_y, full_w, 96)
            pygame.draw.rect(screen, (28, 28, 28), rect)
            pygame.draw.rect(screen, (80, 80, 80), rect, 1)

            img = _load_image(path, size)
            img_rect = img.get_rect()
            img_rect.topleft = (content_x + 8, content_y + 12)
            screen.blit(img, img_rect)

            name = f"Powerup {idx}"
            name_s = header_font.render(name, True, C.WHITE)
            screen.blit(name_s, (content_x + 8 + size[0] + 8, content_y + 8))

            desc = _format_powerup_description(idx)
            # allow a bit longer description width for powerups
            desc_lines = []
            cur = ''
            text_max_w = full_w - (size[0] + 32)
            for word in desc.split(' '):
                if body_font.size((cur + ' ' + word).strip())[0] > text_max_w:
                    desc_lines.append(cur)
                    cur = word
                else:
                    cur = (cur + ' ' + word).strip()
            if cur:
                desc_lines.append(cur)
            for i, ln in enumerate(desc_lines[:3]):
                txt = body_font.render(ln, True, (220, 220, 220))
                screen.blit(txt, (content_x + 8 + size[0] + 8, content_y + 36 + i * 18))

            content_y += 104

        # compute scroll limits based on final content_y
        # Determine content start (just below the title) and footer top so we can
        # compute the visible viewport height exactly instead of using a heuristic.
        # title_h = title_surf.get_height()
        # content_start = padding + title_h + 8  # matches how content_y was initially computed
        content_start = padding + 8
        # footer_top = h - 40  # we draw the footer at y = h - 40

        total_content_height = content_y - content_start
        # visible_height = max(0, footer_top - content_start)
        visible_height = 0
        max_scroll = max(0, total_content_height - visible_height)

        # footer
        hint = body_font.render('Press SPACE/ENTER to start the game. Use UP/DOWN to scroll items.', True, (200, 200, 200))
        screen.blit(hint, (padding, h - 40))

        pygame.display.flip()

    # function returns to caller when closed


if __name__ == '__main__':
    # Quick standalone demo when run directly
    pygame.init()
    screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    show_items_menu(screen)
    pygame.quit()
