import pygame
from objects import Explosion

def resolve_all(sprite_groups, sound_manager, current_frame=0):
    result = {
        "killed_aliens": 0,
        "killed_bosses": 0,
        "hong_bao_collected": 0,
        "applied_powerups": [],  # (ship, powerup)
    }

    # my attack vs enemy attack
    collisions = pygame.sprite.groupcollide(sprite_groups['my_ani'], sprite_groups['animation'], False, False)
    for my_ani, en_anis in collisions.items():
        for en_ani in en_anis:
            if my_ani.power > en_ani.power:
                sound_manager.play('explosion')
                sprite_groups['explosion'].add(Explosion(en_ani.rect.centerx, en_ani.rect.centery, 1))
                en_ani.kill()
            elif my_ani.power < en_ani.power:
                sound_manager.play('explosion')
                sprite_groups['explosion'].add(Explosion(my_ani.rect.centerx, my_ani.rect.centery, 1))
                my_ani.kill()
            else:
                sound_manager.play('explosion')
                sprite_groups['explosion'].add(Explosion(en_ani.rect.centerx, en_ani.rect.centery, 1))
                en_ani.kill()
                my_ani.kill()

    # my attack vs alien
    collisions = pygame.sprite.groupcollide(sprite_groups['my_ani'], sprite_groups['alien'], True, False)
    for ani, aliens in collisions.items():
        for a in aliens:
            a.health_remaining -= ani.power
            sound_manager.play('explosion')
            if a.health_remaining <= 0:
                sprite_groups['explosion'].add(Explosion(a.rect.centerx, a.rect.centery, 2))
                a.kill()
                result['killed_aliens'] += 1
            else:
                sprite_groups['explosion'].add(Explosion(ani.rect.centerx, ani.rect.centery, 1))

    # my attack vs boss
    collisions = pygame.sprite.groupcollide(sprite_groups['my_ani'], sprite_groups['boss'], True, False)
    for ani, bosses in collisions.items():
        for b in bosses:
            b.health_remaining -= ani.power
            sound_manager.play('explosion')
            if b.health_remaining <= 0:
                sprite_groups['explosion'].add(Explosion(b.rect.centerx, b.rect.centery, 3))
                b.kill()
                result['killed_bosses'] += 1
            else:
                sprite_groups['explosion'].add(Explosion(ani.rect.centerx, ani.rect.centery, 1))

    # mypoke vs alien
    collisions = pygame.sprite.groupcollide(sprite_groups['mypoke'], sprite_groups['alien'], False, True, pygame.sprite.collide_mask)
    for s, aliens in collisions.items():
        for a in aliens:
            s.health_remaining -= 1
            sprite_groups['explosion'].add(Explosion(a.rect.centerx, a.rect.centery, 2))
            sound_manager.play("explosion2")
            result["killed_aliens"] += 1

    # mypoke vs enemy attack
    collisions = pygame.sprite.groupcollide(sprite_groups['mypoke'], sprite_groups['animation'], False, True, pygame.sprite.collide_mask)
    for s, anis in collisions.items():
        for ani in anis:
            s.health_remaining -= ani.power
            sprite_groups['explosion'].add(Explosion(ani.rect.centerx, ani.rect.centery, 1))
            sound_manager.play("explosion2")

    # mypoke vs powerups
    collisions = pygame.sprite.groupcollide(sprite_groups['mypoke'], sprite_groups['powerup'], False, True, pygame.sprite.collide_mask)
    for s, powerups in collisions.items():
        for pu in powerups:
            pu_type = getattr(pu, 'pu_type', None)
            result["applied_powerups"].append((s, pu_type))

    # mypoke vs hong_bao
    collisions = pygame.sprite.groupcollide(sprite_groups['mypoke'], sprite_groups['hong_bao'], False, True, pygame.sprite.collide_mask)
    for s, hbs in collisions.items():
        for _ in hbs:
            result["hong_bao_collected"] += 1

    # sword vs alien
    collisions = pygame.sprite.groupcollide(sprite_groups['sword'], sprite_groups['alien'], False, False)
    for sword, aliens in collisions.items():
        for a in aliens:
            if sword.can_damage(a, current_frame):
                a.health_remaining -= sword.power
                sound_manager.play("explosion")
                if a.health_remaining <= 0:
                    sprite_groups['explosion'].add(Explosion(a.rect.centerx, a.rect.centery, 2))
                    a.kill()
                    result["killed_aliens"] += 1
                else:
                    sprite_groups['explosion'].add(Explosion(sword.rect.centerx, sword.rect.centery, 1))

    # sword vs boss
    collisions = pygame.sprite.groupcollide(sprite_groups['sword'], sprite_groups['boss'], False, False)
    for sword, bosses in collisions.items():
        for b in bosses:
            if sword.can_damage(b, current_frame):
                b.health_remaining -= sword.power
                sound_manager.play("explosion")
                if b.health_remaining <= 0:
                    sprite_groups['explosion'].add(Explosion(b.rect.centerx, b.rect.centery, 3))
                    b.kill()
                    result["killed_bosses"] += 1
                else:
                    sprite_groups['explosion'].add(Explosion(sword.rect.centerx, sword.rect.centery, 1))

    # sword vs enemy attack
    collisions = pygame.sprite.groupcollide(sprite_groups['sword'], sprite_groups['animation'], False, False)
    for sword, anis in collisions.items():
        for ani in anis:
            if sword.can_damage(ani, current_frame) and sword.power >= ani.power:
                sound_manager.play("explosion")
                sprite_groups['explosion'].add(Explosion(ani.rect.centerx, ani.rect.centery, 1))
                ani.kill()

    return result
