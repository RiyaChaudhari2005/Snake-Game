import turtle
import random

STEP = 20
score = 0
highest_score = 0
delay_ms = 100
bodies = []

s1 = turtle.Screen()
s1.title("Snake Game")
s1.bgcolor("light green")
s1.setup(width=600, height=600)
s1.tracer(0)

h1 = turtle.Turtle()
h1.shape("circle")
h1.color("black")
h1.penup()
h1.goto(0, 0)
h1.direction = "stop"

f1 = turtle.Turtle()
f1.shape("square")
f1.color("red")
f1.penup()

sb = turtle.Turtle()
sb.hideturtle()
sb.penup()
sb.goto(-260, 260)

def update_score():
    sb.clear()
    sb.write(f"Score:{score} | Highest Score:{highest_score}",
             font=("Arial", 11, "bold"))

def place_food():
    occupied = {(round(h1.xcor()), round(h1.ycor()))}
    occupied.update((round(b.ycor()))
                    for b in bodies)
    cells = [(x, y) for x in range(-280, 281, STEP)
                    for y in range(-280, 241, STEP)
                    if (x, y) not in occupied]
    if cells:
        f1.goto(random.choice(cells))

def change(direction):
    opposite = {"up": "down", "down": "up",
                "left": "right", "right": "left"}
    if h1.direction != opposite[direction]:
        h1.direction = direction

def reset_game():
    global score, delay_ms
    h1.goto(0, 0)
    h1.direction = "stop"
    for body in bodies:
        body.hideturtle()
    bodies.clear()
    score = 0
    delay_ms = 100
    update_score()
    place_food()

def tick():
    global score, highest_score, delay_ms
    # Save previous head/body positions.
    old_positions = [h1.position()] + [b.position() for b in bodies]
    if h1.direction == "up":
        h1.sety(h1.ycor() + STEP)
    elif h1.direction == "down":
        h1.sety(h1.ycor() - STEP)
    elif h1.direction == "left":
        h1.setx(h1.xcor() - STEP)
    elif h1.direction == "right":
        h1.setx(h1.xcor() + STEP)

    # Border se nikalne par opposite side par aana.
    if h1.xcor() > 280: h1.setx(-280)
    if h1.xcor() < -280: h1.setx(280)
    if h1.ycor() > 280: h1.sety(-280)
    if h1.ycor() < -280: h1.sety(280)

    for body, old_pos in zip(bodies, old_positions):
        body.goto(old_pos)

    if h1.distance(f1) < STEP:
        body = turtle.Turtle()
        body.shape("square")
        body.color("blue")
        body.penup()
        body.goto(old_positions[-1])
        bodies.append(body)
        score += 100
        highest_score = max(highest_score, score)
        delay_ms = max(45, delay_ms - 1)
        update_score()
        place_food()

    if any(h1.distance(b) < 10 for b in bodies):
        reset_game()

    s1.update()
    s1.ontimer(tick, delay_ms)

s1.listen()
s1.onkey(lambda: change("up"), "Up")
s1.onkey(lambda: change("down"), "Down")
s1.onkey(lambda: change("left"), "Left")
s1.onkey(lambda: change("right"), "Right")
s1.onkey(lambda: setattr(h1, "direction", "stop"), "space")
update_score()
place_food()
tick()
s1.mainloop()
