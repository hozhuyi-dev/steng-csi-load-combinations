'''
Convert a load combination matrix into text ready for import to CSi software.

The matrix has one row per load combination: its name, its type, then the load
factor for each load case or combination in the column headers (blank where
not used). It can be an Excel file or a CSV.

Usage:
    python generateLoadCombinations.py <matrix.xlsx|.csv> <output.txt> [--format safe|etabs]
'''

import argparse

import pandas as pd


def readMatrix(path):
    '''Read the matrix from an Excel file or a CSV'''
    if path.lower().endswith('.csv'):
        return pd.read_csv(path)
    return pd.read_excel(path)


def linesEtabs(df_data):
    '''Lines for an ETABS text file: the combination type, then each load case or combination'''
    list_loadcombo = list(df_data.iloc[:, 0])

    for i in range(df_data.shape[0]):
        # Write combination type
        yield '  COMBO "{}"  TYPE "{}"\n'.format(df_data.iloc[i, 0], df_data.iloc[i, 1])

        for j in range(2, df_data.shape[1]):
            factor = df_data.iloc[i, j]
            if pd.isna(factor):
                continue

            # Check if it is a load case or combo
            loadName = df_data.columns.values[j]
            loadtype = 'LOADCOMBO' if loadName in list_loadcombo else 'LOADCASE'

            # Write load factor
            yield '  COMBO "{}"  {} "{}"  SF {}\n'.format(df_data.iloc[i, 0], loadtype, loadName, float(factor))


def linesSafe(df_data):
    '''Lines for a SAFE table import: the combination type goes on its first line only'''
    for i in range(df_data.shape[0]):
        isFirst = True

        for j in range(2, df_data.shape[1]):
            factor = df_data.iloc[i, j]
            if pd.isna(factor):
                continue

            # Write load factor
            if isFirst:
                yield '   Name="{}"   Type="{}"   "Is Auto"=No   "Load Name"="{}"   SF={}\n'.format(
                    df_data.iloc[i, 0], df_data.iloc[i, 1], df_data.columns.values[j], float(factor))
            else:
                yield '   Name="{}"   "Load Name"="{}"   SF={}\n'.format(
                    df_data.iloc[i, 0], df_data.columns.values[j], float(factor))

            isFirst = False


def main():
    parser = argparse.ArgumentParser(description='Convert a load combination matrix into text for import to CSi software.')
    parser.add_argument('matrix', help='Excel file or CSV: name, type, then one column per load case or combination')
    parser.add_argument('output', help='Text file to write')
    parser.add_argument('--format', choices=['safe', 'etabs'], default='safe', help='Target software (default: safe)')
    args = parser.parse_args()

    df_data = readMatrix(args.matrix)
    lines = linesSafe(df_data) if args.format == 'safe' else linesEtabs(df_data)

    with open(args.output, 'w') as txtFile:
        txtFile.writelines(lines)


if __name__ == '__main__':
    main()
