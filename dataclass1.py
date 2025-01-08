from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Product:
    name: str
    price: float
    cantidad: int
    contador_producto: ClassVar[int] = 0

    def __post_init__(self):
        try:
            if not self.name:
                raise ValueError("El nombre es un campo requerido")
            if self.price <= 0.0:
                raise ValueError("El precio debe ser mayor a 0.0")
            if self.cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
        except Exception as e:
            print(f"Error: {e}")



if __name__ == "__main__":
    producto1 = Product("Tv", 10.0, 2)
    # Variables de instancias
    print(producto1.__dict__)
    # Variables de clase
    print(Product.contador_producto)
