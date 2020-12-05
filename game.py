class Reversi():
    def __init__(self, board_size=8):
        self.n = board_size
        self.over = False
        self.rounds = 0
        self.last_turn = "W"  # black always starts first
        self.board = self.new_board()
        self.flip_queue = Queue()

    def new_board(self):
        n = self.n
        board = []
        gap = int(n/2-1)
        for i in range(gap):
            board = board + [[None] * n]
        board = board + [[None] * gap + ["W", "B"] + [None] * gap]
        board = board + [[None] * gap + ["B", "W"] + [None] * gap]
        for i in range(gap):
            board = board + [[None]*n]
        return board

    def input_move(self, coord, colour):
        """
        y-values need to be translated:
            1,2,3,4,5,6,7,8
            7,6,5,4,3,2,1,0
        """
        x, y = int(coord[0]) - 1, int(coord[1]) - 1
        if not self.is_valid((x, y), colour):
            print("Invalid Move")
            return None
        self.board[y][x] = colour
        # flip all tiles
        self.flip_tiles()
        # switch players
        self.rounds += 1
        self.last_turn = colour

    def flip_tiles(self):
        """Flip the tiles that can be flipped"""
        q = self.flip_queue
        while not q.empty():
            coord = q.get()
            if coord:
                (x, y) = coord
                tile = self.board[y][x]
                self.board[y][x] = "B" if tile == "W" else "W"

    def show_board(self):
        board = self.board
        n = self.n
        # set chess board
        chess = ([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]])

        # create grey points for easier viewing
        points = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
                  (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
                  (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
                  (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
                  (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8),
                  (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8),
                  (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8),
                  (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]

        x = list(map(lambda x: x[0], points))
        y = list(map(lambda x: x[1], points))

        plt.figure(figsize=(10, 10))

        # Color
        cmap = colors.ListedColormap(['green', 'green'])
        plt.imshow(chess, cmap=cmap)

        # Putting tiles

        for y in range(n):
            for x in range(n):
                if board[y][x]:
                    plt.text(x+1, y+1, '●', fontsize=50, ha='center', va='center',
                             color='black' if board[y][x] == "B" else 'white')

        # Gridlines
        for i in range(1, n+2, 1):
            plt.axhline(i-0.5, color='black')
            plt.axvline(i-0.5, color='black')

        plt.xlim(0.5, n+0.5)
        plt.ylim(0.5, n+0.5)
        plt.show()

    def horizontal_check(self, coord, colour):
        q = self.flip_queue
        board = self.board
        n = self.n

        (x, y) = coord
        opp = "B" if colour == "W" else "W"
        directions = [-1, 1]
        row = board[y]
        for direction in directions:
            curr_x = x + direction
            tiles = []
            while (curr_x >= 0) if direction < 0 else (curr_x < n):  # switch directions as necessary
                if row[curr_x] == colour:
                    player_tiles = list(map(lambda x: x[2], tiles))
                    if opp in player_tiles:
                        # add tiles to flip queue if belonging to opponent
                        for tile in tiles:
                            q.put((tile[0], tile[1]))
                        return True
                    break
                else:
                    tiles.append((curr_x, y, row[curr_x]))
                curr_x += direction
        return False

    def vertical_check(self, coord, colour):
        n = self.n
        board = self.board
        q = self.flip_queue
        (x, y) = coord
        row = []
        opp = "B" if colour == "W" else "W"
        directions = [-1, 1]
        for direction in directions:
            curr_y = y + direction
            tiles = []
            while (curr_y >= 0) if direction < 0 else (curr_y < n):  # switch directions as necessary
                if board[curr_y][x] == colour:
                    player_tiles = list(map(lambda x: x[2], tiles))
                    if opp in player_tiles:
                        # add tiles to flip queue if belonging to opponent
                        for tile in tiles:
                            q.put((tile[0], tile[1]))
                        return True
                    break
                else:
                    tiles.append((x, curr_y, board[curr_y][x]))
                curr_y += direction
        return False

    def diagonal_down_check(self, coord, colour):
        n = self.n
        board = self.board
        q = self.flip_queue
        opp = "B" if colour == "W" else "W"
        directions = [-1, 1]
        for direction in directions:  # switch directions as necessary
            tiles = []
            current_x, current_y = coord

            if direction < 0:
                current_y -= 1
                current_x += 1
            else:
                current_y += 1
                current_x -= 1

            # end condition when traversing up /  traversing down
            while current_y > 0 and current_x > 0 and current_y < n and current_x < n:
                current_tile = board[current_y][current_x]
                if current_tile == colour:  # if tile belongs to player
                    player_tiles = list(map(lambda x: x[2], tiles))
                    if opp in player_tiles:
                        # add tiles to flip queue if belonging to opponent
                        for tile in tiles:
                            q.put((tile[0], tile[1]))
                        return True
                    break
                else:
                    tiles.append((current_x, current_y, current_tile))
                if direction < 0:
                    current_y -= 1
                    current_x += 1
                else:
                    current_y += 1
                    current_x -= 1
        return False

    def diagonal_up_check(self, coord, colour):
        n = self.n
        board = self.board
        q = self.flip_queue
        opp = "B" if colour == "W" else "W"
        directions = [-1, 1]
        for direction in directions:
            tiles = []
            current_x, current_y = coord
            if direction < 0:
                current_y -= 1
                current_x -= 1
            else:
                current_y += 1
                current_x += 1

            # traverse down
            while current_y > 0 and current_x > 0 and current_y < n and current_x < n:
                current_tile = board[current_y][current_x]
                if current_tile == colour:  # if tile belongs to player
                    player_tiles = list(map(lambda x: x[2], tiles))
                    if opp in player_tiles:
                        # add tiles to flip queue if belonging to opponent
                        for tile in tiles:
                            q.put((tile[0], tile[1]))
                        return True
                    break
                else:
                    tiles.append((current_x, current_y, current_tile))

                if direction < 0:
                    current_y -= 1
                    current_x -= 1
                else:
                    current_y += 1
                    current_x += 1
        return False

    def is_valid(self, coord, colour):
        n = self.n
        board = self.board
        if board[coord[1]][coord[0]]:
            print(f"A tile already exists here.")
            return False

        checks = [
            self.horizontal_check,
            self.vertical_check,
            self.diagonal_down_check,
            self.diagonal_up_check
        ]

        return any(list(map(lambda check: check(coord, colour), checks)))

    def current_player(self):
        return "B" if self.last_turn == "W" else "W"

    def translate_player(self, colour):
        return "Black" if colour == "B" else "White"

    def validate_and_marshal_move(self, move):
        try:
            elements = move.split(",")
            x, y = int(elements[0]), int(elements[1])
        except:
            print("Invalid format. Please enter: x,y")
        else:
            return (x, y)
        return None

    def check_valid_moves(self):
        """
        For now, since max tiles is 8*8, we can just look through all tiles that == None.

        Ideally, we can reduce search space by looking at current player's remaining moveset.
        If the player is unable to make a legal move, then we can consider the game to be over.
        """
        cp = self.current_player()
        for y in range(n):
            for x in range(n):
                if self.is_valid((x, y), cp):
                    self.flip_queue = Queue()
                    return
        self.flip_queue = Queue()
        self.over = True
        return

    def count_tiles_and_declare_winner(self):
        b, w = 0, 0
        for row in self.board:
            b += row.count("B")
            w += row.count("W")
        if b == w:
            return
        return "B" if b > w else "W"

    def reset(self):
        self.over = False
        self.board = self.new_board()
        self.rounds = 0
        self.last_turn = "W"
        self.flip_queue = Queue()

    def start(self):
        print("Welcome to Reversi")
        print("When prompted, enter an x,y coordinate like so: 1,2")
        print("Enjoy!")
        while True:
            self.reset()
            while not self.over:
                # check for valid movesets
                if self.rounds > 2:
                    break
                    self.check_valid_moves()
                current_player = self.current_player()
                name = self.translate_player(current_player)
                self.show_board()
                while current_player != self.last_turn:
                    move = input(f"{name}\'s turn to make a move: ")
                    coord = self.validate_and_marshal_move(move)
                    if coord:
                        self.input_move(coord, current_player)

            winner = self.count_tiles_and_declare_winner()
            if winner:
                print(
                    f"Congratulations, {self.translate_player(winner)}! You won!")
            else:
                print(f"It's a draw!")

            again = input("Would you like to play again (Y/N): ")
            if again.lower() == "y":
                pass
            else:
                break
        print("Thanks for playing!")
