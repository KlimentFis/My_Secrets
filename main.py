import sys

def main():
    if len(sys.argv) > 1:
        if sys.argv[1]:
            print("Yes")
            return
    print("No")

if __name__ == "__main__":
    main()