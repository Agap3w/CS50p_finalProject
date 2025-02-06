import chess

# Creazione della scacchiera
board = chess.Board()

print("Scacchiera iniziale:")
print(board)

# Effettuare una mossa (e2e4)
board.push_san("e2e4")
print("\nDopo la mossa e2e4:")
print(board)

# Verifica se la partita è terminata
if board.is_checkmate():
    print("Scacco matto!")
elif board.is_stalemate():
    print("Stallo!")
elif board.is_insufficient_material():
    print("Materiale insufficiente per vincere.")



print("Mosse legali:")
for move in board.legal_moves:
    print(move)


if board.is_check():
    print("Sei sotto scacco!")