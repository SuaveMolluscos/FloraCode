import tkinter as tk
import zlib

def decodificar_ascf(route):
    with open(route, 'rb') as archivo:
        if archivo.read(4) != b'ASCF':
            raise ValueError("It is not a valid ASCF file.")
        
        archivo.seek(3, 1)
        
        len_metadata = int.from_bytes(archivo.read(4), 'little')
        archivo.seek(len_metadata, 1)
        
        len_datos = int.from_bytes(archivo.read(4), 'little')
        datos_comprimidos = archivo.read(len_datos)
        datos = zlib.decompress(datos_comprimidos)
        
        return datos.decode('utf-8').split('\x00')
    
def splash():
    
    frame_delay_ms = 42
    color_text = 'white'
    
    try: 
        frames = decodificar_ascf("assets/frames.bin")

        if not frames:
            return False

        window = tk.Tk()

        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()

        gw = int(w // 3)
        gh = int(h // 1.3)

        pw = int((w // 2) - (gw // 2))
        ph = int((h // 2) - (gh // 2))

        window.title("Suave")
        window.geometry(f"{gw}x{gh}+{pw}+{ph}")
        window.config(background='#222222')

        label = tk.Label(window, 
                        text=frames[0], 
                        bg=window.cget('bg'), 
                        fg=color_text, 
                        justify='left', 
                        anchor='w', 
                        font=('courier', 7, 'normal'))

        label.pack(anchor='nw', expand=False, fill=None)

        def play(index=0):
            if index < len(frames):
                label.config(text=frames[index])
                window.after(frame_delay_ms, play, index + 1)
            else:
                window.after(0, window.destroy)

        def close(event):
            window.destroy()
        
        window.bind('<Escape>', close)

        play()

        window.overrideredirect(True)

        window.mainloop()

        return True

    except Exception as e:
        print("Error:", e)
        return False

finish = splash()
print(finish)