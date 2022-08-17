"""
globals
"""


__version__ = "0.1.5"


LIBRARY = "pyclickup"
API_URL = "https://api.clickup.com/api/v1/"


TEST_API_URL = "https://private-anon-efe850a7d7-clickup.apiary-mock.com/api/v1/"
TEST_TOKEN = "access_token"  # nosec


DEFAULT_STATUSES = [
    {"status": "Open", "type": "open", "orderindex": 0, "color": "#d3d3d3"},
    {"status": "todo", "type": "custom", "orderindex": 1, "color": "#ff00df"},
    {"status": "in progress", "type": "custom", "orderindex": 2, "color": "#f6762b"},
    {"status": "in review", "type": "custom", "orderindex": 3, "color": "#08adff"},
    {"status": "Closed", "type": "closed", "orderindex": 4, "color": "#6bc950"},
]
