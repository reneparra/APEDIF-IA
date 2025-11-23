<<<<<<< HEAD
# 🔍 APEDIF IA

**Análisis de Evidencia Digital Forense con Inteligencia Artificial**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## 📖 Descripción

APEDIF IA es un prototipo educativo de análisis forense digital que integra inteligencia artificial local (Llama 3.1 8B) para asistir en la interpretación de evidencia digital. Desarrollado como Trabajo Final de Licenciatura en Ciencias de Datos.

### Características principales

- ✅ **Análisis forense automatizado** de sistemas de archivos y actividad de red
- ✅ **Inteligencia artificial local** con Llama 3.1 8B (sin envío de datos a la nube)
- ✅ **Generación de datos sintéticos** para entrenamiento y validación ética
- ✅ **Interfaz gráfica moderna** con CustomTkinter
- ✅ **Reportes visuales** en HTML con gráficos interactivos
- ✅ **Evaluación de riesgo** multifactor con categorización de amenazas

---

## 🎯 Propósito

Este proyecto demuestra la viabilidad técnica de integrar IA local en herramientas forenses educativas, promoviendo:

- Accesibilidad tecnológica sin dependencias costosas
- Soberanía digital mediante procesamiento local
- Formación práctica en análisis forense sin comprometer evidencia real

⚠️ **Importante:** APEDIF IA es un prototipo académico, **no validado para uso en investigaciones forenses reales**.

---

## 💻 Requisitos del Sistema

### Mínimos
- Windows 10/11 (64-bit)
- Python 3.11+
- 8 GB RAM
- 10 GB espacio libre

### Recomendados
- Intel i5-12400F o superior
- 16-32 GB RAM
- NVIDIA RTX 3070 8GB (para mejor rendimiento IA)
- SSD con 20+ GB libres

---

## 🚀 Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/APEDIF-IA.git
cd APEDIF-IA
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Instalar Ollama y modelo

1. Descargar Ollama: https://ollama.ai/download/windows
2. Instalar y reiniciar el sistema
3. Descargar modelo:
```bash
ollama pull llama3.1:8b
```

### 5. Crear estructura de directorios
```bash
mkdir C:\ForensicAI\logs
mkdir C:\ForensicAI\reportes
mkdir C:\ForensicAI\casos_reales\casos_procesados
```

### 6. Ejecutar APEDIF IA
```bash
cd src
python forensic_gui_app.py
```

📖 **Para instalación detallada:** Ver `docs/Manual_Instalacion_APEDIF_IA.pdf`

---

## 📂 Estructura del Proyecto
```
APEDIF_IA/
├── src/
│   ├── forensic_data_generator.py    # Generador de casos sintéticos
│   ├── forensic_analyzer.py          # Motor de análisis forense
│   ├── ai_forensic_assistant.py      # Asistente IA local
│   └── forensic_gui_app.py           # Interfaz gráfica
├── docs/
│   └── Manual_Instalacion_APEDIF_IA.pdf
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 🎓 Uso Educativo

### Generar caso sintético y analizar

1. Abrir APEDIF IA
2. Seleccionar tipo de caso (ej: "employee_data_theft")
3. Click en **"🔍 Análisis"**
4. Ver resultados en pestañas (Resumen, Archivos, Red)
5. Click en **"🤖 IA"** para análisis inteligente
6. Click en **"📄 Reporte"** para generar documentación

### Casos sintéticos disponibles

- `employee_data_theft` - Robo de información confidencial
- `intellectual_property_theft` - Robo de propiedad intelectual
- `malware_infection` - Infección de malware
- `ransomware_attack` - Ataque de ransomware
- `financial_fraud` - Fraude financiero

---

## 🤝 Contribuciones

Este proyecto es de código abierto y acepta contribuciones académicas:

- 🐛 Reporte de bugs
- 💡 Sugerencias de mejora
- 📝 Mejoras de documentación
- 🔧 Nuevos módulos de análisis

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍🎓 Autor

**René Alejandro Parra Almirón**

- 📧 Email: [RENE.PARRA82@GMAIL.COM]
- 🎓 Licenciatura en Ciencias de Datos
- 🏫 Universidad Católica de Salta (UCASAL)
- 📅 Año: 2025

---

## 🙏 Agradecimientos

- **Institución:** Universidad Católica de Salta
- **Tecnologías utilizadas:** Python, CustomTkinter, Ollama, Llama 3.1 8B

---

## 📚 Documentación Adicional

- 📖 [Manual de Instalación Completo](docs/Manual_Instalacion_APEDIF_IA.pdf)
- 📝 Trabajo Final de Grado (próximamente)

---

## ⚠️ Disclaimer

APEDIF IA es un **prototipo educativo** desarrollado con fines académicos. No está validado para uso en investigaciones forenses reales ni como herramienta pericial judicial. El sistema procesa únicamente datos sintéticos en su configuración por defecto.

---

## 🔗 Enlaces Útiles

- [Ollama](https://ollama.ai/) - Plataforma de IA local
- [CustomTkinter](https://customtkinter.tomschimansky.com/) - Framework GUI
- [Python](https://www.python.org/) - Lenguaje de programación
=======
# APEDIF-IA
Análisis de Evidencia Digital Forense con Inteligencia Artificial - Prototipo educativo con IA local
>>>>>>> d10b1bf769c0bb76875e94036e632cd0309db81e
