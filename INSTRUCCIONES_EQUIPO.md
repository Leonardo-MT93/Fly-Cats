# 🦁🦋🐅 LA TRIADA SALVAJE - INSTRUCCIONES DE EQUIPO

## 🎯 CONFIGURACIÓN INICIAL (SOLO UNA VEZ)

### 📁 CLONAR EL PROYECTO:
```bash
git clone https://github.com/Leonardo-MT93/Tp---Programacion1---UTN.git fly-cats-game
cd fly-cats-game
```

### 🔧 INSTALAR DEPENDENCIAS:
```bash
pip install pygame
```

### 🌿 CONFIGURAR TU RAMA DE TRABAJO:

#### 🦁 LEÓN:
```bash
git checkout -b feature/core
git push origin feature/core
```

#### 🦋 AGOSTINA:
```bash
git checkout -b feature/player
git push origin feature/player
```

#### 🐅 VISH:
```bash
git checkout -b feature/enemies  
git push origin feature/enemies
```

---

## 📂 ASIGNACIÓN DE ARCHIVOS

### 🦁 LEÓN - Game Manager & Integración
#### ✅ ARCHIVOS QUE PUEDES MODIFICAR:
- `main.py` ← Punto de entrada del juego
- `config.py` ← Configuraciones globales (resolución, FPS, colores)
- `utils.py` ← Funciones compartidas
- `game/game_manager.py` ← Lógica principal del juego
- `README.md` ← Documentación
- `INSTRUCCIONES_EQUIPO.md` ← Este archivo

#### ❌ ARCHIVOS QUE NO DEBES TOCAR:
- `game/player.py`
- `game/bullet.py`  
- `game/enemies.py`
- `game/powerups.py`

### 🦋 AGOSTINA - Player & Bullets System
#### ✅ ARCHIVOS QUE PUEDES MODIFICAR:
- `game/player.py` ← Clase del gato jugador
- `game/bullet.py` ← Clase de las bolas de lana
- `assets/player/` ← Sprites del gato
- `assets/bullets/` ← Sprites de bolas de lana

#### ❌ ARCHIVOS QUE NO DEBES TOCAR:
- `main.py`
- `game/game_manager.py`
- `game/enemies.py`
- `game/powerups.py`

### 🐅 VISH - Enemies & PowerUps System  
#### ✅ ARCHIVOS QUE PUEDES MODIFICAR:
- `game/enemies.py` ← Clase de perros robot
- `game/powerups.py` ← Clase de power-ups
- `assets/enemies/` ← Sprites de enemigos
- `assets/powerups/` ← Sprites de power-ups

#### ❌ ARCHIVOS QUE NO DEBES TOCAR:
- `main.py`
- `game/game_manager.py`
- `game/player.py`
- `game/bullet.py`

---

## 🚀 FLUJO DE TRABAJO DIARIO

### 🌅 AL COMENZAR A TRABAJAR:

#### 🦁 LEÓN:
```bash
# 1. Ir a tu carpeta del proyecto
cd fly-cats-game

# 2. Cambiar a tu rama
git checkout feature/core

# 3. Actualizar con cambios del equipo
git pull origin main

# 4. Verificar que estás en la rama correcta
git branch

# 5. ¡Empezar a coordinar e integrar!
# Edita: main.py, config.py, utils.py, game/game_manager.py
```

#### 🦋 AGOSTINA:
```bash
# 1. Ir a tu carpeta del proyecto
cd fly-cats-game

# 2. Cambiar a tu rama
git checkout feature/player

# 3. Actualizar con cambios del equipo
git pull origin main

# 4. Verificar que estás en la rama correcta
git branch

# 5. ¡Empezar a programar!
# Solo edita: game/player.py y game/bullet.py
```

#### 🐅 VISH:
```bash
# 1. Ir a tu carpeta del proyecto  
cd fly-cats-game

# 2. Cambiar a tu rama
git checkout feature/enemies

# 3. Actualizar con cambios del equipo
git pull origin main

# 4. Verificar que estás en la rama correcta
git branch

# 5. ¡Empezar a programar!
# Solo edita: game/enemies.py y game/powerups.py
```

---

## 💾 GUARDAR TU TRABAJO (DURANTE EL DÍA)

### 🦁 LEÓN:
```bash
# Verificar qué archivos cambiaste
git status

# Agregar solo TUS archivos
git add main.py config.py utils.py game/game_manager.py

# Commit y descripción clara de lo que avanzaste
git commit -m "🦁 Core: Integrate player and enemy systems"

# Subir a tu rama
git push origin feature/core
```

### 🦋 AGOSTINA:
```bash
# Verificar qué archivos cambiaste
git status

# Agregar solo TUS archivos
git add game/player.py game/bullet.py

# Commit y descripción clara de lo que avanzaste
git commit -m "🦋 Player: Add smooth movement controls"

# Subir a tu rama
git push origin feature/player
```

### 🐅 VISH:
```bash
# Verificar qué archivos cambiaste
git status

# Agregar solo TUS archivos
git add game/enemies.py game/powerups.py

# Commit y descripción clara de lo que avanzaste  
git commit -m "🐅 Enemies: Add robot dog AI patterns"

# Subir a tu rama
git push origin feature/enemies
```

---

## 🔄 INTEGRACIÓN SEMANAL (VIERNES)

### 🦁 LEÓN - PROCESO DE INTEGRACIÓN:
```bash
# 1. Cambiar a main y actualizar
git checkout main
git pull origin main

# 2. Traer TUS cambios de feature/core
git checkout feature/core
git pull origin feature/core
git checkout main
git merge feature/core

# 3. Traer cambios de Agostina
git checkout feature/player
git pull origin feature/player
git checkout main
git merge feature/player

# 4. Traer cambios de Vish  
git checkout feature/enemies
git pull origin feature/enemies
git checkout main
git merge feature/enemies

# 5. Resolver conflictos si los hay
# (Revisar archivos con <<<< ==== >>>>)

# 6. Probar que todo funcione
python main.py

# 7. Subir la integración
git push origin main

# 8. Avisar al equipo que pueden actualizar
```

