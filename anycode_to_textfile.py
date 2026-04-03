import os
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD

EXCLUDED_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", "coverage",
    "__pycache__", ".idea", ".vscode", ".turbo", ".vercel",
    "target", "bin", "obj", ".pytest_cache", ".mypy_cache"
}

EXCLUDED_FILES = {
    ".DS_Store", "Thumbs.db", "desktop.ini"
}

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def is_probably_binary(file_path: Path) -> bool:
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(8192)

        if not chunk:
            return False

        if b"\x00" in chunk:
            return True

        text_bytes = set(range(32, 127)) | {7, 8, 9, 10, 12, 13, 27}
        non_text = sum(byte not in text_bytes for byte in chunk)
        return (non_text / len(chunk)) > 0.30
    except Exception:
        return True


def should_skip_file(file_path: Path, output_path: Path):
    try:
        if file_path.resolve() == output_path.resolve():
            return True, "output file itself"
    except Exception:
        pass

    if file_path.name in EXCLUDED_FILES:
        return True, "excluded filename"

    try:
        size = file_path.stat().st_size
        if size > MAX_FILE_SIZE_BYTES:
            return True, f"too large (> {MAX_FILE_SIZE_MB} MB)"
    except Exception:
        return True, "unreadable size"

    if is_probably_binary(file_path):
        return True, "binary file"

    return False, ""


def read_text_file(file_path: Path) -> str:
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc, errors="strict") as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"[ERROR READING FILE: {e}]"

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"[ERROR READING FILE: {e}]"


def collect_from_folder(folder_path: Path, output_path: Path):
    included = []
    skipped = []

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for filename in files:
            file_path = Path(root) / filename
            skip, reason = should_skip_file(file_path, output_path)

            if skip:
                skipped.append((file_path, reason))
            else:
                included.append(file_path)

    return included, skipped


def collect_from_inputs(input_paths, output_path: Path):
    included = []
    skipped = []

    for path in input_paths:
        if path.is_dir():
            inc, sk = collect_from_folder(path, output_path)
            included.extend(inc)
            skipped.extend(sk)
        elif path.is_file():
            skip, reason = should_skip_file(path, output_path)
            if skip:
                skipped.append((path, reason))
            else:
                included.append(path)

    # dedupe
    unique_included = {}
    for p in included:
        try:
            unique_included[str(p.resolve())] = p
        except Exception:
            unique_included[str(p)] = p

    unique_skipped = {}
    for p, reason in skipped:
        key = str(p)
        if key not in unique_skipped:
            unique_skipped[key] = (p, reason)

    included_list = sorted(unique_included.values(), key=lambda x: str(x).lower())
    skipped_list = sorted(unique_skipped.values(), key=lambda x: str(x[0]).lower())

    return included_list, skipped_list


def make_output_filename(input_paths):
    desktop = Path.home() / "Desktop"

    if len(input_paths) == 1 and input_paths[0].is_dir():
        base_name = input_paths[0].name
    elif len(input_paths) == 1 and input_paths[0].is_file():
        base_name = input_paths[0].stem
    else:
        base_name = "mixed_selection"

    safe_name = base_name.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return desktop / f"{safe_name}_combined_{timestamp}.txt"


def write_combined_file(input_paths):
    output_path = make_output_filename(input_paths)
    included_files, skipped_files = collect_from_inputs(input_paths, output_path)

    with open(output_path, "w", encoding="utf-8") as out:
        out.write("PROJECT COMBINED EXPORT\n")
        out.write(f"CREATED: {datetime.now().isoformat(timespec='seconds')}\n")
        out.write(f"TOTAL INPUT PATHS: {len(input_paths)}\n")
        out.write(f"TOTAL INCLUDED FILES: {len(included_files)}\n")
        out.write(f"TOTAL SKIPPED FILES: {len(skipped_files)}\n")
        out.write("=" * 120 + "\n\n")

        out.write("INPUT PATHS\n")
        out.write("-" * 120 + "\n")
        for p in input_paths:
            out.write(f"{p}\n")
        out.write("\n" + "=" * 120 + "\n\n")

        out.write("SKIPPED FILES SUMMARY\n")
        out.write("-" * 120 + "\n")
        for file_path, reason in skipped_files:
            out.write(f"{file_path}  -->  {reason}\n")
        out.write("\n" + "=" * 120 + "\n\n")

        for index, file_path in enumerate(included_files, start=1):
            try:
                size = file_path.stat().st_size
            except Exception:
                size = -1

            content = read_text_file(file_path)

            out.write("=" * 120 + "\n")
            out.write(f"FILE {index}/{len(included_files)}\n")
            out.write(f"PATH: {file_path}\n")
            out.write(f"SIZE: {size} bytes\n")
            out.write("=" * 120 + "\n\n")
            out.write(content)
            out.write("\n\n")

    return output_path, len(included_files), len(skipped_files)


class CodeToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code / File to Text Combiner")
        self.root.geometry("860x620")
        self.root.configure(bg="white")

        self.input_paths = []

        title = tk.Label(
            root,
            text="Drop files/folders anywhere in this window",
            font=("Segoe UI", 16, "bold"),
            bg="white"
        )
        title.pack(pady=(14, 8))

        sub = tk.Label(
            root,
            text="You can also use Select Folder / Select Files",
            font=("Segoe UI", 10),
            bg="white"
        )
        sub.pack(pady=(0, 10))

        btn_frame = tk.Frame(root, bg="white")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Select Folder", width=18, command=self.select_folder).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Select Files", width=18, command=self.select_files).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Clear List", width=18, command=self.clear_list).grid(row=0, column=2, padx=6)
        tk.Button(btn_frame, text="Create Combined Text File", width=24, command=self.create_output).grid(row=0, column=3, padx=6)

        self.drop_area = tk.Label(
            root,
            text="DROP HERE",
            relief="groove",
            bd=2,
            height=5,
            bg="#f3f6fb",
            font=("Segoe UI", 14, "bold")
        )
        self.drop_area.pack(fill="x", padx=20, pady=12)

        self.listbox = tk.Listbox(root, width=120, height=20)
        self.listbox.pack(padx=20, pady=8, fill="both", expand=True)

        self.status_label = tk.Label(root, text="Nothing selected yet.", anchor="w", bg="white")
        self.status_label.pack(fill="x", padx=20, pady=(0, 12))

        # Make BOTH the whole window and the drop area accept drops
        for widget in (self.root, self.drop_area, self.listbox):
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>", self.handle_drop)

    def parse_drop_data(self, data):
        items = self.root.tk.splitlist(data)
        paths = []

        for item in items:
            cleaned = item.strip().strip("{}").strip('"')
            if cleaned:
                paths.append(Path(cleaned))

        return paths

    def add_path(self, path):
        try:
            path = path.resolve()
        except Exception:
            pass

        if not path.exists():
            return

        current = set()
        for p in self.input_paths:
            try:
                current.add(str(p.resolve()))
            except Exception:
                current.add(str(p))

        try:
            key = str(path.resolve())
        except Exception:
            key = str(path)

        if key not in current:
            self.input_paths.append(path)
            self.listbox.insert(tk.END, str(path))

        self.update_status()

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select a folder")
        if folder:
            self.add_path(Path(folder))

    def select_files(self):
        files = filedialog.askopenfilenames(title="Select files")
        for f in files:
            self.add_path(Path(f))

    def clear_list(self):
        self.input_paths = []
        self.listbox.delete(0, tk.END)
        self.update_status()

    def update_status(self, extra=""):
        base = f"Selected items: {len(self.input_paths)}"
        if extra:
            base += f" | {extra}"
        self.status_label.config(text=base)

    def handle_drop(self, event):
        dropped_paths = self.parse_drop_data(event.data)

        added = 0
        for p in dropped_paths:
            before = len(self.input_paths)
            self.add_path(p)
            if len(self.input_paths) > before:
                added += 1

        self.update_status(f"Dropped: {added} new item(s)")

    def create_output(self):
        if not self.input_paths:
            messagebox.showwarning("Nothing selected", "Add at least one file or folder first.")
            return

        try:
            output_path, included_count, skipped_count = write_combined_file(self.input_paths)
            self.update_status(f"Done: {included_count} included, {skipped_count} skipped")
            messagebox.showinfo(
                "Done",
                f"Created:\n{output_path}\n\nIncluded: {included_count}\nSkipped: {skipped_count}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = TkinterDnD.Tk()
    app = CodeToTextApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()