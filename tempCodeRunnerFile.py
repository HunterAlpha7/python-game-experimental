def main_menu():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Draw the menu background
        screen.blit(MENU_BACKGROUND, (0, 0))  # Position the background at (0, 0)

        # Render menu text
        title_text = font.render("The Logical Labyrinth", True, (255, 255, 255))
        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        exit_text = font.render("Press ESC to Exit", True, (255, 255, 255))
        credits_text = font.render("Press C for Credits", True, (255, 255, 255))

        # Display the title and buttons
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(credits_text, (SCREEN_WIDTH // 2 - credits_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT * 3 // 4))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False  # Start the game when SPACE is pressed
                elif event.key == pygame.K_c:
                    credits_screen()  # Show credits screen when C is pressed
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
