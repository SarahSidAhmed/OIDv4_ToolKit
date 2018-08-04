# ---------------
# Date: 7/19/2018
# Place: Biella/Torino
# Author: EscVM & TArt
# Project: OID v4
# ---------------

"""
OID v4 Downloader
Download specific classes of the huge online dataset Open Image Dataset.

Licensed under the MIT License (see LICENSE for details)
------------------------------------------------------------

Usage:
"""


from sys import exit
from textwrap import dedent
from modules.parser import *
from modules.utils import *
from modules.downloader import *
from modules.show import *
from modules.csv_downloader import *

ROOT_DIR = ''
DEFAULT_OID_DIR = os.path.join(ROOT_DIR, 'OID')

if __name__ == '__main__':

    args = parser_arguments()

    if not args.Dataset:
        dataset_dir = os.path.join(DEFAULT_OID_DIR, 'Dataset')
        csv_dir = os.path.join(DEFAULT_OID_DIR, 'csv_folder')
    else:
        dataset_dir = os.path.join(DEFAULT_OID_DIR, args.Dataset)
        csv_dir = os.path.join(DEFAULT_OID_DIR, 'csv_folder')

    name_file_class = 'class-descriptions-boxable.csv'
    CLASSES_CSV = os.path.join(csv_dir, name_file_class)

    if args.command == 'download':

        if args.type_csv is None:
            print('Missing type_csv argument.')
            exit(1)
        if args.classes is None:
            print('Missing classes argument.')
            exit(1)
        if args.multiclasses is None:
            args.multiclasses = 0

        folder = ['train', 'validation', 'test']
        file_list = ['train-annotations-bbox.csv', 'validation-annotations-bbox.csv', 'test-annotations-bbox.csv']

        args.classes = [arg.replace('_', ' ') for arg in args.classes]

        if args.multiclasses == '0':

            mkdirs(dataset_dir, csv_dir, args.classes)

            for classes in args.classes:

                print("[INFO] Downloading {}.".format(classes))
                class_name = classes

                error_csv(name_file_class, csv_dir)
                df_classes = pd.read_csv(CLASSES_CSV, header=None)

                class_code = df_classes.loc[df_classes[1] == class_name].values[0][0]

                if args.type_csv == 'train':
                    name_file = file_list[0]
                    df_val = TTV(csv_dir, name_file)
                    download(args, df_val, folder[0], dataset_dir, class_name, class_code)

                elif args.type_csv == 'validation':
                    name_file = file_list[1]
                    df_val = TTV(csv_dir, name_file)
                    download(args, df_val, folder[1], dataset_dir, class_name, class_code)

                elif args.type_csv == 'test':
                    name_file = file_list[2]
                    df_val = TTV(csv_dir, name_file)
                    download(args, df_val, folder[2], dataset_dir, class_name, class_code)

                elif args.type_csv == 'all':
                    for i in range(3):
                        name_file = file_list[i]
                        df_val = TTV(csv_dir, name_file)
                        download(args, df_val, folder[i], dataset_dir, class_name, class_code)

                else:
                    print('[ERROR] csv file not specified')
                    exit(1)

        elif args.multiclasses == '1':

            class_list = args.classes
            print("[INFO] Downloading {} together.".format(class_list))
            multiclass_name = ['_'.join(class_list)]
            mkdirs(dataset_dir, csv_dir, multiclass_name)

            error_csv(name_file_class, csv_dir)
            df_classes = pd.read_csv(CLASSES_CSV, header=None)

            class_code_list = df_classes.loc[df_classes[1].isin(class_list)][0].values

            class_dict = dict(zip(class_list, class_code_list))

            for class_name in class_list:

                if args.type_csv == 'train':
                    name_file = file_list[0]
                    df_val = TTV(csv_dir, name_file)
                    download(args, df_val, folder[0], dataset_dir, class_name, class_dict[class_name], class_list)

                elif args.type_csv == 'validation':
                    name_file = file_list[1]
                    df_val = TTV(csv_dir, name_file)
                    download(args, df_val, folder[1], dataset_dir, class_name, class_dict[class_name], class_list)

                elif args.type_csv == 'test':
                    name_file = file_list[2]
                    df_val = TTV(csv_dir, name_file)
                    download(args, df_val, folder[2], dataset_dir, class_name, class_dict[class_name], class_list)

                elif args.type_csv == 'all':
                    for i in range(3):
                        name_file = file_list[i]
                        df_val = TTV(csv_dir, name_file)
                        download(args, df_val, folder[i], dataset_dir, class_name, class_dict[class_name], class_list)

    elif args.command == 'visualize':

        while (True):

            print("Which folder do you want to visualize (train, test, validation)? <exit>")
            image_dir = input("> ")
            if image_dir == 'exit':
                exit(1)
            print("Which class?")
            class_name = input("> ")

            download_dir = os.path.join(dataset_dir, image_dir, class_name)
            label_dir = os.path.join(dataset_dir, image_dir, class_name, 'Label')

            if not os.path.isdir(download_dir):
                print("[ERROR] Images folder not found")
                exit(1)
            if not os.path.isdir(label_dir):
                print("[ERROR] Labels folder not found")
                exit(1)

            index = 0

            print(dedent("""
                --------------------------------------------------------
                INFO:
                        - Press 'd' to select next image
                        - Press 'a' to select previous image
                        - Press 'w' to proceed at the previous menu
                        - You can resize the window if it's not optimal
                --------------------------------------------------------
                """))

            show(class_name, download_dir, label_dir, index)

            while True:

                progression_bar(len(os.listdir(download_dir))-1, index+1)

                k = cv2.waitKey(0) & 0xFF

                if k == ord('d'):
                    cv2.destroyAllWindows()
                    if index < len(os.listdir(download_dir)) - 2:
                        index += 1
                    show(class_name, download_dir, label_dir, index)
                elif k == ord('a'):
                    cv2.destroyAllWindows()
                    if index > 0:
                        index -= 1
                    show(class_name, download_dir, label_dir, index)
                elif k == ord('w'):
                    cv2.destroyAllWindows()
                    break
