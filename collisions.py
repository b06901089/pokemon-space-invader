import pygame
from objects import Explosion

def resolve_all(sprite_groups, sound_manager):
    result = {
        "killed_aliens": 0,
        "hong_bao_collected": 0,
        "applied_powerups": [],  # (ship, powerup)
    }

    # bullet vs aliens
    collisions = pygame.sprite.groupcollide(sprite_groups['bullet'], sprite_groups['alien'], True, True)
    for _, aliens in collisions.items():
        for a in aliens:
            result["killed_aliens"] += 1
            sound_manager.play("explosion")
            sprite_groups['explosion'].add(Explosion(a.rect.centerx, a.rect.centery, 2))

    # bullet vs alien bullets
    collisions = pygame.sprite.groupcollide(sprite_groups['bullet'], sprite_groups['alien_bullet'], True, True)
    for bullet, _ in collisions.items():
        sound_manager.play("explosion")
        sprite_groups['explosion'].add(Explosion(bullet.rect.centerx, bullet.rect.centery, 1))

    # bullet vs unbreakable bullets (bullets destroy player bullets)
    collisions = pygame.sprite.groupcollide(sprite_groups['bullet'], sprite_groups['unbreakable_bullet'], True, False)
    for bullet, _ in collisions.items():
        sound_manager.play("explosion")
        sprite_groups['explosion'].add(Explosion(bullet.rect.centerx, bullet.rect.centery, 1))

    # bullet vs boss
    collisions = pygame.sprite.groupcollide(sprite_groups['bullet'], sprite_groups['boss'], True, False)
    for bullet, bosses in collisions.items():
        for b in bosses:
            b.health_remaining -= 1
            sound_manager.play("explosion")
            sprite_groups['explosion'].add(Explosion(bullet.rect.centerx, bullet.rect.centery, 1))
            if b.health_remaining <= 0:
                sound_manager.play("explosion")
                sprite_groups['explosion'].add(Explosion(bullet.rect.centerx, bullet.rect.centery, 3))
                b.kill()

    # alien bullets vs spaceship
    collisions = pygame.sprite.groupcollide(sprite_groups['alien_bullet'], sprite_groups['spaceship'], True, False, pygame.sprite.collide_mask)
    for ab, ships in collisions.items():
        for s in ships:
            sound_manager.play("explosion2")
            s.health_remaining -= 1
            sprite_groups['explosion'].add(Explosion(ab.rect.centerx, ab.rect.centery, 1))

    # unbreakable bullets vs spaceship
    collisions = pygame.sprite.groupcollide(sprite_groups['unbreakable_bullet'], sprite_groups['spaceship'], True, False, pygame.sprite.collide_mask)
    for ab, ships in collisions.items():
        for s in ships:
            sound_manager.play("explosion2")
            s.health_remaining -= 1
            sprite_groups['explosion'].add(Explosion(ab.rect.centerx, ab.rect.centery, 1))

    # alien vs spaceship
    collisions = pygame.sprite.groupcollide(sprite_groups['alien'], sprite_groups['spaceship'], True, False, pygame.sprite.collide_mask)
    for alien, ships in collisions.items():
        result["killed_aliens"] += 1
        for s in ships:
            sound_manager.play("explosion2")
            s.health_remaining -= 1
            sprite_groups['explosion'].add(Explosion(alien.rect.centerx, alien.rect.centery, 2))

    # spaceship vs powerups
    collisions = pygame.sprite.groupcollide(sprite_groups['spaceship'], sprite_groups['powerup'], False, True, pygame.sprite.collide_mask)
    for ship, powerups in collisions.items():
        for pu in powerups:
            pu_type = getattr(pu, 'pu_type', None)
            result["applied_powerups"].append((ship, pu_type))

    # spaceship vs hong_bao
    collisions = pygame.sprite.groupcollide(sprite_groups['spaceship'], sprite_groups['hong_bao'], False, True, pygame.sprite.collide_mask)
    collected = 0
    for ship, hbs in collisions.items():
        for _ in hbs:
            collected += 1
            # ship.health_remaining = min(ship.health_start, ship.health_remaining + 1)
    result["hong_bao_collected"] = collected

    # alien vs sword
    collisions = pygame.sprite.groupcollide(sprite_groups['alien'], sprite_groups['sword'], True, False)
    for a, _ in collisions.items():
        result["killed_aliens"] += 1
        sound_manager.play("explosion")
        sprite_groups['explosion'].add(Explosion(a.rect.centerx, a.rect.centery, 2))

    # alien_bullet vs sword
    collisions = pygame.sprite.groupcollide(sprite_groups['alien_bullet'], sprite_groups['sword'], True, False)
    for a, _ in collisions.items():
        sound_manager.play("explosion")
        sprite_groups['explosion'].add(Explosion(a.rect.centerx, a.rect.centery, 1))

    # spaceship vs animation
    collisions = pygame.sprite.groupcollide(sprite_groups['spaceship'], sprite_groups['animation'], False, True, pygame.sprite.collide_mask)
    for s, anis in collisions.items():
        for ani in anis:
            sound_manager.play("explosion2")
            s.health_remaining -= ani.power
            sprite_groups['explosion'].add(Explosion(ani.rect.centerx, ani.rect.centery, 1))

    return result
