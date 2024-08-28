# Sickle 2

## Prerequisite

- [Xornet-Euphoria/pickaxe: Pickle hand assembler (WIP)](https://github.com/Xornet-Euphoria/pickaxe): ビルドに必要 (ソルバには不要)

## ファイルの説明

- [poc.py](./poc.py): [chall.pkl](./chall.pkl)を生成
- [chall.py](./chall.py): [chall.pkl](./chall.pkl)と共に配布
- [writeup.md](./writeup.md): 作問者Writeup (一部未完、そのうち完全版を公表予定)
- [solve.sage](./solve.sage): 入力の加工と比較部分に応じた、正答の入力を求めるだけのスクリプト
- [solve_simulate/](./solve_simulate/): [chall.pkl](./chall.pkl)から[solve.sage](./solve.sage)で使う値を抽出する過程をある程度再現したディレクトリ
- [unused](./unused/): 入力チェックのために実装を考えていたが採用しなかったもの
