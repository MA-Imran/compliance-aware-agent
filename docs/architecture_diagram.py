# docs/architecture_diagram.py
"""
Architecture Diagram Generator for Compliance-Aware Multi-Agent System
Generates a visual representation of the system architecture
"""

def generate_architecture_diagram():
    """Generate ASCII architecture diagram"""
    diagram = """
COMPLIANCE-AWARE MULTI-AGENT SYSTEM ARCHITECTURE
================================================================================

                            ┌─────────────────────────────────┐
                            │   USER INTERFACE LAYER          │
                            │                                 │
                            │  • run_system.py (CLI)          │
                            │  • Interactive Mode             │
                            │  • Example Queries              │
                            └───────────┬─────────────────────┘
                                        │
                                        ▼
                    ┌─────────────────────────────────┐
                    │    ORCHESTRATION LAYER          │
                    │                                 │
                    │  EnhancedComplianceAwareAgent-  │
                    │  System (Main Coordinator)      │
                    │                                 │
                    │  • Query Processing Pipeline    │
                    │  • Agent Coordination           │
                    │  • Error Handling               │
                    │  • Performance Monitoring       │
                    └─────┬─────────────┬─────────────┘
                          │             │
                          ▼             ▼

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         AGENT LAYER                                     │
    │                                                                         │
    │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
    │  │ RETRIEVAL   │  │  REASONING   │  │ COMPLIANCE   │  │   MEMORY     │  │
    │  │   AGENT     │  │    AGENT     │  │    AGENT     │  │   SYSTEM     │  │
    │  │             │  │              │  │              │  │              │  │
    │  │ • API Calls │  │ • Chain-of-  │  │ • HIPAA      │  │ • SQLite     │  │
    │  │ • Mock Data │  │   Thought    │  │   Checks     │  │   Database   │  │
    │  │ • Fallback  │  │ • Hypothesis │  │ • GDPR       │  │ • Query      │  │
    │  │   Handling  │  │   Generation │  │   Validation │  │   History    │  │
    │  │ • Location  │  │ • Pattern    │  │ • Data       │  │ • Agent      │  │
    │  │   Extraction│  │   Recognition│  │   Retention  │  │   Performance│  │
    │  │             │  │ • Confidence │  │ • Violation  │  │ • Compliance │  │
    │  │             │  │   Scoring    │  │   Logging    │  │   Logging    │  │
    │  └─────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
    │        │                  │                 │                 │          │
    └────────┼──────────────────┼─────────────────┼─────────────────┼──────────┘
             │                  │                 │                 │
             ▼                  ▼                 ▼                 ▼

    ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐
    │ EXTERNAL    │  │  REASONING   │  │ COMPLIANCE   │  │   PERSISTENT      │
    │ DATA        │  │  ARTIFACTS   │  │  RESULTS     │  │   STORAGE         │
    │ SOURCES     │  │              │  │              │  │                   │
    │             │  │ • Structured │  │ • Regulation │  │ • agent_memory.db │
    │ • Open-     │  │   Insights   │  │   Reports    │  │ • Query History   │
    │   Weather   │  │ • Reasoning  │  │ • Violation  │  │ • Performance     │
    │   Map API   │  │   Chain      │  │   Details    │  │   Metrics         │
    │ • Mock Data │  │ • Hypotheses │  │ • Compliance │  │ • System Insights │
    │   Generators│  │ • Patterns   │  │   Status     │  │ • Learning Data   │
    │             │  │ • Confidence │  │ • Audit Trail│  │                   │
    └─────────────┘  │   Scores     │  │              │  └───────────────────┘
                     └──────────────┘  └──────────────┘


DATA FLOW SEQUENCE (Think-Act-Learn-Govern Cycle):
────────────────────────────────────────────────────────────────────────────────

    THINK          ACT            LEARN           GOVERN
     ↓             ↓               ↓               ↓
┌─────────┐   ┌─────────┐   ┌───────────┐   ┌─────────────┐
│ Reasoning│   │Retrieval│   │  Memory   │   │ Compliance  │
│  Agent   │   │ Agent   │   │  System   │   │   Agent     │
└────┬─────┘   └────┬────┘   └─────┬─────┘   └──────┬──────┘
     │               │              │                │
     │ 1. Understand │              │                │
     │    Data       │              │                │
     │               │              │                │
     │ 2. Generate   │              │                │
     │    Hypotheses │              │                │
     │               │              │                │
     │ 3. Identify   │              │                │
     │    Patterns   │              │                │
     │               │              │                │
     │ 4. Synthesize │              │                │
     │    Insights   │              │                │
     └───────┬───────┘              │                │
             │                       │                │
             └───────────────────────┼────────────────┘
                                     │
                             ┌───────┴───────┐
                             │  Final Output │
                             │  with Compliance│
                             │  Validation    │
                             └───────────────┘


AGENT COMMUNICATION PATTERN:
───────────────────────────
User Query
    │
    ▼
Orchestrator → Retrieval Agent → Data
    │
    ▼
Orchestrator → Reasoning Agent → Insights
    │
    ▼
Orchestrator → Compliance Agent → Validation
    │
    ▼
Orchestrator → Memory System → Learning
    │
    ▼
Structured Response to User

================================================================================
"""
    return diagram

def generate_data_flow_diagram():
    """Generate detailed data flow diagram"""
    flow_diagram = """
DATA PROCESSING PIPELINE - DETAILED FLOW
================================================================================

USER QUERY: "What's the weather in Paris and potential impacts?"
────────────────────────────────────────────────────────────────────────────────

STEP 1: RETRIEVAL PHASE
├── Input: User query
├── Process: Extract location, determine data type
├── Action: Fetch from API (fallback to mock data)
├── Output: Structured weather data
└── Example: {location: "Paris", temperature: 22.5, humidity: 65, ...}

STEP 2: REASONING PHASE (Chain-of-Thought)
├── Step 2.1: Data Understanding
│   └── Analyze structure, field types, data quality
├── Step 2.2: Hypothesis Generation
│   └── "Comfortable temperature for outdoor activities"
│   └── "Moderate humidity levels"
├── Step 2.3: Pattern Recognition
│   └── Identify correlations between temperature/humidity
├── Step 2.4: Context Analysis
│   └── Map to user intent, assess relevance
├── Step 2.5: Insight Synthesis
│   └── Generate natural language response
│   └── Calculate confidence score (0.85)
└── Output: Structured insights with reasoning chain

STEP 3: COMPLIANCE PHASE
├── HIPAA Check: Scan for medical/PHI data → ✅ Compliant
├── GDPR Check: Scan for personal data → ✅ Compliant
├── Data Retention: Check timestamp freshness → ✅ Compliant
└── Output: Compliance validation report

STEP 4: MEMORY PHASE
├── Log query and success status
├── Update agent performance metrics
├── Store compliance violations (if any)
├── Generate system insights
└── Update learning models

STEP 5: FINAL OUTPUT
├── Structured response to user
├── Compliance status
├── Performance metrics
├── System recommendations
└── Audit trail

================================================================================
"""
    return flow_diagram

if __name__ == "__main__":
    print(generate_architecture_diagram())
    print("\n" + "="*80 + "\n")
    print(generate_data_flow_diagram())