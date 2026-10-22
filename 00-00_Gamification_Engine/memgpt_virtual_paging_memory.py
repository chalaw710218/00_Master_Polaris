"""
Polaris Bionic Learning System - Cycle 07 Code-as-Memory Module
Title: MemGPT Virtual Paging Memory Manager (Hierarchical Cognitive Memory OS)
Reference: Charles Packer, Ion Stoica, Joseph E. Gonzalez et al., UC Berkeley (2023)
Architecture: In-Context Working Memory -> Recall Memory (FIFO Queue) -> Archival Long-Term Disk
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class WorkingMemory:
    founder_profile: str
    active_agent_persona: str
    current_mission_goal: str

class MemGPTVirtualMemoryManager:
    """
    仿生 MemGPT 虛擬分頁記憶體管理器 (Polaris Edition)
    模擬作業系統虛擬記憶體機制，讓 Agent 在有限 Context 限制下實現跨週期、無限長時程的心智持久化。
    """
    def __init__(self, agent_name: str, max_fifo_size: int = 5):
        self.agent_name = agent_name
        self.max_fifo_size = max_fifo_size
        self.working_memory = WorkingMemory(
            founder_profile="陳品碩 (Pinshuo / 闆仔), 40歲台灣創業者, 務實商道, 零廢話",
            active_agent_persona=f"Polaris Cabinet Role: {agent_name}",
            current_mission_goal="推動極星百億上市社企, 在地創生, 仿生自進化"
        )
        self.recall_memory_fifo: List[str] = []
        self.archival_database: Dict[str, str] = {}

    def insert_recall_message(self, message: str):
        """寫入短期 Recall FIFO 記憶體，超出上限時自動分頁寫出 (Page-out) 至 Archival 庫"""
        self.recall_memory_fifo.append(message)
        if len(self.recall_memory_fifo) > self.max_fifo_size:
            evicted = self.recall_memory_fifo.pop(0)
            archive_key = f"ARCH_{len(self.archival_database) + 1:04d}"
            self.archival_database[archive_key] = evicted

    def search_archival_memory(self, query: str) -> List[str]:
        """按關鍵字檢索長期冷儲存 (Archival Memory Search)"""
        hits = []
        for k, v in self.archival_database.items():
            if query.lower() in v.lower():
                hits.append(f"[{k}] {v}")
        return hits

    def compile_in_context_prompt(self) -> str:
        """編譯主記憶體視窗 (In-Context RAM)"""
        return (
            f"=== CORE WORKING MEMORY ===\n"
            f"Founder: {self.working_memory.founder_profile}\n"
            f"Role: {self.working_memory.active_agent_persona}\n"
            f"Goal: {self.working_memory.current_mission_goal}\n\n"
            f"=== RECALL MEMORY FIFO ({len(self.recall_memory_fifo)} items) ===\n"
            + "\n".join(f"- {msg}" for msg in self.recall_memory_fifo)
        )

if __name__ == "__main__":
    mem = MemGPTVirtualMemoryManager("CEO_Yuki", max_fifo_size=3)
    # 寫入多條工作記憶
    mem.insert_recall_message("Event 1: 成立家宅戰情室")
    mem.insert_recall_message("Event 2: 審計大明毛豆底價")
    mem.insert_recall_message("Event 3: 升級仿生學習系統 v3.0")
    mem.insert_recall_message("Event 4: Eureka 演化模組實測通過")  # Event 1 自動分頁被擠入 Archival
    mem.insert_recall_message("Event 5: 啟動 10 輪自進化攻堅")

    print(mem.compile_in_context_prompt())
    print("\nArchival Search for '毛豆':", mem.search_archival_memory("毛豆"))
    print("Archival Search for '家宅':", mem.search_archival_memory("家宅"))
