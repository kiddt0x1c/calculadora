import streamlit as st
from collections import defaultdict
import re

AVOGADRO = 6.022e23

MASAS_ATOMICAS = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81,
    "C": 12.01, "N": 14.01, "O": 16.00, "F": 18.998, "Ne": 20.180,
    "Na": 22.99, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
    "S": 32.06, "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
    "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938,
    "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38,
    "Ga": 69.723, "Ge": 72.630, "As": 74.922, "Se": 78.971, "Br": 79.904,
    "Kr": 83.798, "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
    "Nb": 92.906, "Mo": 95.95, "Tc": 98.0, "Ru": 101.07, "Rh": 102.91,
    "Pd": 106.42, "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71,
    "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29, "Cs": 132.91,
    "Ba": 137.33, "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24,
    "Pm": 145.0, "Sm": 150.36, "Eu": 151.96, "Gd": 157.25, "Tb": 158.93,
    "Dy": 162.50, "Ho": 164.93, "Er": 167.26, "Tm": 168.93, "Yb": 173.05,
    "Lu": 174.97, "Hf": 178.49, "Ta": 180.95, "W": 183.84, "Re": 186.21,
    "Os": 190.23, "Ir": 192.22, "Pt": 195.08, "Au": 196.97, "Hg": 200.59,
    "Tl": 204.38, "Pb": 207.2, "Bi": 208.98, "Po": 209.0, "At": 210.0,
    "Rn": 222.0, "Fr": 223.0, "Ra": 226.0, "Ac": 227.0, "Th": 232.04,
    "Pa": 231.04, "U": 238.03, "Np": 237.0, "Pu": 244.0, "Am": 243.0,
    "Cm": 247.0, "Bk": 247.0, "Cf": 251.0, "Es": 252.0, "Fm": 257.0,
    "Md": 258.0, "No": 259.0, "Lr": 262.0, "Rf": 267.0, "Db": 270.0,
    "Sg": 271.0, "Bh": 274.0, "Hs": 277.0, "Mt": 278.0, "Ds": 281.0,
    "Rg": 282.0, "Cn": 285.0, "Fl": 289.0, "Lv": 293.0, "Ts": 294.0,
    "Og": 294.0
}

def parse_formula(formula):
    tokens = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    comp = defaultdict(int)
    for (element, count) in tokens:
        if element not in MASAS_ATOMICAS:
            raise ValueError(f"Elemento desconocido: {element}")
        count = int(count) if count else 1
        comp[element] += count
    return dict(comp)

st.title("🧪 Calculadora Química - Grupo 2")

with st.expander("ℹ️ Instrucciones de uso"):
    st.markdown("""
    Esta aplicación te permite realizar cálculos químicos básicos. Sigue estos pasos:
    
    1. Usa el menú de la izquierda para elegir el tipo de cálculo.
    2. Ingresa los datos solicitados como masa, fórmula química o cantidad de moles.
    3. Presiona el botón **Calcular** para obtener el resultado.
    
    **Opciones disponibles:**
    - Calcular moles a partir de masa.
    - Calcular número de partículas (átomos, moléculas) usando el número de Avogadro.
    - Calcular la masa molar de un compuesto.
    - Obtener la composición porcentual de una fórmula.
    - Determinar la fórmula empírica y molecular.
    """)

menu = st.sidebar.selectbox("📘 Selecciona una operación:", [
    "Calcular Moles",
    "Número de Avogadro",
    "Masa Molar",
    "Composición Porcentual",
    "Fórmula Empírica y Molecular"
])

if menu == "Calcular Moles":
    st.header("🧮 Calcular Moles")
    masa = st.number_input("Masa en gramos (g):", min_value=0.0, format="%.6f")
    masa_molar = st.number_input("Masa molar (g/mol):", min_value=0.0, format="%.6f")
    if st.button("Calcular"):
        if masa_molar > 0:
            moles = masa / masa_molar
            st.success(f"Moles = {moles:.4f} mol")
        else:
            st.error("La masa molar debe ser mayor que cero.")

