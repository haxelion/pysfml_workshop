import sfml
import random
import time

# Initialize the window 
window = sfml.RenderWindow(sfml.VideoMode.get_desktop_mode(), 'Rainbow Fire', sfml.window.Style.FULLSCREEN)
visible_area = sfml.Rectangle(sfml.Vector2(0, 0), window.size)

# Seed random
random.seed(time.time())

# Load textures
rainbow_dash_tx = sfml.Texture.from_file('rainbow_dash.png')
evil_pony_tx = sfml.Texture.from_file('evil_pony.png')
blast_tx = sfml.Texture.from_file('blast.png')
bullet_tx = sfml.Texture.from_file('bullet.png')

# Load sounds
blast_sound = sfml.Sound(sfml.SoundBuffer.from_file('blast.wav'))
shot_sound = sfml.Sound(sfml.SoundBuffer.from_file('shot.wav'))

# Load font
bangers_ft = sfml.Font.from_file('Bangers.ttf')

# Score 
score = 0
score_text = sfml.Text('Score: ' + str(score), bangers_ft)
score_text.position = (window.size.x-score_text.global_bounds.width-20, 10)

# Player
player = sfml.Sprite(rainbow_dash_tx)
player.position = (50, window.size.y/2)
player.ratio = (0.5, 0.5)
player_speed = 10

# Enemies
enemies = []
enemy_speed = (-5, 0)
spawn_clock = sfml.Clock()
spawn_time = 1000

# Blasts
blasts = []
blast_speed = (15, 0)
fire_clock = sfml.Clock()
fire_cooldown = 500

# Bullets
bullets = []
bullet_speed = (-10, 0)
bullet_clock = sfml.Clock()
bullet_interval = random.randint(500, 1000)

while window.is_open:

    # Handle window events
    for event in window.events:
        if type(event) is sfml.CloseEvent:
            window.close()
        if type(event) is sfml.KeyEvent and event.pressed and event.code is sfml.Keyboard.ESCAPE:
            window.close()

    # Handle player input
    if sfml.Keyboard.is_key_pressed(sfml.Keyboard.UP):
        player.move((0, -player_speed))
    if sfml.Keyboard.is_key_pressed(sfml.Keyboard.DOWN):
        player.move((0, player_speed))
    if sfml.Keyboard.is_key_pressed(sfml.Keyboard.LEFT):
        player.move((-player_speed, 0))
    if sfml.Keyboard.is_key_pressed(sfml.Keyboard.RIGHT):
        player.move((player_speed, 0))
    # Fire!
    if sfml.Keyboard.is_key_pressed(sfml.Keyboard.SPACE) and fire_clock.elapsed_time.milliseconds > fire_cooldown:
        blast = sfml.Sprite(blast_tx)
        blast.ratio = (0.25, 0.25)
        blast.position = player.position
        blast.move((40, 20))
        blasts.append(blast)
        blast_sound.play()
        fire_clock.restart()

    # Enemy fire
    if len(enemies) > 0 and bullet_clock.elapsed_time.milliseconds > bullet_interval:
        bullet = sfml.Sprite(bullet_tx)
        bullet.ratio = (0.25, 0.25)
        i = random.randint(0, len(enemies)-1)
        bullet.position = enemies[i].position
        bullet.move((-20, 20))
        bullets.append(bullet)
        bullet_interval = random.randint(500, 1000)
        shot_sound.play()
        bullet_clock.restart()

    # Update blasts
    for blast in blasts:
        blast.move(blast_speed)
        if not visible_area.intersects(blast.global_bounds):
            blasts.remove(blast)

    # Update bullets:
    for bullet in bullets:
        bullet.move(bullet_speed)
        if not visible_area.intersects(bullet.global_bounds):
            bullets.remove(bullet)

    # Spawn enemy
    if spawn_clock.elapsed_time.milliseconds > spawn_time:
        enemy = sfml.Sprite(evil_pony_tx)
        enemy.ratio = (0.25,0.25)
        enemy.position = (window.size.x-50, random.randint(0,window.size.y-100))
        enemies.append(enemy)
        spawn_clock.restart()

    # Update enemies
    for enemy in enemies:
        enemy.move(enemy_speed)
        if not visible_area.intersects(enemy.global_bounds):
            enemies.remove(enemy)
        for blast in blasts:
            if blast.global_bounds.intersects(enemy.global_bounds):
                enemies.remove(enemy)
                blasts.remove(blast)
                score += 10
                score_text = sfml.Text('Score: ' + str(score), bangers_ft)
                score_text.position = (window.size.x-score_text.global_bounds.width-20, 10)

    # Draw
    window.clear(sfml.Color(0,128,255))
    for blast in blasts:
        window.draw(blast)
    for enemy in enemies:
        window.draw(enemy)
    for bullet in bullets:
        window.draw(bullet)
    window.draw(player)   
    window.draw(score_text)
    window.display()
    sfml.system.sleep(sfml.milliseconds(20))
