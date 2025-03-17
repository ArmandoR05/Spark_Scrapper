import os
import matplotlib.pyplot as plt
import seaborn as sns
from WebScrapper import Scrapper
from DataProcessing import clean_data

def main():
    output_dir = "output/plots"
    os.makedirs(output_dir, exist_ok=True)
    
    Scrapper()

    # Limpiar
    df = clean_data()

    df.describe().to_csv("output/analysis_results.csv")
    # Distribución de Descuentos en los Productos
    plt.figure(figsize=(10, 5))
    sns.histplot(df['PERC_DESCUENTO'], bins=20, kde=True)
    plt.title("Distribución de Descuentos en los Productos")
    plt.xlabel("Porcentaje de Descuento")
    plt.ylabel("Cantidad de Productos")
    plt.savefig("output/plots/Distribución de Descuentos en los Productos.png")
    plt.show()



    # PROMEDIO DE  DESCUENTO POR CATEGORIA
    avg_discount_by_category = df.groupby('CATEGORIA')['PERC_DESCUENTO'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='CATEGORIA', y='PERC_DESCUENTO', data=avg_discount_by_category)
    plt.title("Promedio de Descuento por Categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Promedio de Descuento")
    plt.xticks(rotation=90)
    plt.savefig("output/plots/Promedio de Descuento por Categoría.png")
    plt.show()

    # PROMEDIO DE PRECIO ACTUAL POR CATEGORIA 
    avg_price_by_category = df.groupby('CATEGORIA')['PRECIO_ACTUAL'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='CATEGORIA', y='PRECIO_ACTUAL', data=avg_price_by_category)
    plt.title("Precio Promedio Actual por Categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Precio Promedio Actual")
    plt.xticks(rotation=90)
    plt.savefig("output/plots/Precio Promedio Actual por Categoría.png")
    plt.show()

    # CANTIDAD DE PRODUCTOS POR CATEGORIA
    category_count = df['CATEGORIA'].value_counts()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=category_count.index, y=category_count.values)
    plt.title("Número de Productos por Categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Número de Productos")
    plt.xticks(rotation=90)
    plt.savefig("output/plots/Número de Productos por Categoría.png")
    plt.show()

    print("Resultados en la carpeta output.")

if __name__ == "__main__":
    main()
