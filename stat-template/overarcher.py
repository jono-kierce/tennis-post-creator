import main
import pandas as pd
if __name__ == "__main__":
    df = pd.read_csv("main.csv", header=None)

    rows , cols = df.shape
    expected_cols = 2
    assert cols == expected_cols, f"CSV not in expected cols of {expected_cols}\n. Expected {expected_cols} cols, got {df.shape[1]}"

    for i in range(1,rows):
        post_caption = df[0][i]
        data_path = df[1][i]
        save_path = data_path.replace(".csv", ".png")
        print(f"Save path {save_path}")
        main.create_everything(data_path, blue_box_caption = post_caption, output_path=save_path)
