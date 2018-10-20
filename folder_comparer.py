"""
Review two folders and mention any differences they have in file content

Folder Comparing. Created by Ciaran Gruber - 19/10/18
"""

from pathlib import Path
import doctest

SAVE_FILE = 'files.txt'
MENU = """Menu:
(S)ave folder to check
(V)iew current folder contents
(C)ompare folders
(Q)uit"""


def compare_folders(folder_files, new_folder_path):
    """Review two folders and show any differences in their content"""
    original_differences = folder_files
    new_folder_differences = []
    for file in Path(new_folder_path).iterdir():
        new_folder_differences.append(str(file.name))
    original_files = original_differences[:]
    for i, file in enumerate(original_files):
        if file in new_folder_differences:
            original_differences.remove(file)
            new_folder_differences.remove(file)
    return original_differences, new_folder_differences


def main():
    """Get user input for the folders to compare"""
    print('Ciaran\'s folder comparing program')
    print(MENU)
    menu_option = input('Menu choice: ').upper()
    while menu_option != 'Q':
        print()
        if menu_option == 'S':
            try:
                folder = input('Folder path: ')
                with open(SAVE_FILE, 'w', encoding="utf-8") as files_folder:
                    for file in Path(folder).iterdir():
                        files_folder.write(str(file.name) + '\n')
            except FileNotFoundError:
                print('File path does not exist')
        elif menu_option == 'V':
            with open(SAVE_FILE, encoding="utf-8") as files_folder:
                files = [file.strip() for file in files_folder.readlines()]
                if len(files) > 0:
                    print('Files available')
                    columns = 1
                    table_data = ['Files']
                    while sum(get_column_widths(files, columns)) < 130 and not columns >= len(files):
                        columns += 1
                        table_data.append('Files')
                    print_table(table_data + files, columns)
                else:
                    print('No folder saved')
        elif menu_option == 'C':
            with open(SAVE_FILE, encoding="utf-8") as files_folder:
                folder_files = [file.strip() for file in files_folder.readlines()]
            if len(folder_files) == 0:
                print('No saved folder details')
            else:
                try:
                    folder = input('Folder path: ')
                    orig_diffs, new_diffs = compare_folders(folder_files, folder)
                    table_data = ['Original Folder', 'New Folder']
                    for file, file2 in zip(orig_diffs, new_diffs):
                        table_data.append(file)
                        table_data.append(file2)
                    if len(orig_diffs) > len(new_diffs):
                        for x in range(len(new_diffs), len(orig_diffs)):
                            table_data.append(orig_diffs[x])
                            table_data.append('')
                    elif len(new_diffs) > len(orig_diffs):
                        for x in range(len(orig_diffs), len(new_diffs)):
                            table_data.append('')
                            table_data.append(new_diffs[x])
                    print()
                    print('Files/Directories that do not exist in the other folder:')
                    print_table(table_data, 2)
                except FileNotFoundError:
                    print('File path does not exist')
        else:
            print('Invalid menu choice')
        print()
        print(MENU)
        menu_option = input('Menu choice: ').upper()


def print_table(data, column_count):
    """Print a table"""
    while len(data) % column_count != 0:
        data.append('')
    row_sizes = get_column_widths(data, column_count)
    print(' {:_<{}s}'.format('', sum(row_sizes) + column_count * 3 - 1))
    for x in range(column_count):
        print('| {:^{}} '.format(data[x], row_sizes[x]), end='')
    print('|')
    for x in range(column_count):
        print('|{:_<{}s}'.format('', row_sizes[x] + 2), end='')
    print('|')
    for x in range(column_count, len(data)):
        if x % column_count + 1 == column_count:
            print('| {:^{}} |'.format(data[x], row_sizes[x % column_count]))
            for a in range(column_count):
                print('|{:{}<{}s}'.format('', '_' if x >= len(data) - column_count else '-', row_sizes[a] + 2), end='')
            print('|')
        else:
            print('| {:^{}} '.format(data[x], row_sizes[x % column_count]), end='')


def get_column_widths(cells, column_count):
    """
    Get sizes of the rows for a table
    >>> print(get_column_widths(['Header', 'Header', 'Cell 1', 'Cell 2', 'Stuffy Stuff', 'Cel'], 2))
    [12, 6]
    """
    sizes = [0 for _ in range(column_count)]
    for i, file in enumerate(cells):
        if len(file) > sizes[i % column_count]:
            sizes[i % column_count] = len(file)
    return sizes


if __name__ == '__main__':
    doctest.testmod()
    main()
