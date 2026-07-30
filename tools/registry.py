from tools.weather import weather_script
from tools.calculator import quick_calc, full_calc
from tools.github import github_tool
from tools.profile import remember_tool, profile_tool

TOOLS = {
    "/calc": full_calc,
    "/github": github_tool,
    "/math": quick_calc,
    "/profile": profile_tool,
    "/remember": remember_tool,
    "/weather": weather_script
}
