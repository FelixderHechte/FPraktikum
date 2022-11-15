# Diese Bibliothek dient dazu plots mit matplotlib als Bilder abzuspeichern, ohne whitespace
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

#speichert die am letzten aufgerufene Figur
def speichern(name, pad=50, dpi = 400, path=""):
    filename = path + name

    plt.tight_layout()
    plt.savefig(filename, dpi)

    padding = [-pad, -pad, pad, pad]

    bildFigur= Image.open(filename)
    imageBox = ImageOps.invert(image.convert("RGB")).getbbox()
    imageBox = tuple(np.asarray(imageBox)) + pad

    bildFigur.crop(imageBox).save(filename)
