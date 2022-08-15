use std::{collections::HashMap, io};

#[derive(Debug, Clone)]
struct Matrice {
    column: i8,
    line: i8,
}

impl Matrice {
    fn new(column: i8, line: i8) -> Matrice {
        Matrice { column, line }
    }
}

struct Board {
    board: Vec<Vec<i8>>,
    players: Vec<Player>,
    player_turn: u8,
}

impl Board {
    fn print_board(&self) {
        let mut hash_map_icon: HashMap<i8, char> = HashMap::new();
        hash_map_icon.insert(self.players[0].nb_in_board, self.players[0].icon_in_board);
        hash_map_icon.insert(self.players[1].nb_in_board, self.players[1].icon_in_board);
        hash_map_icon.insert(0, ' ');

        println!("---------------\n");

        for line in &self.board {
            for cell in line {
                match hash_map_icon.get(cell) {
                    Some(icon) => print!("|{}", icon),
                    None => panic!("Error: invalid icon in cell"),
                };
            }
            println!("|");
        }

        println!();

        self.print_players_attribut();

        println!("---------------\n");
    }

    fn print_players_attribut(&self) {
        for player in &self.players {
            println!("{} : {}", player.name, player.icon_in_board);
        }
    }

    fn get_player_turn(&self) -> &Player {
        let player: Option<&Player> = self.players.get(self.player_turn as usize);
        match player {
            Some(player) => return player,
            None => panic!("Error: player turn invalid"),
        };
    }

    fn is_valid_number(&self, column_index: isize) -> bool {
        0 <= column_index && column_index <= 6
    }

    fn can_place_piece(&self, column: usize) -> bool {
        self.get_free_place_line(column) != -1
    }

    fn get_free_place_line(&self, column: usize) -> isize {
        // iterate lines
        for x in (0..=self.board.len() - 1).rev() {
            // get nb in board
            let nb_in_board = match self.board[x].get(column) {
                Some(nb) => nb,
                None => {
                    panic!("Invalid variable in board");
                }
            };

            // can put one piece
            if nb_in_board == &0 {
                return x as isize;
            }
        }
        // colume full
        return -1;
    }

    fn get_cell_mut(&mut self, matrice: &Matrice) -> Result<&mut i8, io::ErrorKind> {
        //get line
        match self.board.get_mut(matrice.line as usize) {
            Some(line) => {
                // get cell from column and line
                match line.get_mut(matrice.column as usize) {
                    Some(nb_in_board) => Ok(nb_in_board),
                    None => Err(io::ErrorKind::Other),
                }
            }
            None => Err(io::ErrorKind::Other),
        }
    }

    fn get_cell(&self, matrice: &Matrice) -> Result<i8, io::ErrorKind> {
        //get line
        match self.board.get(matrice.line as usize) {
            Some(line) => {
                // get cell from column and line
                match line.get(matrice.column as usize) {
                    Some(nb_in_board) => Ok(*nb_in_board),
                    None => Err(io::ErrorKind::Other),
                }
            }
            None => Err(io::ErrorKind::Other),
        }
    }

    fn place_piece(&mut self, column: usize) -> Matrice {
        let line = self.get_free_place_line(column);
        let player_turn_nb_in_board: i8 = self.get_player_turn().nb_in_board.clone() as i8;

        // invalid column
        if line == -1 {
            panic!("Error the column given is full, cannot place piece");
        }

        let matrice: Matrice = Matrice {
            line: line as i8,
            column: column as i8,
        };

        let nb_in_board: &mut i8 = match self.get_cell_mut(&matrice) {
            Ok(nb_in_board) => nb_in_board,
            Err(_) => panic!("Error: cell does not exist"),
        };

        *nb_in_board = player_turn_nb_in_board;

        Matrice {
            column: column as i8,
            line: line as i8,
        }
    }

    fn chance_turn(&mut self) {
        if self.player_turn == 0 {
            self.player_turn = 1;
        } else {
            self.player_turn = 0;
        }
    }

    fn check_victory(&self, matrice: &Matrice) -> i8 {
        let mut matrice_list: Vec<Matrice> = vec![Matrice::new(0, 0); 4];
        let mut cell_values: Vec<i8> = vec![0; 4];

        //check lines victory
        'main_loop_lines: for i in 0..4 {
            for x in 0..=3 {
                // update matrices
                matrice_list[x as usize] = Matrice::new(matrice.column - x + i as i8, matrice.line);
                //println!("matrice_list = {:?}", matrice_list);

                // check if the cell exists
                match self.get_cell(&matrice_list[x as usize]) {
                    Ok(value) => cell_values[x as usize] = value,
                    Err(_) => {
                        continue 'main_loop_lines;
                    }
                }
            }

            if cell_values == vec![-1; 4] || cell_values == vec![1; 4] {
                return cell_values[0];
            }
        } // line

        // check columns
        'main_loop_col: for i in 0..4 {
            for x in 0..=3 {
                // update matrices
                matrice_list[x as usize] = Matrice::new(matrice.column, matrice.line - x + i as i8);

                // check if the cell exists
                match self.get_cell(&matrice_list[x as usize]) {
                    Ok(value) => cell_values[x as usize] = value,
                    Err(_) => {
                        continue 'main_loop_col;
                    }
                }
            }

