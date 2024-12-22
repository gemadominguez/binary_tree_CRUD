from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json


 #<---- CARGA Y GUARDADO JSON----->

def load_products():
    try:
        with open("products.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return{}
    
def save_products(products):
    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)


def load_orders():
    try:
        with open("orders.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return{}
    
def save_orders(orders):
    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)





# <---------------DEFINICIONES CLASES PRODUCTOS ---------------->

# Interior/Estructura del nodo "producto"
class InteriorNodoProducto:
    def __init__(self, id:int, name:str, price:float, quantity:int, category:str = ""):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }

# Nodo que representa el producto en el árbol binario
class NodoProducto:
    def __init__(self, producto: InteriorNodoProducto):
        self.producto = producto
        self.izquierda = None
        self.derecha = None

# ÁRBOL BINARIO 
class ArbolBinarioProducto:
    def __init__(self):
        self.raiz = None  

# <--------Métodos de inserción, búsqueda y eliminaciónL---------------------->

    #INSERTAR nodo
    def insertar(self, nodo: NodoProducto): 
        if self.raiz is None:
            self.raiz = nodo  
        else:
            self.insertar_en_nodo(self.raiz, nodo) 

    def insertar_en_nodo(self, nodo_actual: NodoProducto, nodo_nuevo: NodoProducto):
        if nodo_nuevo.producto.id < nodo_actual.producto.id:
            if nodo_actual.izquierda is None: 
                nodo_actual.izquierda = nodo_nuevo 
            else:
                self.insertar_en_nodo(nodo_actual.izquierda, nodo_nuevo)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = nodo_nuevo
            else:
                self.insertar_en_nodo(nodo_actual.derecha, nodo_nuevo)
    
    #BUSCAR nodo
    def buscar(self, id_producto: int):
        return self.busqueda(self.raiz, id_producto)
    
    def busqueda(self, nodo_actual: NodoProducto, id_producto: int):
        if nodo_actual is None:
            return None
        if id_producto == nodo_actual.producto.id: 
            return nodo_actual 
        elif id_producto < nodo_actual.producto.id:
            return self.busqueda(nodo_actual.izquierda, id_producto)
        else:
            return self.busqueda(nodo_actual.derecha, id_producto)

    #ELIMINAR nodo
    def eliminar(self, id_producto: int):
        return self.eliminando(self.raiz, id_producto)

    def eliminando(self, nodo_actual: NodoProducto, id_producto: int):
        if nodo_actual is None:
            return None  
        if id_producto == nodo_actual.producto.id:
            if nodo_actual.izquierda is None and nodo_actual.derecha is None:
                if nodo_actual == self.raiz:
                    self.raiz = None
                return None
            elif nodo_actual.izquierda is None:
                if nodo_actual == self.raiz:
                    self.raiz = nodo_actual.derecha
                return nodo_actual.derecha
            elif nodo_actual.derecha is None:
                if nodo_actual == self.raiz:
                    self.raiz = nodo_actual.izquierda
                return nodo_actual.izquierda
            else:
                nodo_minimo = self.obtener_minimo(nodo_actual.derecha)
                nodo_actual.producto = nodo_minimo.producto
                nodo_actual.derecha = self.eliminando(nodo_actual.derecha, nodo_minimo.producto.id)
        elif id_producto < nodo_actual.producto.id:
            nodo_actual.izquierda = self.eliminando(nodo_actual.izquierda, id_producto)
        else:
            nodo_actual.derecha = self.eliminando(nodo_actual.derecha, id_producto)
        return nodo_actual

    def obtener_minimo(self, nodo: NodoProducto):
        nodo_actual = nodo
        while nodo_actual.izquierda is not None:
            nodo_actual = nodo_actual.izquierda
        return nodo_actual

    #ACTUALIZAR nodo
    def actualizar(self, id_producto: int, nuevo_producto: InteriorNodoProducto):
        nodo_a_actualizar = self.buscar(id_producto)
        if nodo_a_actualizar:
            nodo_a_actualizar.producto = nuevo_producto  
            return True
        return False
    

