class ConsoleVersion:
    POSITION_MAP = {
        (0, 0): "oben links",
        (0, 1): "oben mitte",
        (0, 2): "oben rechts",
        (1, 0): "mitte links",
        (1, 1): "mitte mitte",
        (1, 2): "mitte rechts",
        (2, 0): "unten links",
        (2, 1): "unten mitte",
        (2, 2): "unten rechts",
    }

    def __init__(self):
        self.big_board = [[self._create_small_board() for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.next_big_field = None

    def _create_small_board(self):
        return [[str(i * 3 + j + 1) for j in range(3)] for i in range(3)]

    def print_board(self):
        for big_row in range(3):
            for small_row in range(3):
                line = [" | ".join(self.big_board[big_row][big_col][small_row] if isinstance(self.big_board[big_row][big_col], list) else [self.big_board[big_row][big_col][0][0]] * 3) for big_col in range(3)]
                print("    ".join(line))
            if big_row < 2:
                print("-" * 40)

    def check_winner(self, board):
        for row in range(3):
            if board[row][0] in ["X", "O"] and board[row][0] == board[row][1] == board[row][2]:
                return board[row][0]
        for col in range(3):
            if board[0][col] in ["X", "O"] and board[0][col] == board[1][col] == board[2][col]:
                return board[0][col]
        if board[0][0] in ["X", "O"] and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] in ["X", "O"] and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        return None

    def play_turn(self, big_row, big_col, small_index):
        small_row, small_col = divmod(small_index - 1, 3)

        if not isinstance(self.big_board[big_row][big_col], list):
            print(f"Das große Feld ({self.POSITION_MAP[(big_row, big_col)]}) ist bereits entschieden. Du kannst frei wählen.")
            self.next_big_field = None
            return False

        if self.next_big_field and (big_row, big_col) != self.next_big_field:
            print(f"Du musst im großen Feld {self.POSITION_MAP[self.next_big_field]} spielen!")
            return False

        if self.big_board[big_row][big_col][small_row][small_col] in ["X", "O"]:
            print("Ungültiger Zug: Feld ist bereits belegt! Wähle ein anderes Feld im großen Spielfeld oder passe die Eingabe an.")
            return False

        self.big_board[big_row][big_col][small_row][small_col] = self.current_player

        winner = self.check_winner(self.big_board[big_row][big_col])
        if winner:
            print(f"Spieler {winner} hat das kleine Feld ({self.POSITION_MAP[(big_row, big_col)]}) gewonnen!")
            self.big_board[big_row][big_col] = [[winner] * 3] * 3

        big_board_state = [
            [self.big_board[row][col][0][0] if isinstance(self.big_board[row][col], list) else self.big_board[row][col][0][0] for col in range(3)]
            for row in range(3)
        ]

        if self.check_winner(big_board_state):
            print(f"Spieler {self.current_player} gewinnt das Spiel!")
            return True

        if isinstance(self.big_board[small_row][small_col], list) and any(cell not in ["X", "O"] for row in self.big_board[small_row][small_col] for cell in row):
            self.next_big_field = (small_row, small_col)
        else:
            print(f"Das große Feld ({self.POSITION_MAP[(small_row, small_col)]}) ist voll oder bereits entschieden. Du kannst frei wählen.")
            self.next_big_field = None

        self.current_player = "O" if self.current_player == "X" else "X"
        return False

    def start_game(self):
        print("Super Tic Tac Toe!")
        print("-" * 17 + " RH  " + "-"*17)
        while True:
            self.print_board()
            print(f"Spieler {self.current_player} ist am Zug.")

            try:
                if self.next_big_field:
                    big_row, big_col = self.next_big_field
                    if not isinstance(self.big_board[big_row][big_col], list):
                        print(f"Das erzwungene große Feld ({self.POSITION_MAP[(big_row, big_col)]}) ist bereits entschieden. Du kannst frei wählen.")
                        self.next_big_field = None
                    else:
                        print(f"Erzwungenes großes Feld: {self.POSITION_MAP[(big_row, big_col)]}")

                if not self.next_big_field:
                    position = input("Großes Feld (oben, mitte, unten + links, mitte, rechts): ").lower().split()
                    if len(position) != 2:
                        print("Ungültige Eingabe. Beispiel: 'oben links'")
                        continue

                    big_row = ["oben", "mitte", "unten"].index(position[0])
                    big_col = ["links", "mitte", "rechts"].index(position[1])

                small_index = int(input("Kleines Feld (Nummer 1-9): "))
                if not (1 <= small_index <= 9):
                    print("Ungültige Eingabe: Nummer muss zwischen 1 und 9 liegen!")
                    continue

                if self.play_turn(big_row, big_col, small_index):
                    break
            except ValueError:
                print("Ungültige Eingabe: Bitte geben Sie korrekte Werte ein.")
            except IndexError:
                print("Ungültige Eingabe: Feld außerhalb des gültigen Bereichs.")

def main():
    game = ConsoleVersion()
    game.start_game()

if __name__ == "__main__":
    main()