            if cell_values == vec![-1; 4] || cell_values == vec![1; 4] {
                return cell_values[0];
            }
        } // columns

        // check diagonals like this one : /
        'main_loop_diag_forward: for i in 0..4 {
            for x in 0..=3 {
                // update matrices
                matrice_list[x as usize] =
                    Matrice::new(i + matrice.column - x, i + matrice.line - x);

                // check if cell exists
                match self.get_cell(&matrice_list[x as usize]) {
                    Ok(value) => cell_values[x as usize] = value,
                    Err(_) => {
                        continue 'main_loop_diag_forward;
                    }
                }
            }

            if cell_values == vec![-1; 4] || cell_values == vec![1; 4] {
                return cell_values[0];
            }
        }

        // check diagonales like this one : \
        'main_loop_diag_backward: for i in 0..4 {
            for x in 0..=3 {
                // update matrices
                matrice_list[x as usize] =
                    Matrice::new(i + matrice.column - x, i + matrice.line + x);

                // check if cell exists
                match self.get_cell(&matrice_list[x as usize]) {
                    Ok(value) => cell_values[x as usize] = value,
                    Err(_) => {
                        continue 'main_loop_diag_backward;
                    }
                }
            }

            if cell_values == vec![-1; 4] || cell_values == vec![1; 4] {
                return cell_values[0];
            }
        }

        return 0;
    }

    fn get_player_from_nb_in_board(&self, nb_in_board: i8) -> Option<&Player> {
        for player in &self.players {
            if player.nb_in_board == nb_in_board {
                return Some(&player);
            }
        }
        return None;
    }
}

struct Player {
    name: String,
    // player index refered to there own index in board
    nb_in_board: i8,
    icon_in_board: char,
}

impl Player {}

fn main() {
    let mut board = Board {
        board: vec![
            vec![0, 0, 0, 0, 0, 0, 0],
            vec![0, 0, 0, 0, 0, 0, 0],
            vec![0, 0, 0, 0, 0, 0, 0],
            vec![0, 0, 0, 0, 0, 0, 0],
            vec![0, 0, 0, 0, 0, 0, 0],
            vec![0, 0, 0, 0, 0, 0, 0],
        ],

        players: vec![
            Player {
                name: String::from(""),
                nb_in_board: -1,
                icon_in_board: 'N',
            },
            Player {
                name: String::from(""),
                nb_in_board: 1,
                icon_in_board: 'N',
            },
        ],

        player_turn: 0,
    };

    initialize_players(&mut board);
    

    board.print_board();

    let running = true;
    let mut winner: Option<&Player> = None;

    while running {
        let column_choice = get_player_choice(&mut board);
        let matrice: Matrice = board.place_piece(column_choice);
        board.chance_turn();
        board.print_board();
        let victory = board.check_victory(&matrice);

        if victory != 0 {
            winner = board.get_player_from_nb_in_board(victory);
            break;
        }
    }

    match winner {
        Some(winner) => println!(
            "Le joueur {} ({}) a gagné la partie !",
            winner.name, winner.icon_in_board
        ),
        None => panic!("Error: the winner does not exist !!!"),
    }
}

fn initialize_players(board: &mut Board) {
    for x in 0..board.players.len() {
        get_pseudo(board, x);
    }

    loop {
        let mut icon = String::new();
        println!(
            "{}, quel icône veux tu choisir : X (1), O (2)",
            board.players[0].name
        );

        io::stdin()
            .read_line(&mut icon)
            .expect("Error: cannot read line");

        icon = icon.trim_end().to_string();

        if icon.eq("1") || icon.eq("X") {
            board.players[0].icon_in_board = 'X';
            board.players[1].icon_in_board = 'O';
            break;
        } else if icon.eq("2") || icon.eq("O") {
            board.players[0].icon_in_board = 'O';
            board.players[1].icon_in_board = 'X';
            break;
        }
    }

    println!(
        "{} vous avez donc le signe '{}',\n{} vous avez le signe suivant : '{}'",
        board.players[0].name,
        board.players[0].icon_in_board,
        board.players[1].name,
        board.players[1].icon_in_board
    );
}

fn get_pseudo(board: &mut Board, index: usize) {
    let mut pseudo = String::new();
    println!("player {}, please give your pseudo", index + 1);
    io::stdin()
        .read_line(&mut pseudo)
        .expect("Error: cannot read line from user");

    pseudo = pseudo.trim_end().to_string();

    if pseudo.eq("") {
        println!("Le pseudo donné n'est pas valide");
        get_pseudo(board, index);
        return;
    }

    // same pseudo than the fiste player
    if index != 0 && pseudo.eq(&board.players[0].name) {
        println!("Vous ne pouvez pas prendre le pseudo du premier joueur !!");
        get_pseudo(board, index);
        return;
    }

    board.players[index].name = pseudo;
}

fn get_player_choice(board: &mut Board) -> usize {
    loop {
        let player = board.get_player_turn();

        let mut nb_column = String::new();

        print!(
            "{} ({}) c'est votre tour de jeu, dans quelle ligne veux tu mettre ton pion ?  ",
            player.name, player.icon_in_board
        );
        io::stdin()
            .read_line(&mut nb_column)
            .expect("Error : cannot get column numbre from user");

        // convert nb_turn into a integer
        let nb_column: usize = match nb_column.trim().parse() {
            Ok(nb) => nb,
            Err(_) => {
                println!("Le chiffre donné n'est pas correct (entre 1 et 7)");
                continue;
            }
        };

        let nb_col_index = nb_column - 1;

        // invaid number
        if !board.is_valid_number(nb_col_index as isize) {
            println!("Le nombre donné n'est pas correct, il doit être entre 1 et 7");
            continue;
        }

        if !board.can_place_piece(nb_col_index) {
            println!(
                "Le colonne n°{} est déjà pleine, veuillez réessayer",
                nb_column
            );
            continue;
        }

        return nb_col_index;
    }
}
