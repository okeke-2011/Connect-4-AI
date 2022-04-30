import pandas as pd

from minimax_algorithm import engine, SavedMoves, sessionmaker


def show_all_learned_moves():
    Session = sessionmaker(bind=engine)
    session = Session()

    all_moves = session.query(SavedMoves)
    print(pd.read_sql(all_moves.statement, session.bind))

    # print("Board State\t\t\t\t\tOptimal Move")
    # for entry in all_moves:
    #     print(f"{entry.board_state}\t{entry.optimal_move}")


if __name__ == "__main__":
    show_all_learned_moves()
