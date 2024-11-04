import subprocess
import time
import tkinter as tk
from tkinter import messagebox

steam_path = "C:\Program Files (x86)\Steam\steam.exe"

class FarmSteam:
    def __init__(self, root):
        self.root = root
        self.root.title("FarmSteam")
        self.root.geometry("400x300")

        self.processes = []
        self.game_app_ids = []

        tk.Label(root, text="AppID do Jogo:").pack()
        self.app_id_entry = tk.Entry(root)
        self.app_id_entry.pack()

        tk.Button(root, text="Adicionar Jogo", command=self.add_game).pack()
        tk.Button(root, text="Remover Jogo", command=self.remove_game).pack()

        tk.Label(root, text="Duracao do Farm (em horas):").pack()  # Alterado aqui
        self.duration_entry = tk.Entry(root)
        self.duration_entry.pack()

        tk.Button(root, text="Iniciar Farm", command=self.start_farm).pack()
        tk.Button(root, text="Parar Farm", command=self.stop_farm).pack()

        self.games_list = tk.Listbox(root)
        self.games_list.pack(fill=tk.BOTH, expand=True)

    def add_game(self):
        app_id = self.app_id_entry.get()
        if app_id:
            self.game_app_ids.append(app_id)
            self.games_list.insert(tk.END, f"AppID {app_id}")
            self.app_id_entry.delete(0, tk.END)

    def remove_game(self):
        selected = self.games_list.curselection()
        if selected:
            index = selected[0]
            self.games_list.delete(index)
            del self.game_app_ids[index]

    def start_game(self, app_id):
        """Inicia o processo do jogo usando o Steam."""
        process = subprocess.Popen([steam_path, "-applaunch", app_id])
        return process

    def start_farm(self):
        duration_hours = self.duration_entry.get()
        try:
            duration_seconds = int(duration_hours) * 3600
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor válido para a duração.")
            return

        for app_id in self.game_app_ids:
            process = self.start_game(app_id)
            self.processes.append(process)
            self.games_list.insert(tk.END, f"Iniciando AppID {app_id}...")

        self.root.after(duration_seconds * 1000, self.stop_farm)
        messagebox.showinfo("Farm Iniciado", "O farm de horas foi iniciado.")

    def stop_farm(self):
        for process in self.processes:
            process.terminate()
        self.processes.clear()
        self.games_list.insert(tk.END, "Todos os jogos foram encerrados.")
        messagebox.showinfo("Farm Parado", "O farm de horas foi encerrado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FarmSteam(root)
    root.mainloop()
