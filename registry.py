from tools.weather import weather_script
from tools.calculator import quick_calc, full_calc
from tools.github import github_tool

TOOLS = {
    "/weather": weather_script,
    "/math": quick_calc,
    "/calc": full_calc,
    "/github": github_tool
}
