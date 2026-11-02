# Load Combinations for CSi Software

A short Python script that turns a load combination matrix into text ready to import into CSi SAFE or ETABS. Typing in hundreds of combinations by hand is slow and error-prone. With this script, you keep the matrix in Excel and generate the import text from it.

## Input

The input is one row per combination: its name, its type, then a load factor under each load case or combination it includes. A column headed with another combination's name nests that combination (ETABS writes it as `LOADCOMBO`). See [`examples/load_combinations.csv`](examples/load_combinations.csv):

| LOAD COMBO | COMBO TYPE | SW | SDL | LL | WL_0 | WL_90 | ULS Gravity | ULS Wind 0 | ULS Wind 90 |
|---|---|---|---|---|---|---|---|---|---|
| ULS Gravity | Linear add | 1.35 | 1.35 | 1.5 | | | | | |
| ULS Wind 0 | Linear add | 1.35 | 1.35 | 1.05 | 1.5 | | | | |
| ULS Wind 90 | Linear add | 1.35 | 1.35 | 1.05 | | 1.5 | | | |
| SLS Characteristic | Linear add | 1 | 1 | 1 | | | | | |
| ULS Envelope | Envelope | | | | | | 1 | 1 | 1 |

## Output

SAFE (default), in the format of its Load Combination Definitions table ([full file](examples/load_combinations_safe.txt)):

```
   Name="ULS Wind 0"   Type="Linear add"   "Is Auto"=No   "Load Name"="SW"   SF=1.35
   Name="ULS Wind 0"   "Load Name"="SDL"   SF=1.35
   Name="ULS Wind 0"   "Load Name"="LL"   SF=1.05
   Name="ULS Wind 0"   "Load Name"="WL_0"   SF=1.5
```

ETABS, with `--format etabs`, in the `COMBO` syntax of its text model files ([full file](examples/load_combinations_etabs.txt)):

```
  COMBO "ULS Envelope"  TYPE "Envelope"
  COMBO "ULS Envelope"  LOADCOMBO "ULS Gravity"  SF 1.0
  COMBO "ULS Envelope"  LOADCOMBO "ULS Wind 0"  SF 1.0
  COMBO "ULS Envelope"  LOADCOMBO "ULS Wind 90"  SF 1.0
```

## Usage

With [uv](https://docs.astral.sh/uv/):

```sh
uv run src/generateLoadCombinations.py examples/load_combinations.csv out.txt                  # SAFE
uv run src/generateLoadCombinations.py examples/load_combinations.csv out.txt --format etabs   # ETABS
```

The matrix can also be an `.xlsx` file. Without uv, run `pip install pandas openpyxl` and then run the script with `python`.