# <-------------Cargar productos desde JSON Y Añadirlo al arbol ----------------->

def cargar_productos_desde_json():
    try:
        with open("products.json", "r") as file:
            productos_json = json.load(file)
            # Crear el árbol binario a partir de los productos cargados
            arbol_productos = ArbolBinarioProducto()
            for producto_data in productos_json.values():
                producto = InteriorNodoProducto(**producto_data)
                nodo_producto = NodoProducto(producto)
                arbol_productos.insertar(nodo_producto)
            return arbol_productos
    except FileNotFoundError:
        return ArbolBinarioProducto() 



# <---------------DEFINICIONES CLASES PEDIDOS ---------------->

# Interior/Estructura del nodo "pedido"
class InteriorNodoPedido:
    def __init__(self, id_pedido: int):
        self.id_pedido = id_pedido
        self.productos = []  # Aqui se almacenan los productos
    
    # Agregar producto al pedido
    def agregar_producto(self, producto: NodoProducto):
        self.productos.append(producto)

# Nodo que representa el pedido en el árbol binario
class NodoPedido:
    def __init__(self, pedido: InteriorNodoPedido):
        self.pedido = pedido
        self.siguiente = None

class ListaEnlazadaPedidos:
    def __init__(self):
        self.cabeza = None  


# <--------Métodos de inserción, búsqueda y eliminación---------------------->
    
    # Agregar un pedido a la lista
    def agregar_pedido(self, pedido: NodoPedido):
        nuevo_nodo = NodoPedido(pedido)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            nodo_actual = self.cabeza
            while nodo_actual.siguiente is not None:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo
    
    # Buscar un pedido por ID
    def buscar_pedido(self, id_pedido: int):
        nodo_actual = self.cabeza
        while nodo_actual is not None:
            if nodo_actual.pedido.id_pedido == id_pedido:
                return nodo_actual.pedido
            nodo_actual = nodo_actual.siguiente
        return None  
    
    # Eliminar un pedido por ID
    def eliminar_pedido(self, id_pedido: int):
        nodo_actual = self.cabeza
        anterior = None
        
        while nodo_actual is not None:
            if nodo_actual.pedido.id_pedido == id_pedido:
                if anterior is None:  
                    self.cabeza = nodo_actual.siguiente
                else:
                    anterior.siguiente = nodo_actual.siguiente
                return True  
            anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente
        return False  



#<------------------- CRUD (Productos) ------------------->
app = FastAPI()


