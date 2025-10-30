from __future__ import annotations

from app.config import settings
from app.tools import search_sops


def run_offline_crew(task: str) -> dict:
    """Mirror CrewAI roles without calling an LLM (CI / demo)."""
    hits = search_sops(task, settings.corpus_dir, top_k=3)
    sources = [h["id"] for h in hits]
    excerpts = "\n\n".join(f"### {h['title']}\n{h['text'][:500]}" for h in hits) or "Sin SOP coincidente."

    plan = (
        "1) Aislar la zona y confirmar paro de máquina.\n"
        "2) Aplicar LOTO según SOP aplicable.\n"
        "3) Diagnosticar causa raíz con checklist del técnico.\n"
        "4) Ejecutar corrección y verificar arranque controlado.\n"
        "5) Registrar incidencia y liberar candados."
    )
    technician = (
        f"Incidencia: {task}\n\n"
        f"SOPs recuperados ({len(hits)}):\n{excerpts}\n\n"
        "Acciones sugeridas: seguir el procedimiento recuperado, no saltar bloqueos de seguridad."
    )
    safety = (
        "Review de seguridad: verificar EPP, LOTO completo, cero energía residual y "
        "comunicación con supervisión antes de reenergizar. "
        "Si hay interacción humano-máquina, mantener distancias y señalización."
    )
    return {
        "plan": plan,
        "technician_notes": technician,
        "safety_review": safety,
        "sources": sources,
        "mode": "offline",
    }
