import sys
import os


def print_usage_and_exit():
    print("Usage: grep search_string directory [-o outfile] [-i]")
    sys.exit(1)


def create_outfile(outfile):
    try:
        with open(outfile, "x") as f:
            pass
    except FileExistsError:
        print(f"Error: {outfile} already exists")
        sys.exit(1)


def read_from_stdin(search_string, case_sensitive, outfile):
    matches = []
    try:
        while True:
            line = input()
            if line == "":
                break
            if not case_sensitive:
                line = line.lower()
                search_string = search_string.lower()
            if search_string in line:
                matches.append(line)
                if outfile:
                    with open(outfile, "a") as f:
                        f.write(line + "\n")
    except EOFError:
        pass
    return matches


def read_from_directory(search_string, case_sensitive, outfile, dir_path):
    matches = []
    try:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        for line in f:
                            line = line.rstrip("\n")
                            if not case_sensitive:
                                line = line.lower()
                                search_string = search_string.lower()
                            if search_string in line:
                                matches.append(f"{file_path}:{line}")
                                if outfile:
                                    with open(outfile, "a") as out_f:
                                        out_f.write(f"{file_path}:{line}\n")
                                else:
                                    print(f"{file_path}:{line}")
    except FileNotFoundError:
        print(f"Error: {dir_path} not found")
        sys.exit(1)
    return matches


def main():
    if len(sys.argv) < 2:
        print_usage_and_exit()

    search_string = sys.argv[1]
    matches = []
    case_sensitive = True

    if "-o" in sys.argv:
        try:
            index = sys.argv.index("-o")
            outfile = sys.argv[index + 1]
            create_outfile(outfile)
        except IndexError:
            print("Error: Please provide an output file name after -o flag")
            sys.exit(1)
    else:
        outfile = None

    if "-i" in sys.argv:
        case_sensitive = False

    if len(sys.argv) == 2 or ("-o" in sys.argv and len(sys.argv) == 4):
        matches = read_from_stdin(search_string, case_sensitive, outfile)
    else:
        if "-o" in sys.argv:
            dir_path = sys.argv[2]
        else:
            dir_path = sys.argv[2]
        matches = read_from_directory(search_string, case_sensitive, outfile, dir_path)

    if not outfile:
        for match in matches:
            print(match)


if __name__ == "__main__":
    main()