# <--- Pydantic Productos ---->
class ModeloProducto(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    category: str 


#CREAR PRODUCTO (POST)
@app.post("/api/products/")
def create_product(product:ModeloProducto):
    arbol_productos = cargar_productos_desde_json()
    products = load_products()
    if product.id in products:
        raise HTTPException(status_code=400, detail="El producto ya existe")
    
    nuevo_producto = InteriorNodoProducto(product.id, product.name, product.price, product.quantity, product.category)
    nodo_producto = NodoProducto(nuevo_producto)
    arbol_productos.insertar(nodo_producto)  
    
    products[product.id] = product.model_dump()
    save_products(products)
    return product

#CONSULTAR PRODUCTO POR ID (GET)
@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    arbol_productos = cargar_productos_desde_json()
    producto_encontrado = arbol_productos.buscar(product_id)
    if not producto_encontrado:
        raise HTTPException(
            status_code=404,
            detail="Producto con ID {product_id] no encontrado"
        )
    return {"mensaje": "Se ha encontrado", "el producto": ModeloProducto(**producto_encontrado.producto.__dict__).model_dump()}


#LISTAR TODOS LOS PRODUCTOS (GET)
@app.get("/api/products/")
def list_products():
    return load_products()






#<--------------- CRUD (Pedidos) ---------------------->

# <--- Pydantic Pedidos ---->
class ModeloPedido(BaseModel):
    id: int
    Lista_productos: List[int]

@app.post("/api/orders/")
def create_order(order: ModeloPedido):
    orders = load_orders()
    arbol_productos = cargar_productos_desde_json()

    # Verificar si el ID del pedido ya existe
    if order.id in orders:
        raise HTTPException(status_code=400, detail="El pedido ya ha sido creado")

    productos_encontrados = []
    
    for product_id in order.Lista_productos:
        producto_nodo = arbol_productos.buscar(product_id)

        if producto_nodo:
            productos_encontrados.append({
                "id": producto_nodo.producto.id,
                "name": producto_nodo.producto.name,
                "price": producto_nodo.producto.price,
                "quantity": producto_nodo.producto.quantity,
                "category": producto_nodo.producto.category
            })
        else:
            productos_encontrados.append({
                "id": product_id,
                "mensaje": "Producto no encontrado"
            })


    order_data = order.dict()  
    order_data["Lista_productos"] = productos_encontrados  
    orders[order.id] = order_data 
    save_orders(orders)  

    return {"mensaje": "Pedido creado", "pedido": order_data}


#CONSULTAR PEDIDO POR ID (GET)
@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    orders = load_orders()
    arbol_productos = cargar_productos_desde_json()

    
    order_id_str = str(order_id)


    if order_id_str not in orders:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    order = orders[order_id_str]  
    productos_encontrados = []

   
    for producto in order["Lista_productos"]:
        product_id = producto["id"] 
        producto_nodo = arbol_productos.buscar(product_id)  
        
        if producto_nodo:
            productos_encontrados.append({
                "id": producto_nodo.producto.id,
                "name": producto_nodo.producto.name,
                "price": producto_nodo.producto.price,
                "quantity": producto_nodo.producto.quantity,
                "category": producto_nodo.producto.category
            })
        else:
            productos_encontrados.append({
                "id": product_id,
                "mensaje": "Producto no encontrado"
            })

    return {"id": order_id_str, "Lista_productos": productos_encontrados}



#ACTUALIZAR PEDIDO (PUT)


# PUT para actualizar un pedido
@app.put("/api/orders/{order_id}")
def update_order(order_id: str, order: ModeloPedido):
    orders = load_orders()  # Cargar los pedidos desde el archivo
    arbol_productos = cargar_productos_desde_json()  # Cargar los productos

    # Imprimir los pedidos cargados para depuración
    print(f"Pedidos cargados: {orders}")

    # Verificar si el pedido existe
    if order_id not in orders:
        raise HTTPException(status_code=404, detail=f"Pedido con id {order_id} no encontrado")

    # Crear una nueva lista de productos con la información completa (nombre, precio, etc.)
    productos_completos = []
    
    # Buscar los productos completos por su ID
    for product_id in order.Lista_productos:
        producto_nodo = arbol_productos.buscar(product_id)  # Buscar el producto en el árbol binario
        if producto_nodo:  # Si el producto se encuentra
            producto_completo = {
                "id": producto_nodo.producto.id,
                "name": producto_nodo.producto.name,
                "price": producto_nodo.producto.price,
                "quantity": producto_nodo.producto.quantity,
                "category": producto_nodo.producto.category
            }
            productos_completos.append(producto_completo)
        else:
            raise HTTPException(status_code=404, detail=f"Producto con id {product_id} no encontrado")
    
    # Actualizar el pedido con los productos completos
    order_data = {
        "id": order.id,
        "Lista_productos": productos_completos
    }

    # Reemplazar el pedido completo en el archivo
    orders[order_id] = order_data
    save_orders(orders)  # Guardamos los cambios en el archivo JSON

    return {"mensaje": "Pedido actualizado", "pedido": order_data}




#ELIMINAR UN PEDIDO (DELETE)
@app.delete("/api/orders/{order_id}")
def delete_order(order_id: str):
    orders = load_orders()
    if order_id not in orders:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )
    del orders[order_id]
    save_orders(orders) 
    return {"mensaje": "Pedido eliminado"}


#LISTAR TODOS LOS PEDIDOS (GET)
@app.get("/api/orders/")
def list_orders():
    return load_orders()



