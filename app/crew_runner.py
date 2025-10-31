from __future__ import annotations

from app.config import settings
from app.offline import run_offline_crew
from app.tools import search_sops


def _build_crew(task: str):
    """Lazy import so offline/tests work without heavy CrewAI side effects."""
    from crewai import Agent, Crew, Process, Task
    from crewai.tools import tool

    @tool("search_sops")
    def search_sops_tool(query: str) -> str:
        """Busca procedimientos SOP locales por palabras clave."""
        hits = search_sops(query, settings.corpus_dir, top_k=3)
        if not hits:
            return "No se encontraron SOPs."
        return "\n\n".join(f"[{h['id']}]\n{h['text'][:800]}" for h in hits)

    planner = Agent(
        role="Maintenance Planner",
        goal="Descomponer la incidencia industrial en un plan de pasos seguro y ordenado",
        backstory="Planificador de mantenimiento en planta con foco en tiempos de parada y coordinación.",
        allow_delegation=False,
        verbose=False,
    )
    technician = Agent(
        role="Field Technician Advisor",
        goal="Recuperar SOPs y proponer acciones técnicas concretas",
        backstory="Técnico de campo experto en cintas, prensas y utilaje industrial.",
        tools=[search_sops_tool],
        allow_delegation=False,
        verbose=False,
    )
    safety = Agent(
        role="Safety Critic",
        goal="Revisar riesgos, LOTO y EPP antes de ejecutar",
        backstory="Responsable de seguridad industrial; bloquea planes inseguros.",
        allow_delegation=False,
        verbose=False,
    )

    t_plan = Task(
        description=f"Crea un plan paso a paso para: {task}",
        expected_output="Lista numerada de pasos de intervención",
        agent=planner,
    )
    t_tech = Task(
        description=(
            f"Para la incidencia '{task}', usa search_sops y propone acciones técnicas citando SOPs."
        ),
        expected_output="Notas técnicas con referencias a SOPs",
        agent=technician,
        context=[t_plan],
    )
    t_safe = Task(
        description=(
            f"Revisa el plan y las notas técnicas para '{task}'. Señala riesgos LOTO/EPP y condiciones de arranque."
        ),
        expected_output="Dictamen de seguridad claro (OK / bloqueos)",
        agent=safety,
        context=[t_plan, t_tech],
    )

    crew = Crew(
        agents=[planner, technician, safety],
        tasks=[t_plan, t_tech, t_safe],
        process=Process.sequential,
        verbose=False,
    )
    return crew, t_plan, t_tech, t_safe


def run_crew(task: str) -> dict:
    if not settings.use_crewai:
        return run_offline_crew(task)

    crew, t_plan, t_tech, t_safe = _build_crew(task)
    crew.kickoff(inputs={"task": task})
    hits = search_sops(task, settings.corpus_dir, top_k=3)
    return {
        "plan": str(t_plan.output) if t_plan.output else "",
        "technician_notes": str(t_tech.output) if t_tech.output else "",
        "safety_review": str(t_safe.output) if t_safe.output else "",
        "sources": [h["id"] for h in hits],
        "mode": "crewai",
    }
