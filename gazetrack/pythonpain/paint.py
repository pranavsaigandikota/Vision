import pygame
import speech_recognition as sr
import threading

pygame.init()
fps = 60
timer = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
active_size = 5  
active_color = 'white'
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Vision')
painting = []
recognizer = sr.Recognizer()
is_listening = False  # Track if speech recognition is active

def draw_menu():
    pygame.draw.rect(screen, 'gray', [0, 0, WIDTH, 70])
    pygame.draw.line(screen, 'black', (0, 70), (WIDTH, 70), 3)

    xl_brush = pygame.draw.rect(screen, 'black', [10, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (35, 35), 20)
    l_brush = pygame.draw.rect(screen, 'black', [70, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (95, 35), 15)
    m_brush = pygame.draw.rect(screen, 'black', [130, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (155, 35), 10)
    s_brush = pygame.draw.rect(screen, 'black', [190, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (215, 35), 5)

    brush_list = [xl_brush, l_brush, m_brush, s_brush]

    blue = pygame.draw.rect(screen, (0, 0, 255), [WIDTH - 35, 10, 25, 25])    
    red = pygame.draw.rect(screen, (255, 0, 0), [WIDTH - 35, 35, 25, 25])   
    green = pygame.draw.rect(screen, (0, 255, 0), [WIDTH - 60, 10, 25, 25])  
    yellow = pygame.draw.rect(screen, (255, 255, 0), [WIDTH - 60, 35, 25, 25])  
    teal = pygame.draw.rect(screen, (0, 255, 255), [WIDTH - 85, 10, 25, 25]) 
    purple = pygame.draw.rect(screen, (255, 0, 255), [WIDTH - 85, 35, 25, 25])
    white = pygame.draw.rect(screen, (255, 255, 255), [WIDTH - 110, 10, 25, 25]) 
    black = pygame.draw.rect(screen, (0, 0, 0), [WIDTH - 110, 35, 25, 25])   

    color_rect = [blue, red, green, yellow, teal, purple, white, black]
    rgb_list = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0),
                (0, 255, 255), (255, 0, 255), (255, 255, 255), (0, 0, 0)]
    
    return brush_list, color_rect, rgb_list

def draw_painting(paints):
    for paint in paints:
        pygame.draw.circle(screen, paint[0], paint[1], paint[2])

def listen_for_command():
    global active_color, active_size, is_listening

    if not is_listening:
        is_listening = True

        try:
            # Start the listening process and print feedback
            print("Listening for color and size commands...")

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                print("Adjusted for ambient noise, starting to listen...")
                audio = recognizer.listen(source)
                print("Captured audio, processing...")

            # Recognize speech and convert to text
            mytext = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {mytext}")

            # Process the recognized text
            colors = {"red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0), 
                      "yellow": (255, 255, 0), "purple": (255, 0, 255), "white": (255, 255, 255), 
                      "black": (0, 0, 0), "teal": (0, 255, 255)}
            if mytext in colors:
                active_color = colors[mytext]
                print(f"Color changed to: {mytext}")

            if "small" in mytext:
                active_size = 10
                print("Brush size set to small")
            elif "medium" in mytext:
                active_size = 15
                print("Brush size set to medium")
            elif "large" in mytext:
                active_size = 25
                print("Brush size set to large")
            elif "extra large" in mytext:
                active_size = 50
                print("Brush size set to extra large")

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        
        is_listening = False

run = True
while run:
    timer.tick(fps)
    screen.fill('white')
    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]

    if left_click and mouse[1] > 70:
        painting.append((active_color, mouse, active_size))

    draw_painting(painting)

    if mouse[1] > 70:
        pygame.draw.circle(screen, active_color, mouse, active_size)

    brushes, colors, rgbs = draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Trigger voice command for color and brush size
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Press 'C' to change color via speech
                threading.Thread(target=listen_for_command).start()
            elif event.key == pygame.K_b:  # Press 'B' to change brush size via speech
                threading.Thread(target=listen_for_command).start()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(brushes)):
                if brushes[i].collidepoint(event.pos):
                    active_size = 20 - (i * 5)
            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    active_color = rgbs[i]  

    pygame.display.flip()

pygame.quit()