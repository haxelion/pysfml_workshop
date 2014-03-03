import sfml

window = sfml.RenderWindow(sfml.VideoMode(1366, 768), 'Rainbow Fire', sfml.window.Style.FULLSCREEN)
rainbow_dash_tx = sfml.Texture.from_file('rainbow_dash.png')
player = sfml.Sprite(rainbow_dash_tx)
player.position = (50, 300)
player.ratio = (0.5, 0.5)
speed = 10

while window.is_open:
    for event in window.events:
        if type(event) is sfml.CloseEvent:
            window.close()
        if type(event) is sfml.KeyEvent and event.pressed and event.code is sfml.Keyboard.ESCAPE:
            window.close()
    if sfml.Keyboard.is_key_pressed(sfml.Keyboard.UP):
        player.move((0, -speed))
    if sfml.Keyboard.is_key_pressed(sfml.Keyboard.DOWN):
        player.move((0, speed))
    if sfml.Keyboard.is_key_pressed(sfml.Keyboard.LEFT):
        player.move((-speed, 0))
    if sfml.Keyboard.is_key_pressed(sfml.Keyboard.RIGHT):
        player.move((speed, 0))
    window.clear(sfml.Color(0,128,255))
    window.draw(player)   
    window.display()
    sfml.system.sleep(sfml.milliseconds(20))