elif menu == "Número de Avogadro":
    st.header("🔬 Número de Avogadro")
    opcion = st.selectbox("¿Qué deseas calcular?", ["átomos", "moléculas", "partículas de un compuesto"])
    
    if opcion == "partículas de un compuesto":
        formula = st.text_input("Fórmula del compuesto (ej: H2O):")
        moles = st.number_input("Introduce los moles:", min_value=0.0, format="%.6f")
        if st.button("Calcular"):
            try:
                comp = parse_formula(formula)
                total_atomos = sum(comp.values())
                total_particulas = moles * AVOGADRO * total_atomos
                st.success(f"Total de partículas en {moles:.3f} mol de {formula}: {total_particulas:.3e}")
            except Exception as e:
                st.error(str(e))
    else:
        moles = st.number_input("Introduce los moles:", min_value=0.0, format="%.6f")
        if st.button("Calcular"):
            cantidad = moles * AVOGADRO
            st.success(f"{opcion.capitalize()} = {cantidad:.3e}")

elif menu == "Masa Molar":
    st.header("⚖️ Masa Molar")
    formula = st.text_input("Fórmula química (ej: H2O):")
    if st.button("Calcular"):
        try:
            comp = parse_formula(formula)
            masa = sum(MASAS_ATOMICAS[el] * n for el, n in comp.items())
            st.success(f"Masa Molar de {formula} = {masa:.3f} g/mol")
        except Exception as e:
            st.error(str(e))

elif menu == "Composición Porcentual":
    st.header("📊 Composición Porcentual")
    formula = st.text_input("Fórmula química (ej: H2O):")
    if st.button("Calcular"):
        try:
            comp = parse_formula(formula)
            masa_molar = sum(MASAS_ATOMICAS[el] * n for el, n in comp.items())
            resultado = ""
            for el, n in comp.items():
                masa_el = MASAS_ATOMICAS[el] * n
                porcentaje = (masa_el / masa_molar) * 100
                resultado += f"{el}: {porcentaje:.2f}%\n"
            st.text_area(f"Composición porcentual de {formula}:", value=resultado, height=150)
        except Exception as e:
            st.error(str(e))

elif menu == "Fórmula Empírica y Molecular":
    st.header("🧪 Fórmula Empírica y Molecular")
    n = st.number_input("¿Cuántos elementos hay?", min_value=1, step=1)
    masas = {}
    if n:
        for i in range(int(n)):
            el = st.text_input(f"Símbolo del elemento #{i+1}", key=f"el_{i}")
            masa = st.number_input(f"Masa en gramos de {el}:", min_value=0.0, format="%.6f", key=f"masa_{i}")
            if el and masa > 0:
                masas[el] = masa / MASAS_ATOMICAS.get(el, 1)
        if st.button("Calcular Fórmulas"):
            try:
                if not masas:
                    st.error("Introduce los datos correctamente.")
                else:
                    min_val = min(masas.values())
                    proporciones = {el: round(val / min_val) for el, val in masas.items()}
                    formula_empirica = ''.join([f"{el}{int(cant) if cant > 1 else ''}" for el, cant in proporciones.items()])
                    st.success(f"Fórmula empírica: {formula_empirica}")

                    masa_empirica = sum(MASAS_ATOMICAS[el] * cant for el, cant in proporciones.items())
                    masa_molecular = st.number_input("Introduce la masa molecular experimental:", min_value=0.0, format="%.6f")
                    if masa_molecular > 0:
                        factor = round(masa_molecular / masa_empirica)
                        formula_molecular = ''.join([f"{el}{int(cant * factor) if cant * factor > 1 else ''}" for el, cant in proporciones.items()])
                        st.success(f"Fórmula molecular: {formula_molecular}")
                    else:
                        st.info("Introduce una masa molecular experimental válida para calcular fórmula molecular.")
            except Exception as e:
                st.error(str(e))
