from datetime import datetime
from typing import List
from backend.database.nosql.model.battery_knowledge import BatteryKnowledge

BATTERY_KNOWLEDGE_DATA: List[BatteryKnowledge] = [
    # Basic Technology
    BatteryKnowledge(
        title="Lithium-Ion Battery Fundamentals",
        content="""
        Lithium-ion batteries are rechargeable power sources that operate through the movement of lithium ions.
        Key characteristics:
        1. High energy density (150-200 Wh/kg)
        2. No memory effect
        3. Low self-discharge rate (2-3% per month)
        4. High cycle life (500-1500 cycles)
        5. Operating voltage: 3.6V nominal
        
        The four main components are:
        - Cathode (positive electrode)
        - Anode (negative electrode)
        - Electrolyte
        - Separator
        """,
        category="technology",
        tags=["lithium-ion", "basics", "components", "specifications"]
    ),
    
    # Battery Chemistry
    BatteryKnowledge(
        title="Common Battery Chemistries",
        content="""
        Different lithium-ion chemistries offer varying advantages:
        
        1. NMC (Lithium Nickel Manganese Cobalt Oxide):
           - High energy density
           - Good thermal stability
           - Used in EVs and grid storage
        
        2. LFP (Lithium Iron Phosphate):
           - Excellent safety profile
           - Long cycle life
           - Lower cost
           - Common in stationary storage
        
        3. NCA (Lithium Nickel Cobalt Aluminum Oxide):
           - Highest energy density
           - Used in Tesla vehicles
           - More sensitive to temperature
        
        4. LTO (Lithium Titanate):
           - Exceptional cycle life
           - Very fast charging
           - Lower energy density
           - Higher cost
        """,
        category="technology",
        tags=["chemistry", "NMC", "LFP", "NCA", "LTO"]
    ),
    
    # Maintenance and Operation
    BatteryKnowledge(
        title="Optimal Charging Patterns",
        content="""
        For maximum battery life, follow these guidelines:
        1. Avoid frequent deep discharges below 20% SoC
        2. Maintain charge levels between 20-80% for daily use
        3. Charge at moderate C-rates (0.5C to 1C)
        4. Avoid extreme temperatures (<0°C or >45°C)
        5. Use occasional full charges for cell balancing
        
        Charging speeds:
        - Slow charging: 0.2C to 0.5C
        - Standard charging: 0.5C to 1C
        - Fast charging: 1C to 3C
        - Ultra-fast charging: >3C
        
        Regular cycling between 20-80% can extend battery life by up to 40%.
        """,
        category="maintenance",
        tags=["charging", "lifecycle", "best-practices", "temperature"]
    ),
    
    # Grid Integration
    BatteryKnowledge(
        title="Grid Frequency Regulation",
        content="""
        Batteries provide essential grid frequency regulation services:
        
        1. Primary Response:
           - Response time: <1 second
           - Duration: Up to 15 minutes
           - Automatic response to frequency deviations
        
        2. Secondary Response:
           - Response time: <10 seconds
           - Duration: Up to 30 minutes
           - Managed by grid operators
        
        3. Benefits:
           - Grid stability improvement
           - Reduced need for spinning reserves
           - Revenue generation potential
           - Carbon emission reduction
        
        Typical payment rates: $30-50/MWh for frequency regulation services.
        """,
        category="grid-services",
        tags=["frequency-regulation", "grid-services", "revenue", "response-time"]
    ),
    
    # Market Analysis
    BatteryKnowledge(
        title="Energy Market Peak Hours",
        content="""
        Energy markets typically experience demand peaks:
        
        1. Morning Peak (7-9 AM):
           - Residential demand surge
           - Commercial startup
           - Average price premium: 25-40%
        
        2. Evening Peak (5-8 PM):
           - Highest daily demand
           - Residential + Commercial overlap
           - Average price premium: 40-60%
        
        3. Seasonal Variations:
           - Summer peaks: Air conditioning load
           - Winter peaks: Heating and lighting
           - Shoulder seasons: Lower demand
        
        Optimal battery dispatch strategy:
        - Charge during off-peak (11 PM - 5 AM)
        - Discharge during peak periods
        - Monitor real-time pricing signals
        """,
        category="market",
        tags=["peak-hours", "demand", "pricing", "dispatch"]
    ),
    
    # Performance Metrics
    BatteryKnowledge(
        title="Battery Performance Metrics",
        content="""
        Key metrics for evaluating battery performance:
        
        1. Round-Trip Efficiency:
           - AC-AC: 85-90%
           - DC-DC: 90-95%
           - Factors: Temperature, C-rate, SoC
        
        2. Cycle Life:
           - LFP: 3000-5000 cycles
           - NMC: 1500-3000 cycles
           - Defined at 80% capacity retention
        
        3. Response Time:
           - Power electronics: <100ms
           - Full power delivery: <1s
           - Ramp rate: Up to 100% per second
        
        4. Energy Density:
           - Volumetric: 200-400 Wh/L
           - Gravimetric: 150-250 Wh/kg
        """,
        category="technology",
        tags=["metrics", "efficiency", "cycle-life", "response-time"]
    ),
    
    # Safety and Risk Management
    BatteryKnowledge(
        title="Battery Safety Protocols",
        content="""
        Essential safety measures for battery systems:
        
        1. Thermal Management:
           - Operating range: 15-35°C optimal
           - Cooling systems: Air, liquid, phase change
           - Temperature monitoring points
        
        2. Fire Safety:
           - Fire suppression systems
           - Thermal runaway detection
           - Emergency ventilation
           - Isolation protocols
        
        3. Electrical Safety:
           - Insulation monitoring
           - Ground fault detection
           - Arc flash protection
           - Emergency disconnects
        
        4. Regular Inspections:
           - Monthly visual inspections
           - Quarterly performance tests
           - Annual safety system checks
        """,
        category="safety",
        tags=["safety", "thermal-management", "fire-protection", "maintenance"]
    ),
    
    # Environmental Impact
    BatteryKnowledge(
        title="Environmental Considerations",
        content="""
        Environmental aspects of battery systems:
        
        1. Carbon Footprint:
           - Manufacturing: 75-100 kg CO2/kWh
           - Operation: Depends on grid mix
           - End-of-life: Recycling reduces impact
        
        2. Material Recovery:
           - Lithium recovery rate: 90%+
           - Cobalt recovery rate: 95%+
           - Nickel recovery rate: 90%+
           - Aluminum/Copper: 98%+
        
        3. Recycling Process:
           - Hydrometallurgical
           - Pyrometallurgical
           - Direct recycling
           - Combined approaches
        
        4. Sustainability Initiatives:
           - Circular economy approach
           - Supply chain transparency
           - Responsible sourcing
           - Life cycle assessment
        """,
        category="environmental",
        tags=["recycling", "carbon-footprint", "sustainability", "materials"]
    ),
    
    # Economic Analysis
    BatteryKnowledge(
        title="Battery Economics",
        content="""
        Economic factors in battery storage:
        
        1. Capital Costs (2023):
           - Utility scale: $200-300/kWh
           - Commercial: $400-600/kWh
           - Residential: $800-1000/kWh
        
        2. Revenue Streams:
           - Energy arbitrage: $50-100/kW-year
           - Frequency regulation: $30-50/MWh
           - Capacity payments: $75-150/kW-year
           - Demand charge reduction: $100-200/kW-year
        
        3. Operating Costs:
           - O&M: $8-15/kW-year
           - Insurance: 0.5-1% of CAPEX
           - Warranty: 1-2% of CAPEX
           - Performance degradation: 2%/year
        
        4. Project Finance:
           - Typical IRR: 10-15%
           - Payback period: 5-8 years
           - Project life: 10-15 years
           - Warranty period: 10 years
        """,
        category="economics",
        tags=["costs", "revenue", "finance", "investment"]
    ),
    
    # Future Trends
    BatteryKnowledge(
        title="Emerging Battery Technologies",
        content="""
        Next-generation battery technologies:
        
        1. Solid-State Batteries:
           - Higher energy density
           - Improved safety
           - Expected commercialization: 2025+
           - Challenges: Manufacturing scale
        
        2. Flow Batteries:
           - Unlimited cycle life
           - Independent power/energy scaling
           - Lower energy density
           - Applications: Grid storage
        
        3. Sodium-Ion:
           - Lower cost than lithium
           - Abundant materials
           - Lower energy density
           - Market entry: 2024-2025
        
        4. Other Technologies:
           - Lithium-sulfur
           - Metal-air batteries
           - Structural batteries
           - Dual-ion systems
        """,
        category="technology",
        tags=["future", "innovation", "solid-state", "flow-batteries"]
    )
]

async def populate_battery_knowledge():
    """Populate MongoDB with battery knowledge data."""
    from ..mongodb import MongoDBConnection
    
    mongo = MongoDBConnection()
    collection = mongo.get_collection(BatteryKnowledge.Config.collection_name)
    
    # Clear existing data
    await collection.delete_many({})
    
    # Insert new data
    documents = [knowledge.model_dump() for knowledge in BATTERY_KNOWLEDGE_DATA]
    await collection.insert_many(documents)
    
    print(f"Inserted {len(documents)} battery knowledge documents")

if __name__ == "__main__":
    import asyncio
    asyncio.run(populate_battery_knowledge()) 