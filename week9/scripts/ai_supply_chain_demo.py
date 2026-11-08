from datetime import datetime

with open("/tmp/ai_supply_chain_demo.log", "a") as f:
    f.write(f"AI Supply Chain test: {datetime.now()}\n")
