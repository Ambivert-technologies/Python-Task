import pandas as pd
from PIL import Image, ImageFont, ImageDraw

def cal_padding(w, img_edit, key_is, i, k, df, tit_fnt):
    text_width, text_height = img_edit.textsize(f"{key_is} {df[k][i]}", font=tit_fnt)
    return ((w // 2) - (text_width // 2))


def send_data_for_image(mykey, df):
    for i in range(len(df)):
        w, h = df['Width'][i], df['Height'][i]
        shape = [(0, 0), (w, h)]

        # creating new Image object
        img = Image.new("RGB", (w, h))

        # create rectangle image
        tit_fnt = ImageFont.truetype("Input/myfont.ttf", 15)
        img_edit = ImageDraw.Draw(img)
        img_edit.rectangle(shape, fill="#ffffff")
        text_height = 40
        for k in mykey:
            key_is = ""
            if str(k).startswith("N/A")==False:
                key_is = k
            if str(k) != "Height" and str(k) != "Width":
                pad = cal_padding(w, img_edit, key_is, i, k, df, tit_fnt)
                img_edit.text((pad, text_height), f"{key_is} {df[k][i]}", (0, 0, 0), font=tit_fnt)
                text_height = text_height + 35
        # img.show()
        img.save(f"Output/image{i}.jpg")


def extract_data():
    global all_key
    df = pd.read_csv("Input/csvfile.csv")
    mykeys = df.keys()
    for i in mykeys:
        all_key.append(i)
    send_data_for_image(mykey=all_key, df=df)


if __name__ == "__main__":
    all_key = []
    extract_data()

    title = []
    df = pd.read_csv("Input/csvfile.csv")
    for i in range(len(df)):
        title.append(df["Title:"][i])

    df["Filename"] = title
    df.to_csv("./Output/Output.csv")