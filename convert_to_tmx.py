import tkinter as tk
from tkinter import messagebox  # Importing the messagebox module
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.etree import ElementTree as ET
from xml.dom import minidom


class TMXConverterApp:
    def __init__(self, root):
        self.root = root
        root.title("TMX Converter")

        self.source_label = tk.Label(root, text="Source:")
        self.source_label.grid(row=0, column=0, padx=10, pady=10)

        self.source_entry = tk.Entry(root, width=30)
        self.source_entry.grid(row=0, column=1, padx=10, pady=10)

        self.target_label = tk.Label(root, text="Target:")
        self.target_label.grid(row=1, column=0, padx=10, pady=10)

        self.target_entry = tk.Entry(root, width=30)
        self.target_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Pair", command=self.add_pair)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.generate_button = tk.Button(root, text="Generate TMX", command=self.generate_tmx)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.pair_list = []

    def add_pair(self):
        source_text = self.source_entry.get()
        target_text = self.target_entry.get()

        if source_text and target_text:
            self.pair_list.append((source_text, target_text))
            self.source_entry.delete(0, tk.END)
            self.target_entry.delete(0, tk.END)

    def generate_tmx(self):
        if not self.pair_list:
            return

        tmx_data = self.create_tmx(self.pair_list)

        with open("chatgpt_test/output.tmx", "w", encoding="utf-8") as file:
            file.write(self.prettify(tmx_data))

        messagebox.showinfo("TMX Conversion", "TMX file generated successfully!")

    def create_tmx(self, source_target_pairs):
        tmx = Element('tmx', version='1.4')
        header = SubElement(tmx, 'header', segtype='sentence', o_tmf='unknown')
        body = SubElement(tmx, 'body')

        for source, target in source_target_pairs:
            tu = SubElement(body, 'tu')
            tuv_source = SubElement(tu, 'tuv', {'xml:lang': 'en'})
            seg_source = SubElement(tuv_source, 'seg')
            seg_source.text = source

            tuv_target = SubElement(tu, 'tuv', {'xml:lang': 'target_language_code'})
            seg_target = SubElement(tuv_target, 'seg')
            seg_target.text = target

        return tmx

    def prettify(self, elem):
        rough_string = tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


if __name__ == "__main__":
    root = tk.Tk()
    app = TMXConverterApp(root)
    root.mainloop()