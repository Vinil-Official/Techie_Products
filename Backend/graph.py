# from langgraph.graph import (
#     StateGraph,
#     START,
#     END
# )

# from state import LeadState

# from agents.input_agent import input_agent
# from agents.discovery_agent import discovery_agent


# graph = StateGraph(LeadState)


# # -----------------------------
# # NODES
# # -----------------------------

# graph.add_node(
#     "input_agent",
#     input_agent
# )

# graph.add_node(
#     "discovery_agent",
#     discovery_agent
# )


# # -----------------------------
# # FLOW
# # -----------------------------

# graph.add_edge(
#     START,
#     "input_agent"
# )

# # graph.add_edge(
# #     "input_agent",
# #     "discovery_agent"
# # )

# graph.add_edge(
#     "input_agent",
#     END
# )


# # -----------------------------
# # COMPILE
# # -----------------------------

# app = graph.compile()

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from state import LeadState

from agents.input_agent import input_agent

from agents.website_discovery import (
    website_discovery
)

from agents.Website_Analyzer import (
    website_analyzer
)


# ============================================================
# GRAPH
# ============================================================

builder = StateGraph(
    LeadState
)


# ============================================================
# NODES
# ============================================================

builder.add_node(
    "input_agent",
    input_agent
)

builder.add_node(
    "website_discovery",
    website_discovery
)

builder.add_node(
    "website_analyzer",
    website_analyzer
)


# ============================================================
# EDGES
# ============================================================

builder.add_edge(
    START,
    "input_agent"
)

builder.add_edge(
    "input_agent",
    "website_discovery"
)

builder.add_edge(
    "website_discovery",
    "website_analyzer"
)

builder.add_edge(
    "website_analyzer",
    END
)


# ============================================================
# COMPILE
# ============================================================

app = builder.compile()