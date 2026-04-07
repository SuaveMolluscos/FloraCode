import tkinter as tk
import struct
import json
import zlib
import threading

class ASCIIVideoPlayer:
    """Reproductor de video ASCII desde archivo .bin con formato ASCF"""
    
    def __init__(self, parent, bin_path, on_complete=None):
        """
        parent: ventana principal (se ocultará durante la reproducción)
        bin_path: ruta al archivo .bin con los frames
        on_complete: función a llamar cuando termine la intro
        """
        self.parent = parent
        self.bin_path = bin_path
        self.on_complete = on_complete
        self.frames = []
        self.metadata = {}
        self.current_frame = 0
        self.is_playing = True
        self.after_id = None
        
        # Crear ventana splash sin bordes
        self.splash = tk.Toplevel(parent)
        self.splash.title("")
        
        # Eliminar todos los botones de ventana
        self.splash.overrideredirect(True)
        
        # Configurar fondo negro
        self.splash.configure(bg='black')
        
        # Centrar la ventana temporalmente (se ajustará después)
        self.splash.geometry("800x600+{}+{}".format(
            self.splash.winfo_screenwidth() // 2 - 400,
            self.splash.winfo_screenheight() // 2 - 300
        ))
        
        # Crear widget de texto para mostrar ASCII art
        self.text_widget = tk.Text(
            self.splash,
            bg='black',
            fg='#00ff00',  # Verde neón para efecto matrix
            font=('Courier', 10),
            wrap='none',
            bd=0,
            highlightthickness=0
        )
        self.text_widget.pack(expand=True, fill='both')
        self.text_widget.config(state='disabled')
        
        # Mostrar mensaje de carga
        self.loading_label = tk.Label(
            self.splash,
            text="Cargando intro...",
            bg='black',
            fg='gray',
            font=('Arial', 12)
        )
        self.loading_label.pack(pady=10)
        
        # Iniciar carga en segundo plano
        threading.Thread(target=self.load_video, daemon=True).start()
    
    def center_window(self, frame_width=None, frame_height=None):
        """Centra la ventana en la pantalla"""
        self.splash.update_idletasks()
        
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        
        # Calcular tamaño de ventana basado en el frame o usar valores por defecto
        if frame_width and frame_height:
            # Estimar tamaño en píxeles (cada caracter ~ ancho 8px, alto 16px)
            win_width = min(frame_width * 8 + 20, screen_width - 100)
            win_height = min(frame_height * 16 + 20, screen_height - 100)
        else:
            # Tamaño por defecto
            win_width = 800
            win_height = 600
        
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        
        self.splash.geometry(f"{win_width}x{win_height}+{x}+{y}")
    
    def load_video(self):
        """Carga y descomprime el archivo .bin en un hilo separado"""
        try:
            with open(self.bin_path, 'rb') as f:
                # Leer magic number
                magic = f.read(4)
                if magic != b'ASCF':
                    raise ValueError(f"Formato inválido: esperado ASCF, obtenido {magic}")
                
                # Leer versión y compresión
                version = struct.unpack('B', f.read(1))[0]
                compression_level = struct.unpack('B', f.read(1))[0]
                flags = struct.unpack('B', f.read(1))[0]
                
                # Leer metadatos
                metadata_len = struct.unpack('I', f.read(4))[0]
                metadata_json = f.read(metadata_len)
                self.metadata = json.loads(metadata_json.decode('utf-8'))
                
                # Leer datos comprimidos
                data_len = struct.unpack('I', f.read(4))[0]
                compressed_data = f.read(data_len)
                
                # Descomprimir
                decompressed = zlib.decompress(compressed_data)
                
                # Separar frames
                frames_data = decompressed.decode('utf-8').split('\x00')
                self.frames = frames_data[:-1] if frames_data[-1] == '' else frames_data
                
                print(f"✓ Video cargado: {self.metadata.get('title', 'Sin título')}")
                print(f"✓ Frames: {len(self.frames)}")
                
                # Mostrar información de metadatos disponibles
                print(f"✓ Metadatos encontrados: {list(self.metadata.keys())}")
                
                # Obtener dimensiones de los frames (calcular automáticamente si no están en metadatos)
                frame_width, frame_height = self.get_frame_dimensions()
                
                print(f"✓ Dimensiones detectadas: {frame_width}x{frame_height}")
                print(f"✓ FPS: {self.metadata.get('fps', 24)}")
                
                # Actualizar UI desde el hilo principal
                self.splash.after(0, lambda: self.video_loaded(frame_width, frame_height))
                
        except Exception as e:
            print(f"✗ Error cargando video: {e}")
            import traceback
            traceback.print_exc()
            self.splash.after(0, self.load_error, str(e))
    
    def get_frame_dimensions(self):
        """Obtiene las dimensiones del frame analizando el primer frame"""
        if not self.frames:
            return 80, 24  # Dimensiones por defecto
        
        # Analizar el primer frame
        first_frame = self.frames[0]
        lines = first_frame.split('\n')
        
        # Altura = número de líneas
        frame_height = len(lines)
        
        # Ancho = longitud máxima de línea
        frame_width = max(len(line) for line in lines) if lines else 80
        
        return frame_width, frame_height
    
    def video_loaded(self, frame_width, frame_height):
        """Callback cuando el video termina de cargarse"""
        # Eliminar mensaje de carga
        self.loading_label.destroy()
        
        # Guardar dimensiones
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Centrar ventana con las dimensiones correctas
        self.center_window(frame_width, frame_height)
        
        # Configurar el widget de texto
        self.text_widget.config(
            width=frame_width,
            height=frame_height
        )
        
        # Calcular tamaño de fuente óptimo
        self.calculate_font_size()
        
        # Iniciar reproducción
        self.play_next_frame()
    
    def calculate_font_size(self):
        """Calcula el mejor tamaño de fuente para la ventana actual"""
        try:
            # Obtener tamaño de la ventana
            win_width = self.splash.winfo_width()
            win_height = self.splash.winfo_height()
            
            # Calcular tamaño de fuente basado en dimensiones
            font_width_px = win_width // self.frame_width if self.frame_width > 0 else 8
            font_height_px = win_height // self.frame_height if self.frame_height > 0 else 16
            
            # Tamaño de fuente aproximado (puntos)
            font_size = max(6, min(20, font_height_px))
            
            self.text_widget.config(font=('Courier', font_size))
        except:
            # Si hay error, usar tamaño por defecto
            self.text_widget.config(font=('Courier', 10))
    
    def load_error(self, error_msg):
        """Muestra error si no se puede cargar el video"""
        self.loading_label.config(text=f"Error: {error_msg}", fg='red')
        # Esperar 2 segundos y cerrar
        self.splash.after(2000, self.close_splash)
    
    def play_next_frame(self):
        """Reproduce el siguiente frame de la animación"""
        if not self.is_playing or self.current_frame >= len(self.frames):
            # Terminó la animación
            print(f"✓ Reproducción completada ({self.current_frame} frames)")
            self.close_splash()
            return
        
        # Obtener el frame actual
        frame_text = self.frames[self.current_frame]
        
        # Actualizar el widget de texto
        self.text_widget.config(state='normal')
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', frame_text)
        self.text_widget.config(state='disabled')
        
        # Avanzar al siguiente frame
        self.current_frame += 1
        
        # Mostrar progreso cada 30 frames
        if self.current_frame % 30 == 0:
            print(f"Reproduciendo: {self.current_frame}/{len(self.frames)} frames")
        
        # Calcular delay basado en FPS (o usar 24 por defecto)
        fps = self.metadata.get('fps', 24)
        delay_ms = int(1000 / fps)
        
        # Programar el siguiente frame
        self.after_id = self.splash.after(delay_ms, self.play_next_frame)
    
    def close_splash(self):
        """Cierra la ventana splash y muestra la aplicación principal"""
        print("Cerrando intro...")
        
        # Detener la reproducción
        self.is_playing = False
        if self.after_id:
            self.splash.after_cancel(self.after_id)
        
        # Cerrar ventana splash
        self.splash.destroy()
        
        # Mostrar ventana principal
        if self.parent:
            self.parent.deiconify()
            self.parent.lift()
            self.parent.focus_force()
        
        # Llamar callback
        if self.on_complete:
            self.on_complete()
    
    def skip_intro(self):
        """Permite saltar la intro (opcional)"""
        self.close_splash()


# Función de conveniencia
def show_splash_with_video(parent_window, video_path, callback=None):
    """Muestra la intro con video ASCII"""
    player = ASCIIVideoPlayer(parent_window, video_path, callback)
    return player


# Prueba independiente
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    video_path = r"D:\My portfolio\FloraCode\assets\frames.bin"
    
    def on_complete():
        print("¡Intro terminada! Ahora cargaría el programa principal")
        root.deiconify()
        
        # Ejemplo de interfaz principal
        label = tk.Label(root, text="¡Programa Principal Cargado!", 
                        font=("Arial", 20), bg='black', fg='white')
        label.pack(expand=True, fill='both')
        root.geometry("400x300")
        
        # Centrar ventana principal
        root.eval('tk::PlaceWindow . center')
    
    # Mostrar intro
    player = show_splash_with_video(root, video_path, on_complete)
    
    # Opción: permitir saltar intro con Escape
    def on_escape(event):
        player.skip_intro()
    
    # Bindear escape después de que la ventana esté creada
    root.after(100, lambda: player.splash.bind('<Escape>', lambda e: player.skip_intro()))
    
    root.mainloop()