try:
    from src.get_coverage import processedDataIntoList
except Exception as e:
    print("Import error in dbc_example.py.")
    print("Make sure you're running the command in the parent directory")

"""
how to run: 'python -m src.get_cvg_example',
while being situated in the parent directory of both src and how_it_works.
"""

def main():
    pair = processedDataIntoList(statusUpdates=True)
    lst = pair[0]
    ignored = pair[1]

    print(f"Processed {len(lst)} requests.")
    if ignored == 1:
        print(f"Ignored {len(lst)} request.")
    else:
        print(f"Processed {len(lst)} requests.")
    
    if len(lst) != 0:
        print(f"Example:")
        print(lst[0])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(f"Interrupted...")
    except Exception as e:
        print(f"An error occured: {e}")
