import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
from sklearn.decomposition import PCA
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tifffile

class PCAAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TIFF Görüntü PCA Analiz Aracı")
        self.root.geometry("1000x800")

        self.top_frame = tk.Frame(root, pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_load = tk.Button(self.top_frame, text="TIFF Görüntüsü Yükle", command=self.load_image, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.btn_load.pack(side=tk.LEFT, padx=20)
        
        self.lbl_status = tk.Label(self.top_frame, text="Lütfen bir görüntü yükleyin...", font=("Arial", 10, "italic"))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.table_frame = tk.Frame(root, height=200)
        self.table_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        tk.Label(self.table_frame, text="PCA İstatistik Tablosu", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.tree = ttk.Treeview(self.table_frame, columns=("Bileşen", "Açıklanan Varyans", "Varyans Oranı (%)", "Std. Sapma"), show="headings", height=6)
        self.tree.heading("Bileşen", text="Bileşen (PC)")
        self.tree.heading("Açıklanan Varyans", text="Açıklanan Varyans (Eigenvalue)")
        self.tree.heading("Varyans Oranı (%)", text="Varyans Oranı (%)")
        self.tree.heading("Std. Sapma", text="Standart Sapma")
        
        self.tree.column("Bileşen", anchor="center", width=100)
        self.tree.column("Açıklanan Varyans", anchor="center", width=150)
        self.tree.column("Varyans Oranı (%)", anchor="center", width=150)
        self.tree.column("Std. Sapma", anchor="center", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.image_path = None
        self.original_image = None
        self.pca_result = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("TIFF Images", "*.tif *.tiff"), ("All Files", "*.*")])
        if not file_path:
            return

        try:
            self.image_path = file_path
            self.lbl_status.config(text=f"Yüklenen Dosya: {file_path.split('/')[-1]} | İşleniyor...")
            self.root.update()
            
            try:
                self.original_image = tifffile.imread(file_path)
            except Exception:
                img = Image.open(file_path)
                self.original_image = np.array(img)

            self.perform_pca()

        except Exception as e:
            messagebox.showerror("Hata", f"Görüntü işlenirken hata oluştu:\n{e}")
            self.lbl_status.config(text="Hata oluştu.")

    def perform_pca(self):
        img_shape = self.original_image.shape
        
        if len(img_shape) == 2:
            messagebox.showwarning("Uyarı", "Tek kanallı (Grayscale) görüntülerde PCA spektral analiz için uygun değildir. Yine de işlem deneniyor...")
            flat_img = self.original_image.reshape(-1, 1)
        else:
            flat_img = self.original_image.reshape(-1, img_shape[2])

        n_components = min(flat_img.shape[1], 10)
        pca = PCA(n_components=n_components)
        transformed_data = pca.fit_transform(flat_img)
        
        pc1_image = transformed_data[:, 0].reshape(img_shape[0], img_shape[1])

        explained_variance = pca.explained_variance_
        explained_variance_ratio = pca.explained_variance_ratio_ * 100
        std_deviation = np.sqrt(explained_variance)

        self.update_table(n_components, explained_variance, explained_variance_ratio, std_deviation)

        self.plot_results(pc1_image)
        self.lbl_status.config(text="PCA Analizi Tamamlandı.")

    def update_table(self, n, variances, ratios, std_devs):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for i in range(n):
            self.tree.insert("", "end", values=(
                f"PC{i+1}",
                f"{variances[i]:.4f}",
                f"%{ratios[i]:.2f}",
                f"{std_devs[i]:.4f}"
            ))

    def plot_results(self, pc1_img):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        
        if len(self.original_image.shape) > 2:
            disp_img = self.original_image[:, :, :3] if self.original_image.shape[2] >= 3 else self.original_image[:,:,0]
        else:
            disp_img = self.original_image
            
        ax1.imshow(disp_img, cmap='gray' if len(self.original_image.shape) == 2 else None)
        ax1.set_title("Orijinal Görüntü (RGB/Preview)")
        ax1.axis('off')

        im2 = ax2.imshow(pc1_img, cmap='viridis')
        ax2.set_title("PCA Sonucu (1. Temel Bileşen)")
        ax2.axis('off')
        
        plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = PCAAnalyzerApp(root)
    root.mainloop()