### 🦁 LEÓN, 🦋 AGOSTINA y 🐅 VISH - ACTUALIZAR DESPUÉS DE INTEGRACIÓN:
```bash
# 1. Ir a tu rama
git checkout feature/core     # León
git checkout feature/player   # Agostina  
git checkout feature/enemies  # Vish

# 2. Traer cambios integrados
git pull origin main

# 3. ¡Continuar trabajando!
```

---

## 🆘 COMANDOS DE EMERGENCIA (Avisar por WSP/Discord)

### 🚨 SI ALGO SE ROMPE:
```bash
# Ver el estado actual
git status

# Ver historial de cambios
git log --oneline

# Volver al último commit que funcionaba
git reset --hard HEAD~1

# O volver a un commit específico
git reset --hard [código-del-commit]
```

### 🚨 SI HAY CONFLICTOS:
```bash
# Ver archivos en conflicto
git status

# Editar manualmente los archivos que tienen:
# <<<<<<< HEAD
# tu código  
# =======
# código de otra persona
# >>>>>>> rama

# Después de resolver:
git add [archivo-resuelto]
git commit -m "🦁 Fix: Resolve merge conflicts"
```

### 🚨 SI TE EQUIVOCAS DE RAMA:
```bash
# Guardar cambios temporalmente
git stash

# Cambiar a la rama correcta
git checkout feature/player  # o la que corresponda

# Recuperar cambios
git stash pop
```

---

## 📞 COMUNICACIÓN DEL EQUIPO

### 💬 ANTES DE MODIFICAR INTERFACES:
**SIEMPRE avisar en el grupo si vas a cambiar:**
- Nombres de funciones públicas
- Parámetros de funciones que usan otros
- Estructura de clases que otros importan

### 📝 FORMATO DE COMMITS (OPCIONAL PERO RECOMENDADO):

#### 🎨 CON EMOJIS (Para darle personalidad):
```bash
🦁 León:     "🦁 Core: descripción"
🦋 Agostina: "🦋 Player: descripción"  
🐅 Vish:     "🐅 Enemies: descripción"
```

#### 📝 SIN EMOJIS (También válido):
```bash
León:     "Core: descripción"
Agostina: "Player: descripción"  
Vish:     "Enemies: descripción"
```

#### ⌨️ CÓMO ESCRIBIR TU EMOJI ANIMAL:

**🦋 AGOSTINA (Mariposa):**
- **Windows:** Win + . (punto) → buscar "butterfly"  
- **Mac:** Cmd + Control + Espacio → buscar "mariposa"

**🐅 VISH (Tigre):**
- **Windows:** Win + . (punto) → buscar "tiger"
- **Mac:** Cmd + Control + Espacio → buscar "tigre"  

### 🆘 CUANDO PEDIR AYUDA:
- Error que no puedes resolver en 30 min
- Conflictos de merge complicados
- Cuando no sabes si tocar un archivo compartido
- Antes de cambiar algo que afecte a otros

---

## 🧪 TESTING BÁSICO

### 🔍 ANTES DE CADA COMMIT:
```bash
# Probar que el juego se ejecute sin errores
python main.py

# Si hay errores, revisarlos antes de commit
```

### 🦋 AGOSTINA - PROBAR:
- ✅ El gato se mueve con las flechas
- ✅ El gato dispara con ESPACIO
- ✅ No sale de los bordes de pantalla
- ✅ No hay errores en consola

### 🐅 VISH - PROBAR:
- ✅ Los enemigos aparecen y se mueven
- ✅ Los power-ups funcionan correctamente
- ✅ Los enemigos desaparecen al salir de pantalla
- ✅ No hay errores en consola

### 🦁 LEÓN - PROBAR:
- ✅ Todo se integra sin errores
- ✅ Las colisiones funcionan
- ✅ El juego inicia y termina correctamente
- ✅ Rendimiento acceptable (60 FPS)

---

## 🎯 OBJETIVOS SEMANALES

### 📅 SEMANA 1:
- 🦋 Agostina: Gato que se mueve y dispara básico
- 🐅 Vish: Enemigo simple que cae
- 🦁 León: Integración básica + colisiones

### 📅 SEMANA 2:
- 🦋 Agostina: Pulir movimiento + animaciones
- 🐅 Vish: Múltiples enemigos + power-up básico
- 🦁 León: Game over + reinicio + puntuación

---

## 🏆 REGLAS DE ORO DE LA TRIADA

1. **🤝 RESPETO:** Nunca toques archivos de otras integrantes
2. **💬 COMUNICACIÓN:** Avisa cambios que afecten a otros
3. **🧪 TESTING:** Siempre prueba antes de commit
4. **🆘 AYUDA:** Pide ayuda antes de frustrarte
5. **🎯 FOCUS:** Cada una en su especialidad
6. **✨ CALIDAD:** Mejor poco bien hecho que mucho mal hecho

---

## 📞 CONTACTOS DE EMERGENCIA

- **🦁 León:** [leonardotolaba.20@gmail.com]
- **🦋 Agostina:** [agostina.email@ejemplo.com]  
- **🐅 Vish:** [vish.email@ejemplo.com]
- **📱 Grupo:** La Triada Salvaje - WhatsApp/Discord

---

*🌟 "En la naturaleza del código, la triada nunca falla" - La Triada Salvaje 🦁🦋🐅*

**¡A PROGRAMAR! 🚀🎮**