# CrewAI Plant Crew

Crew multiagente con **CrewAI** para consultas sobre procedimientos de mantenimiento industrial (SOPs). Roles: planificador, técnico y crítico de seguridad.

Modo offline (sin API key) para demos/tests. Con `OPENAI_API_KEY` usa el crew real de CrewAI.

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Uso

```bash
python scripts/demo_run.py "Parada de emergencia en la cinta T901"
uvicorn app.main:app --reload --port 8010
pytest -q
```

## API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Estado y modo (offline/crewai) |
| POST | `/run` | `{ "task": "..." }` → plan + consejos + review de seguridad |

## Roles

- **planner** — descompone la incidencia en pasos
- **technician** — recupera SOPs y propone acciones
- **safety_critic** — revisa LOTO / EPP / riesgos
