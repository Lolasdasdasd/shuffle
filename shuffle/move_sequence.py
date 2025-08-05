from pathlib import Path
import pandas as pd
from shuffle.path_config import DATADIR
import numpy as np
import random

class MovesDB():
    def __init__(self, csv_path:Path):
        self.df = pd.read_csv(csv_path, sep=",")

    def set_df(self, new_df:pd.DataFrame):
        self.df = new_df.copy()

    @property
    def moves(self) -> list[str]:
        mv = self.df["abbreviation"].unique()#.tolist()
        return mv[~pd.isna(mv)].tolist()
    
    @property
    def columns(self) -> list[str]:
        c = sorted(self.df.columns.tolist())
        return c


class MoveSequenceGenerator():
    def __init__(self, mdb:MovesDB):
        self.sequence = []
        self.mdb = mdb
        self.pointer = -1
        pass

    def walk(self) -> str:
        self.pointer += 1
        while self.pointer > len(self.sequence)-1:
            self.generate_batch()
        return self.sequence[self.pointer]
        

    def generate_batch(self):
        print("  generate batch")
        ap = self.mdb.moves
        random.shuffle(ap)
        self.sequence += ap



if __name__ == '__main__':
    mdb = MovesDB(DATADIR / "moves.csv")
    gen = MoveSequenceGenerator(mdb)
    for i in range(50):
        print(gen.walk())