# Tanks Game 

## Descriere

**Tanks Game ** este un joc 2D turn-based unde doi jucători controlează tancuri pe un teren realist generat procedural. Scopul este să distrugi tancul adversarului folosind proiectile cu diferite tipuri de muniție, ținând cont de unghiul și puterea lansării.

Jocul include:
- Teren cu dealuri generate procedural și crateruri create după explozii.
- Mișcare realistă a tancurilor, limitată de teren și combustibil.
- Două tipuri de proiectile: standard și homing (urmăresc ținta).
- Interfață intuitivă cu afișarea vieții, combustibilului, puterii și unghiului.
- Posibilitatea de a introduce numele proprii pentru fiecare jucător.
- Ecran de start pentru introducerea numelor și ecran de final cu opțiuni de restart sau ieșire.
- Fundal animat cu cer și textură pentru teren.

---

## Cum se joacă

- **Mișcare tanc**:  
  - `A` și `D` pentru deplasare stânga/dreapta (consumă combustibil)  
- **Ajustare unghi**:  
  - `UP` și `DOWN` pentru a crește/scădea unghiul tunului  
- **Ajustare putere**:  
  - `RIGHT` și `LEFT` pentru a crește/scădea puterea lansării  
- **Schimbare tip proiectil**:  
  - `1` pentru proiectil standard  
  - `2` pentru proiectil homing  
- **Lansare proiectil**:  
  - `SPACE` pentru a trage  
- **Pe ecranul de final**:  
  - `R` pentru restart  
  - `Q` pentru ieșire din joc

---

## Cerințe

- Python 3.x  
- Pygame (`pip install pygame`)

---

## Cum să rulezi jocul

1. Clonează acest repository:

   ```bash
   git clone https://github.com/utilizatorul-tau/tanks-game.git
   cd tanks-game

