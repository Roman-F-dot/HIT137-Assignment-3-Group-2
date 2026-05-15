class GameManager:
    def __init__(self, total_targets=5):
        self.mistakes = 0
        self.found = 0
        self.max_mistakes = 3
        self.total_targets = total_targets
        self.game_over = False
        self.game_won = False
        self.found_indices = []

    def check_click(self, x, y, target_coordinates):
        if self.game_over or self.game_won:
            return {"status": "inactive"}

        # Iterate through the 5 target boxes
        for i in range(len(target_coordinates)):
            tx = target_coordinates[i][0]
            ty = target_coordinates[i][1]
            tw = target_coordinates[i][2]
            th = target_coordinates[i][3]
            
            if tx <= x <= (tx + tw) and ty <= y <= (ty + th):
                # We clicked a box
                if i not in self.found_indices:
                    self.found += 1
                    self.found_indices.append(i)
                    
                    if self.found == self.total_targets:
                        self.game_won = True
                        
                    return {"status": "hit", "found": self.found, "index": i, "game_won": self.game_won}
                else:
                    return {"status": "already_found"}

        # If the loop finishes and didn't return, it means we clicked empty space
        self.mistakes += 1
        if self.mistakes >= self.max_mistakes:
            self.game_over = True
            
        return {"status": "miss", "mistakes": self.mistakes, "game_over": self.game_over}

    def reset_game(self):
        self.mistakes = 0
        self.found = 0
        self.game_over = False
        self.game_won = False
        self.found_indices = []