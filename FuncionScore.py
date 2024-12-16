from fastapi import FastAPI, HTTPException
import pandas as pd
import os

# Definir la ruta del archivo CSV
file_path = os.path.join(os.path.dirname(__file__), 'FuncionScore.csv')

app = FastAPI()

df = pd.read_csv(file_path)
print(df.head())  # Verifica las primeras filas del DataFrame

# Obtener la URL base de las variables de entorno
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

@app.get("/")
def read_root():
    return {
        "message": (
            "Bienvenido a la API de películas.\n"
            "Usa el endpoint /score/?title=nombre_de_la_pelicula"
            "para obtener datos de una película específica.\n"
            "Por ejemplo: /score/?title=Toy%20Story"
            "\n"
            "O usa /titles"
            "para obtener el listado de películas.\n"
            "Por ejemplo: /titles"
            "\n"
            "Ejemplos de uso:\n"
            f"1. Obtener información de una película:\n"
            f"{BASE_URL}/score/?title=Toy%20Story"
            f"2. Listar todas las películas:\n"
            f"{BASE_URL}/titles"
        )
    }

@app.get("/score/")
async def get_movie(title: str):
    print(f"Buscando película: '{title}'")  # Muestra el título buscado
    movie = df[df['title'].str.lower() == title.lower()]
    print(f"Películas encontradas: {movie}")  # Muestra el DataFrame encontrado

    if movie.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie_data = movie.iloc[0]
    return {
        "title": movie_data['title'],
        "release_date": int(movie_data['release_year']),  # Convertir a int
        "vote_average": float(movie_data['vote_average'])  # Convertir a float
    }

@app.get("/titles/")
async def get_titles():
    print("Llamando al endpoint /titles/")  # Para diagnóstico
    return df['title'].tolist()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Instrucciones para ejecutar la aplicación:
# Ejecutar en la terminal: uvicorn main:app --reload
