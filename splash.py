import tkinter as tk
import zlib

def decodificar_ascf(path):
    with open(path, 'rb') as f:
        if f.read(4) != b'ASCF':
            raise ValueError("Invalid ASCF file")

        f.seek(3, 1)  # skip version, compression, flags
        f.seek(int.from_bytes(f.read(4), 'little'), 1)  # skip metadata
        
        data = zlib.decompress(f.read(int.from_bytes(f.read(4), 'little')))
        return [f for f in data.decode().split('\x00') if f]

def splash(path="assets/frames.bin", delay=42, color='white'):
    try:
        frames = decodificar_ascf(path)
        if not frames:
            return False

        root = tk.Tk()
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        gw, gh = w // 3, int(h / 1.3)

        root.geometry(f"{gw}x{gh}+{(w-gw)//2}+{(h-gh)//2}")
        root.configure(bg='#222222')
        root.overrideredirect(True)

        label = tk.Label(root, text='', bg=root['bg'], fg=color,
                         justify='left', anchor='w',
                         font=('courier', 7))
        label.pack(anchor='nw')

        def play(i=0):
            if i >= len(frames):
                root.destroy()
                return
            label.config(text=frames[i])
            root.after(delay, play, i+1)

        root.bind('<Escape>', lambda e: root.destroy())
        play()
        root.mainloop()
        return True

    except Exception as e:
        print("Error:", e)
        return False